import os
import openai
import json
import re

# want to write a function that just takes out the sterotypes and just has a json file where the source and target
# is the key and it points to dict of all examples indexed by natural numbers


# for whatever reason this does not work. Maybe lets just scrape out all of the examples and then loop over that
# we dont need the sterotype
def Bias_Remover():
    # want to store all of these de-biased examples in an identical format with the examples changed
    with open('Sterotype_Examples.json','r') as file1:
        for line in file1:  # each line in the file is a dictonary {Target-> Source: {1:S1, 2:S2, ...,.n:Sn}}
            obj = json.loads(line)
            pair = obj.keys() # keys returns a set
            for x in pair: # get the pair from the set and set it equal to source_to_target
                source_to_target = x

            de_biased_examples = {source_to_target:[]}
        
            examples = obj[source_to_target] # get the dict of sterotypes
            
            for utterance in examples:
                clean_utterance = Remove_Bias(source_to_target,utterance)
                de_biased_examples[source_to_target].append(clean_utterance)
            
            with open('Debiased_Sterotype_Examples.json', 'a') as file2:
                json.dump(de_biased_examples,file2)
                file2.write('\n') 
