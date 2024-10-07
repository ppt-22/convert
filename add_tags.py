#!/usr/bin/env python3
# ACE Rules tags and RA updater

import argparse
import os
import time
import yaml
import pandas as pd
import json
from subprocess import Popen
import math


def main(args):

    tag_id = load_json(args.tag_ids)
    input_file = pd.read_csv(args.input_data)
    input_json = input_file.to_dict(orient='records')
    count = 0
    # print(input_json)
    print(args.rules_directory)
    for root, main_dir, files in os.walk(args.rules_directory):
        print("heylo")
        for j in input_json:
            if j["id"] in root:
                if not root.endswith(j["id"]):
                    continue
                try:
                    print("Rule: ", j["id"])
                    ra = []
                    if not pd.isna(j["RA - investigate"]):
                        ra.extend(list(j["RA - investigate"].split(",")))
                    if not pd.isna(j["RA - contain"]):
                        ra.extend(list(j["RA - contain"].split(",")))
                    if not pd.isna(j["RA - remediate"]):
                        ra.extend(list(j["RA - remediate"].split(",")))
                    if len(ra)>1:
                        ra = [s.strip(' ') for s in ra]
                    tags_orig = list(j["Tags"].split(","))
                    for file in files:
                        if file.endswith(".yaml"):
                            filepath = os.path.join(root, file)
                            rule_file = load_yaml(filepath)
                            rule_file["version"] = int(time.time())
                            rule_file["metadata"]["recommended_action"] = list(ra)
                            tags_fin = []
                            for i in tags_orig:
                                i = i.lower().strip(" ")
                                if i in tag_id.keys():
                                    tags_fin.append(tag_id[i])
                                else:
                                    print("Error: Key Not found", i)
                                    exit()
                            rule_file["metadata"]["tags"] = tags_fin
                            count = count + 1
                            write_data(rule_file, filepath)
                            p = Popen([args.rule_tester, "--format",
                                       "RBC", "--rules", filepath, "--write-rules", filepath])
                            p.wait()
                except AttributeError as e:
                    print("e: ", e)
                    exit()
    print("Processed Rule Files: ", count)


def load_yaml(yaml_file):
    # Load file
    if os.path.exists(yaml_file):
        with open(yaml_file, "rb") as fin:
            out = yaml.safe_load(fin,)
            return out


def load_json(file):
    if os.path.exists(file):
        with open(file, "rb") as fin:
            data_file = json.load(fin)
            return data_file


def write_data(intel_data, out_file):
    '''write_data: Writes data file'''
    with open(out_file, "w") as fout:
        yaml.dump(intel_data, fout)
        print("Data written (%s)" % out_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ACE Rule Tags & RA")
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=True, help="Verbose output"
    )
    parser.add_argument(
        "-r", "--rules-directory", action="store", help="Rule Directory to process"
    )
    parser.add_argument(
        "-d", "--input-data", action="store", help="CSV file with RA and tags associated to the rule"
    )
    parser.add_argument(
        "--rule-tester", action="store", help="Rule Tester File"
    )
    parser.add_argument(
        "--tag-ids", action="store", help="Tag Ids"
    )
    args = parser.parse_args()
    main(args)
