import yaml
import argparse
import re
import json

from analyzers import chatgpt,spacy
from utils import tools

def create_analyzers(support_yaml, input):
    synctaxAnalyzer = spacy.synctaxAnalyze(input)
    support_yaml, input_target = tools.init_sb_template(synctaxAnalyzer, input)

    kubectl_cmd = chatgpt.create_kubectl_cmd(input_target)

    print("========= openai generated kubectl cmd: =========")
    print(kubectl_cmd, "\n")
    

    if re.search(r"kubectl.+get.+pod", kubectl_cmd):
        pod_yaml = chatgpt.create_k8s_yaml(input_target, "pod")
        cluster_pod_statuses_analyzer = tools.create_cluster_pod_statuses_analyzer(pod_yaml)
        support_yaml["metadata"]["name"] = "pods-are-healthy"
        support_yaml["spec"] = {
            "analyzers": []
        }
        support_yaml["spec"]["analyzers"].append(cluster_pod_statuses_analyzer)

    return support_yaml

def create_outcomes(support_yaml, input, prefix="", suffix=""):
    outcomes = []
    outcomes_raw_json = chatgpt.create_json(input)

    outcomes_raw = json.loads(outcomes_raw_json)
    print("========= openai generated json: =========")
    print(outcomes_raw, "\n")

    for key, values in outcomes_raw.items():
        if re.search(r"_not", key):
            key = re.sub(r"_not.*", "", key)
            operator = "!= "
            operator_text = "not "
        else:
            operator = "== "
            operator_text = ""
        for v in values:
            outcomes.append({
                f"{key}": {
                    "when": f"{operator}{v}",
                    "message": f"{prefix}{operator_text}{v}{suffix}"
                }
            })

    support_yaml["spec"] = {
        "outcomes": outcomes
    }

    return support_yaml