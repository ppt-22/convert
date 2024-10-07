#!/usr/bin/env python3
# ACE rule formatter

import os
import time
import yaml
import json
import argparse
from subprocess import Popen


SEVERITY_ID = {
    "unknown": 0,
    "informational": 1,
    "low": 2,
    "medium": 3,
    "high": 4,
    "critical": 5
    }

CLASSIFICATION = {
    "Command and Control": 100,
    "Beaconing": 90,
    "Spearphish": 80,
    "Webshell": 70,
    "Denial of Service": 65,
    "Attempted Exploit": 60,
    "Reconnaissance": 50,
    "Methodology": 40,
    "Suspicious": 30
}

KILL_CHAIN = {
    "Recon": 1,
    "Weaponization": 2,
    "Delivery": 3,
    "Exploitation": 4,
    "Installation": 5,
    "C2": 6,
    "Act": 7,
    "n/a": "n/a"
}

THREAT_TYPE = {
    "APT": 100,
    "Evil": 50,
    "Commodity": 25,
    "Methodology": 5
}

DEFAULT_MITRE = "/home/pavan_pothams/projects/xdr-detection-ace-rules/config/mitre_data.json"
DEFAULT_TAGS = "/home/pavan_pothams/projects/xdr-detection-ace-rules/config/tag_ids.json"


def main(args):

    method = args.option
    if args.out_file:
        output = args.out_file
    else:
        output = args.rule_file

    # Translate Helix Json rule and format it.
    if method == "translate":
        rule_json = load_json(args.rule_file)
        write_cache(rule_json, "temp_data.json")
        print("Translating rule")
        p = Popen([f"{args.ruletester}", "--format", "helix"
                      , "--rules", "temp_data.json", "--write-rules", args.out_file])

        p.wait()

    if args.test_events:
        print("Testing")
        Popen([args.ruletester, "--rules", output, "--events", args.test_events])


def load_yaml(cache_file):
    '''load_cache: Load cache'''
    # Load file
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as fin:
            out = yaml.safe_load(fin,)
            return out


def load_json(file):

    if os.path.exists(file):
        with open(file, "rb") as fin:
            data_file = json.load(fin)
            return data_file


def write_data(data, out_file):
    '''write_data: Writes data file'''
    with open(out_file, "w") as fout:
        yaml.dump(data, fout)
        print("Data written (%s)" % out_file)


def write_cache(alert_cache, cache_file):
    '''write_cache: Writes cache file'''
    with open(cache_file, "w") as fout:
        json.dump(alert_cache, fout)
        print("Cache file written (%s)" % cache_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ACE rules Formatter")
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="Verbose output"
    )
    parser.add_argument('-o', '--option', choices=["translate"], required=True, help="Choose method Translate: Helix rule to ACE, Format: format YAML ACE rule")
    parser.add_argument('-r', '--rule-file', required=True, help="Rule to format")
    parser.add_argument('-e', '--test-events', help="test event file")
    parser.add_argument('-m', '--mitre-data', default=DEFAULT_MITRE, help="mitre data file")
    parser.add_argument('-t', '--tags-data', default=DEFAULT_TAGS, help="tags data file")
    parser.add_argument('--out-file', action="store", help="Output file path")
    parser.add_argument('--ruletester', required=True)
    args = parser.parse_args()
    main(args)

