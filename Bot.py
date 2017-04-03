import math
import os
from Scenario import Scenario
from Dialog import Dialog
from Response_Node import Response_Node


#input:  line - String
#output: list of token strings

def tokenize(line):
	result = line.lower().split()
	for i in xrange(len(result)): #remove punctuation marks
		if not result[i][-1].isalnum():
			result[i] = result[i][:-1]
	return result


#input:  questions  - list of strings
#output: counts     - dictionary of token:count
#        num_tokens - total number of tokens in questions list  

def process(questions):
	counts = {}
	num_tokens = 0
	for question in questions:
		for token in tokenize(question):
			num_tokens += 1
			if token not in counts:
				counts[token] = 0
			counts[token] += 1

	return counts, num_tokens

            
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



#input:  responses - set of Response_Node
#        temp_map  - dict of Response_Node:int
#output: dict of (start id, neighbor id) all mapped to 1

def get_transitions(responses, temp_map):
	transitions = {}
	for response in responses:
		curr_id = temp_map[response] #look up id for starting response in dict

        #for each neighbor from this start response, add (start id, neighbor id) to dict
		for neighbor in response.get_neighbors():
			transitions[(curr_id, temp_map[neighbor])] = 1

	return transitions


#input:  transition_prob - dict mapping (curr id, next id):log_prob
#        response_old    - previous response id
#        response_new    - potential curr reponse id
#output: log probability of this transition occuring

def get_prob_trans(transition_prob, response_old, response_new):
    if (response_old, response_new) in transition_prob:
        return transition_prob[(response_old, response_new)]
    else:
        return transition_prob['<UNK>']

            

class Bot:

    #input: scenario   - Scenario Object
    #       smoothing  - smoothing constant

    def __init__(self, scenario, smoothing):
        print 'initializing'
        self.kb = [] #kb of (response, log_probs dict, response_id) tuples

        dialog = scenario.get_dialog()
        temp_map = {}  # used to help create the transition probs
        count = 0      # used for giving ids to responses
        self.total_points = dialog.get_total_points()

        #initialize knowledge base with dialog from scenario
        for response in dialog.get_responses():
        	counts, num_tokens = process(response.get_questions())
        	self.kb.append((response.get_response(), log_probs(counts, num_tokens, smoothing), count, response.get_points()))
        	temp_map[response] = count #this map will be used to look up response objects to their ids
        	count += 1
        
        transitions = get_transitions(dialog.get_responses(), temp_map)
        #initialize transition probabilities dictionary
        self.transition_prob = log_probs(transitions, len(transitions), 1e-15)

        

    #input: query         - string representing string from user
    #       prev_response - id of response previously made from bot
    #ouput: list with ordered responses from greatest to lowest probability, (reply, prob, id)

    def reply(self, prev_response, query):
        input_arr = tokenize(query) #preprocess input
        result = []

        #compute probability of response given this query, and previous reponse_id for all replies in KB
        for curr_reply, reply_probs, response_id, points in self.kb:
            total = float(0)

            for token in input_arr:
                if token in reply_probs:
                    total += reply_probs[token]
                else:
                    total += reply_probs['<UNK>'] #special word used when we've never seen this token before

            result.append((curr_reply, total + get_prob_trans(self.transition_prob, prev_response, response_id), response_id, points))
            

        #sort list from highest probability to lowest probability
        result.sort(key = lambda x: x[1], reverse = True)
        return result


    #output: total possible points in this dialog int
    def get_total_points(self):
        return self.total_points