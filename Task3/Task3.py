"""
Task 3 compare specs names from suppliers:
once you have json files for optosigma and thorlabs products, you need to unify and homogenize the specs names in order to integrate them in a single database, ie, thorlabs display "Focal Length" while optosigma names it as "Focal length f", but these specs represent the same.
- pick a set of specs (5 to 10) which you think are the most relevant for lenses
- make a script to try to identify these specs in optosigma and thorlabs products (regex can be helpful for making patterns and removing/replacing text)
- generate new json files using the homogenized spec names you have chosen before.

Please submit the code you use to do the tasks and the json output as a github repository.

+ Not too many things to do here as the outputs of task1.py and task2.py are in the same format
+ Just a simple list concatenation will suffice, then we write the combined output to a json file
"""


file_thorlabs = "./Task2/task2.json"
file_optosigma = "./Task1/task1.json"
file_combined_output = "./Task3/task3.json"

import json
import sys

#fetch the outputs of the other two scripts
try:
   with open(file_thorlabs, 'r', encoding='utf-8') as f:
      data_thorlabs = json.load(f)

   with open(file_optosigma, 'r', encoding='utf-8') as f:
      data_optosigma = json.load(f)
except:
   #If error -> probably a folder access issue or files missing, just terminate for now
    #Can take alternative actions in a future version by checking the cause of the error
    print('Cannot fetch the files, do you have access to the output folder?')
    sys.exit()


print('Length of Thorlabs lenses: ' + str(len(data_thorlabs)))
print('Length of OptoSigma lenses: ' + str(len(data_optosigma)))

#concatenate the lists
combined_lenses = data_thorlabs+data_optosigma
print('Length of combined lenses: ' + str(len(data_optosigma+data_thorlabs)))

print(combined_lenses[10])

try:
    #Try to save the combined component list in json format
    with open(file_combined_output, "w") as outfile:
        json.dump(combined_lenses, outfile, ensure_ascii=False)
except:
    #If error -> probably a folder access issue, just terminate for now
    #Can take alternative actions in a future version by checking the cause of the error
    print('Cannot save the file, do you have access to the destination folder?')
    sys.exit()