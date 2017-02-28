import math
import os


#input:  dictionary d, list of strings l
#updates dictionary with frequency of strings in l
def add_dict(d, l):
    for token in l:
        if token in d:
            d[token] += 1
        else:
            d[token] = 1

def tokenize(line):
	result = line.lower().split()
	for i in xrange(len(result)):
		if not result[i][-1].isalnum():
			result[i] = result[i][:-1]
	return result


#input: file to learn from
def process(input_file):
    l = []
    f = open(input_file, 'r')

    curr_reply = ''        
    curr_counts = {}       #token counts
    curr_num_inputs = 0    #number of inputs corresponding to current reply
    curr_num_tokens = 0    #number of tokens in all inputs to current reply
    total_inputs = 0       #total number of inputs in the file
    
    for line in f:
        if line[0] == '\n': #marks end of this reply: get ready for next reply in file
            l.append((curr_reply, curr_num_inputs, curr_counts, curr_num_tokens))
            curr_reply = ''
            curr_counts = {}
            curr_num_inputs = 0
            curr_num_tokens = 0


        elif line[0] == '+': #new reply
            curr_reply = line[1:-1] #extract string part from line

        elif line[0] == '-': #input line
            line_arr = tokenize(line[1:]) #preprocess line
            add_dict(curr_counts, line_arr) #update token counts
            curr_num_inputs += 1
            curr_num_tokens += len(line_arr)
            total_inputs += 1

        else: #continuation of input onto a new line
            line_arr = tokenize(line[1:])
            add_dict(curr_counts, line_arr)
            curr_num_tokens += len(line_arr)


    if len(curr_reply) != 0: #if we still have a reply in the buffer
        l.append((curr_reply, curr_num_inputs, curr_counts, curr_num_tokens))
    
    f.close()
    return l, total_inputs

            
#input: dictionary counts, total number of tokens total_count, smoothing constant        
def log_probs(counts, total_count, smoothing):
    result = {}
    #compute log-probabilities to avoid underflow
    for token, count in counts.iteritems():
        result[token] = math.log(count + smoothing) - math.log(total_count + smoothing*(len(counts) + 1))
    result['<UNK>'] = math.log(smoothing) - math.log(total_count + smoothing*(len(counts) + 1))
    return result

            


class Bot(object):

    #input: input filepath as a string, smoothing constant
    def __init__(self, input_file, smoothing):
        print 'initializing'
        l, total_inputs = process(input_file)
        self.kb = []
        #initialize knowledge base with input
        for reply, num_inputs, counts, num_tokens in l:
            self.kb.append((reply, log_probs(counts, num_tokens, smoothing), math.log(num_inputs) - math.log(total_inputs)))
        
        

    #input: string
    #ouput: list ordered from best to worst response probabilistically
    def reply(self, input):
        input_arr = input.lower().split() #preprocess to all lowercase and split on whitespace
        result = []
        divisor = float(0)

        #compute probability of response given this input for all replies in KB
        for curr_reply, reply_probs, prob in self.kb:
            total = float(0)

            for token in input_arr:
                if token in reply_probs:
                    total += reply_probs[token]
                else:
                    total += reply_probs['<UNK>'] #special word used when we've never seen this token before
            total += prob
            total = math.exp(total)
            divisor += total
            result.append((curr_reply, total))

        for i in xrange(len(result)):
        	result[i] = (result[i][0], result[i][1]/divisor)



        #sort list from highest probability to lowest probability
        result.sort(key = lambda x: x[1], reverse = True)
        print result
        return result


'''b = Bot("test.txt", 1e-2)
s = ''
while s != 'exit':
    s = raw_input("User: ")
    for x in b.reply(s):
    	print x
    print ""'''