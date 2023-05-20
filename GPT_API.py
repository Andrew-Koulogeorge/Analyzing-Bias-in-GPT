from GPT import GPT_Source_To_Target_Sterotypes # why does this run GPT_Responses ?????????
from GPT import GPT_Implict_Expressions
from GPT import Remove_Bias
import random
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

combination_demographic_bank = [
    'White Men',
    'Asian Women',
    'Black Women',
    'White Women',
    'Queer Men',
    'Asian Man',
    'Old Jews',
]


def sort_by_target(bank):
    with open('./Sterotypes/Sterotypes_By_List.json') as f1:
        for line in f1: # go over objects in the json file
            obj = json.loads(line)
            pair = obj.keys() # keys returns a set
            for x in pair: # get the pair from the set and set it equal to source_to_target
                source_to_target = x
            ### source to target is a string from the source group to the target group. We want to get out what the target it
            for x in bank:
                if f"->{x}" in source_to_target: target = x
            # now that I have the filtered sterotypes, i want to write them to another json file
            with open(f"./Sterotypes/Sterotypes_By_Target/Sterotypes_Against{target}.json",'a') as f2:
                json.dump(obj,f2)
                f2.write('\n')
            


# function to create all the sterotypes from the source to ratget 
def build_sterotypes(bank): # didnt finish all indians, jews
    for x in bank:
        for y in bank:
            if x != y:
                output = GPT_Source_To_Target_Sterotypes(x,y)
                with open('Combination_Source_To_Target.json', 'a') as file:
                    json.dump(output, file)
                    file.write('\n')

# code to go over the StoT jason files and pull out the lists of sterotypes for each pair 
def Sterotype_Extractor():
    with open('Combination_Source_To_Target.json') as f1:
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
            with open("Combination_Sterotypes.json",'a') as f2:
                json.dump(types,f2)
                f2.write('\n')
    
def example_creator():
    with open('combo_sterotype.json','r') as file1:
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
            
            with open('Combination_Examples.json', 'a') as file2:
                json.dump(examples_json_container,file2)
                file2.write('\n')

def Example_Extractor():
    with open('Combination_Examples.json') as f1:
        for line in f1: # go over objects in the json file
            obj = json.loads(line)
            pair = obj.keys() # keys returns a set
            for x in pair: # get the pair from the set and set it equal to source_to_target
                source_to_target = x
            
            # this is the dict which contains sterotypes as a key and examples as a value
            examples_per_sterotype = obj[source_to_target]

            # want to create a new dict for each sterotype. Sterotype will be the key and a dictonary examples will be the values

           # Matches any digit followed by any characters until the first period is found
            sterotypes = examples_per_sterotype.keys()
            for sterotype in sterotypes:
                examples = examples_per_sterotype[sterotype] # get the long string of all examples

                # want to break up the examples 
                pattern = re.compile(r'(?<=\n).*?(?=\n)') # subject to change
                all_matches = re.findall(pattern, examples)
                filerted_examples = [x for x in all_matches if x!= ''] # now have an array of all the examples for the pair and sterotype
                for i in range(len(filerted_examples)):
                    filerted_examples[i] = re.sub('\d+\.','',filerted_examples[i])

                examples = {}
                for i,example in enumerate(filerted_examples):
                    i+=1
                    examples[i] = example
                examples_per_sterotype[sterotype] = examples
            
            line = {source_to_target:examples_per_sterotype}

            # now that I have the filtered sterotypes, i want to write them to another json file
            with open("Clean_Combination_Examples.json",'a') as f2:
                json.dump(line,f2)
                f2.write('\n')


# for whatever reason this does not work. Maybe lets just scrape out all of the examples and then loop over that
# we dont need the sterotype
def Example_Extractor():
    # want to store all of these de-biased examples in an identical format with the examples changed
    with open('Sterotype_data/Sterotypes.json','r') as file1:
        for line in file1:  # each line in the file is a dictonary {Target-> Source: {1:S1, 2:S2, ...,.n:Sn}}
            obj = json.loads(line)
            pair = obj.keys() # keys returns a set
            for x in pair: # get the pair from the set and set it equal to source_to_target
                source_to_target = x

            new = {source_to_target:[]}
        
            sterotypes_to_examples= obj[source_to_target] # get the dict of sterotypes
            indexs = sterotypes_to_examples.keys() # get a set of all the sterotypes
            
            for index in indexs:
                sterotype = sterotypes_to_examples[index] # get the dictonary of examples
                new[source_to_target].append(sterotype)

                #for i in range(1,len(utterances)+1):
                    #index = str(i)
                    #utterance = utterances[index]
                    #new[source_to_target].append(utterance)
            
            print(sterotypes_to_examples)
            with open('Sterotypes_By_List.json', 'a') as file2:
                json.dump(new,file2)
                file2.write('\n') 

# for whatever reason this does not work. Maybe lets just scrape out all of the examples and then loop over that
# we dont need the sterotype
def Bias_Remover():
    # want to store all of these de-biased examples in an identical format with the examples changed
    with open('left_to_run_combination.json','r') as file1:
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
            
            with open('Debiased_Combination_Sterotype_Examples.json', 'a') as file2:
                json.dump(de_biased_examples,file2)
                file2.write('\n') 

def sample():
    with open('Examples_By_Sterotypes.json','r') as file1:
        for line in file1:  # each line in the file is a dictonary {Target-> Source: {1:S1, 2:S2, ...,.n:Sn}}
            sample = {}
            obj = json.loads(line)
            pair = obj.keys() # keys returns a set
            for x in pair: # get the pair from the set and set it equal to source_to_target
                source_to_target = x
            sterotypes = list(obj[source_to_target].keys())
            random_sterotype = random.choice(sterotypes)

            ### want to check that the examples is not empty
            while obj[source_to_target][random_sterotype] == {}:
                random_sterotype = random.choice(sterotypes)
            
            sample[source_to_target] = {random_sterotype:obj[source_to_target][random_sterotype]}
            
            with open('Sample-Examples_By_Sterotypes.json', 'a') as file2:
                json.dump(sample,file2)
                file2.write('\n') 
if __name__ == "__main__":
    sort_by_target(complete_demographic_bank)