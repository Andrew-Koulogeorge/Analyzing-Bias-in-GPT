from GPT import GPT_Source_To_Target_Sterotypes # why does this run GPT_Responses ?????????
from GPT import GPT_Implict_Expressions
import json
import re

# Read in prompts from the prompts.txt file
# Send those prompts to the GPT_Responses function to generate output
# Write those responses line by line in the Data_Generation/responses.txt 
    
complete_demographic_bank = [
    'Whites',
    'Blacks',
    'Asians',
    'Hispanics',
    'Indians',
    'Arabics',
    'Christians',
    'Jews',
    'Muslims',
    'Males',
    'Females',
    "Queers",
    'Old People',
    'Young People',
    "Americans",
    'Fench People',
    'Middle Eastern People'
]
# function to create all the sterotypes from the source to ratget 
def build_sterotypes(bank): # didnt finish all indians, jews
    for x in bank:
        for y in bank:
            if x != y:
                output = GPT_Source_To_Target_Sterotypes(x,y)
                with open('Source_To_Target.json', 'a') as file:
                    json.dump(output, file)
                    file.write('\n')

# code to go over the StoT jason files and pull out the lists of sterotypes for each pair 
def Sterotype_Extractor():
    with open('Source_To_Target.json') as f1:
        for line in f1: # go over objects in the json file
            obj = json.loads(line)
            pair = obj.keys() # keys returns a set
            for x in pair: # get the pair from the set and set it equal to source_to_target
                source_to_target = x
            sterotypes = obj[source_to_target]

        # Matches any digit followed by any characters until the first period is found
            pattern = re.compile(r'(?<=\n).*?(?=\n)')
            all_matches = re.findall(pattern, sterotypes)
            filerted_matched = [x for x in all_matches if x!= ''] # now have an array of all the sterotypes for the pair
            for i in range(len(filerted_matched)):
                filerted_matched[i] = re.sub('\d+\.','',filerted_matched[i])

            types = {source_to_target: {}}
            for i,example in enumerate(filerted_matched):
                i+=1
                types[source_to_target][i] = example

            # now that I have the filtered sterotypes, i want to write them to another json file
            with open("Sterotypes.json",'a') as f2:
                json.dump(types,f2)
                f2.write('\n')
    
def example_creator():
    with open('s2.json','r') as file1:
        for line in file1:  # each line in the file is a dictonary {Target-> Source: {1:S1, 2:S2, ...,.n:Sn}}
            obj = json.loads(line)
            pair = obj.keys() # keys returns a set
            for x in pair: # get the pair from the set and set it equal to source_to_target
                source_to_target = x
        
            sterotypes = obj[source_to_target] # get the dict of sterotypes
            examples_json_container = {source_to_target: {}} # container that will hold the examples for each sterotype
            for i in range(1,len(sterotypes)+1): # looping over each sterotype
                index = str(i)
                sterotype = sterotypes[index]
                example = GPT_Implict_Expressions(source_to_target,sterotype)
                examples_json_container[source_to_target][sterotype] = example
            
            with open('Examples.json', 'a') as file2:
                json.dump(examples_json_container,file2)
                file2.write('\n')

example_creator()


