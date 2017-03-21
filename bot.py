import math
import os


#input:  d - dictionary
#        l - list of strings l
#updates dictionary with frequency of strings in l

def add_dict(d, l):
    for token in l:
        if token in d:
            d[token] += 1
        else:
            d[token] = 1


#input:  line - String
#output: list of token strings

def tokenize(line):
	result = line.lower().split()
	for i in xrange(len(result)): #remove punctuation marks
		if not result[i][-1].isalnum():
			result[i] = result[i][:-1]
	return result


#input: file to learn from
#won't be needed when the database class is implemented

def process(input_file):
    l = []
    f = open(input_file, 'r')

    curr_reply = ''        
    curr_counts = {}       #token counts
    curr_num_tokens = 0    #number of tokens in all inputs to current reply
    curr_id = -1
    transitions_count = {}
    
    for line in f:
        if line[0] == '\n': #marks end of this reply: get ready for next reply in file
            l.append((curr_reply, curr_counts, curr_num_tokens , curr_id))
            curr_reply = ''
            curr_counts = {}
            curr_num_tokens = 0
            curr_id = -1

        elif line[0] == '+': #new reply
            curr_reply = line[1:-1] #extract string part from line

        elif line[0] == '-': #input line
            line_arr = tokenize(line[1:]) #preprocess line
            add_dict(curr_counts, line_arr) #update token counts
            curr_num_tokens += len(line_arr)

        elif line[0] == '%': # reply ids of replies that come after this id'
            temp = line[1:].split()
            for i in temp:
                transitions_count[(curr_id, int(i))] = 1

        elif line[0] == '#': #reply id
            curr_id = int(line[1:].split()[0])

        else: #continuation of input onto a new line
            line_arr = tokenize(line[1:])
            add_dict(curr_counts, line_arr)
            curr_num_tokens += len(line_arr)


    if len(curr_reply) != 0: #if we still have a reply in the buffer
        l.append((curr_reply, curr_counts, curr_num_tokens , curr_id))
    
    f.close()
    return l, transitions_count

            
#input:  counts - dictionary of token:count
#        total_count - total number of tokens in counts 
#        smoothing - smoothing constant: "steal from the rich and give to the needy"       
#output: dictionary of token:log_prob

def log_probs(counts, total_count, smoothing):
    result = {}
    #compute log-probabilities to avoid underflow
    for token, count in counts.iteritems():
        result[token] = math.log(count + smoothing) - math.log(total_count + smoothing*(len(counts) + 1))

    #generic token to be used when need prob for a token not seen before
    result['<UNK>'] = math.log(smoothing) - math.log(total_count + smoothing*(len(counts) + 1))
    return result

            


class Bot(object):

    #input: input_file - filepath as a string
    #       smoothing  - smoothing constant

    def __init__(self, input_file, smoothing):
        l, transitions_count = process(input_file)
        self.kb = {}
        self.previous_response_id = -1 #keep track of previous response made from bot

        #initialize knowledge base with input
        for reply, counts, num_tokens, response_id in l:
            self.kb[response_id] = ((reply, log_probs(counts, num_tokens, smoothing)))
        
        #initialize transition probabilities dictionary
        self.transition_prob = log_probs(transitions_count, len(transitions_count), 1e-15)



    #input:  response_old - previous response id
    #        response_new - potential curr reponse id
    #output: log probability of this transition occuring

    def get_prob_trans(self, response_old, response_new):
        if (response_old, response_new) in self.transition_prob:
            return self.transition_prob[(response_old, response_new)]
        else:
            return self.transition_prob['<UNK>']
        

    #input: input - user query
    #ouput: list with ordered responses from greatest to lowest probability, (reply, prob, id)

    def reply(self, input):
        input_arr = input.lower().split() #preprocess input
        result = []

        #compute probability of response given this input, and previous reponse_id for all replies in KB
        for response_id in self.kb:
            curr_reply, reply_probs = self.kb[response_id]
            total = float(0)

            for token in input_arr:
                if token in reply_probs:
                    total += reply_probs[token]
                else:
                    total += reply_probs['<UNK>'] #special word used when we've never seen this token before

            result.append((curr_reply, total + self.get_prob_trans(self.previous_response_id, response_id), response_id))
            

        #sort list from highest probability to lowest probability
        result.sort(key = lambda x: x[1], reverse = True)
        self.previous_response_id = result[0][2]
        return result


b = Bot("test.txt", 1e-4)
s = ''
while s != 'exit':
    s = raw_input("User: ")
    for x in b.reply(s):
    	print x
    print ""