import subprocess
import yaml
import json
import os
import sys
import shutil
import pandas as pd

rule_tester_path = "/home/pavan_pothams/projects/ruletest"
xdr_repo_path = "/home/pavan_pothams/projects/new/xdr-detection-ace-rules"
dirname = os.path.dirname(__file__)

# get file name
# file_name = sys.argv[1]
# csv_file_path = os.path.join(dirname, f"csv_files/{file_name}.csv")
# input_file = pd.read_csv(csv_file_path)
# rule_ids = input_file["id"].tolist()
# remaining_rule_ids = rule_ids[:]

rule_ids = [sys.argv[1]]
print(rule_ids)
remaining_rule_ids = rule_ids[:]

#Get the list of all files and directories
path = "/home/pavan_pothams/projects/TAP_Detection/rules/production"
dir_list = os.listdir(path)

rule_data = []

for i in dir_list:
        if '.json' in i:
                with open(f'{path}/{i}', 'r') as f:
                        # data = yaml.load(f, Loader=yaml.SafeLoader)
                        data = json.load(f,)
                        if data.get("id") in rule_ids:
                            remaining_rule_ids.remove(data.get("id"))
                            rule_data.append([data.get("id"),i])

def file_operations(r):
    create_dir_command = f"mkdir {xdr_repo_path}/rules/one_stage_rules/{r[0]}"
    create_file_command = f"touch {xdr_repo_path}/rules/one_stage_rules/{r[0]}/rule.yaml"
    test_folder = f"mkdir {xdr_repo_path}/rules/one_stage_rules/{r[0]}/positiveTests"
    test_file = f"touch {xdr_repo_path}/rules/one_stage_rules/{r[0]}/positiveTests/test.json"
    process = subprocess.Popen(create_dir_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen(create_file_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen(test_folder, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    process = subprocess.Popen(test_file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    shutil.copy(f'/home/pavan_pothams/projects/TAP_Detection/rules/tests/{r[0]}.json', test_file.replace("touch ",""))

    if os.path.isfile(f"/home/pavan_pothams/projects/TAP_Detection/rules/tests/negative/{r[0]}.json"):
        n_test_folder = f"mkdir {xdr_repo_path}/rules/one_stage_rules/{r[0]}/negativeTests"
        n_test_file = f"touch {xdr_repo_path}/rules/one_stage_rules/{r[0]}/negativeTests/test.json"
        process = subprocess.Popen(n_test_folder, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        process = subprocess.Popen(n_test_file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()        
        shutil.copy(f'/home/pavan_pothams/projects/TAP_Detection/rules/tests/negative/{r[0]}.json', n_test_file.replace("touch ",""))


for r in rule_data:

    file_operations(r)
    # Your long shell command
    rule_json_path = f"/home/pavan_pothams/projects/TAP_Detection/rules/production/{r[1]}"
    ace_path = f"{xdr_repo_path}/rules/one_stage_rules/{r[0]}/rule.yaml"
    command = f"python3 ./convert_rule.py -v -o translate -m /home/pavan_pothams/projects/new/xdr-detection-ace-rules/config/mitre_data.json -r {rule_json_path} --out-file {ace_path} --ruletester {rule_tester_path}"
    # Run the command with Popen
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()

    # Capture standard output and standard error (optional)
    output, error = process.communicate()

    # Check return code (optional)
    if process.returncode == 0:
        print("Command successful! Rule: ",r)
    else:
        print(f"Command failed with error code: {process.returncode}")
        # Print error output if needed
        print(f"Error: {error.decode()}")

# command_tags = f"python3 add_tags.py -v -r {xdr_repo_path}/rules/one_stage_rules -d {csv_file_path} --rule-tester /home/pavan_pothams/projects/ruletest --tag-ids tag_ids_new.json"
# # Run the command with Popen
# process_tags = subprocess.Popen(command_tags, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# process_tags.wait()

print(remaining_rule_ids)