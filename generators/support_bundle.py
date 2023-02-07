import yaml
import argparse
import re
import json

from analyzers import chatgpt,spacy
from utils import tools


def create_collectors(support_yaml, input):

    kubectl_cmd = chatgpt.create_kubectl_cmd(input)
    metric_labels = ""
    print(kubectl_cmd)

    if re.search(r"kubectl.+logs", kubectl_cmd):
        svc_yaml = chatgpt.create_k8s_yaml(input, "service", "with port 80")
        log_collector = tools.create_log_selectors_from_svc_yaml(svc_yaml)
        support_yaml["metadata"]["name"] = "get-logs-from-pod-with-labels"
        support_yaml["spec"] = {
            "collectors": []
        }
        support_yaml["spec"]["collectors"].append(log_collector)

    if re.search(r"kubectl.+top.+node", kubectl_cmd):
        support_yaml["spec"] = {
            "hostCollectors": []
        }
        formated_cmd = "kubectl top node --metric-labels="
        metric_labels = chatgpt.create_kubectl_cmd_formated(input, formated_cmd)
        support_yaml["metadata"]["name"] = f"get-metrics-from-{metric_labels}"
        support_yaml["spec"]["hostCollectors"].append({
            f"{metric_labels}": {}
        })

    return support_yaml, metric_labels

def create_metrics_outcomes(support_yaml, input, metric_label, prefix="", suffix=""):
    outcomes = []
    outcomes_raw_json = chatgpt.create_json(input)

    outcomes_raw = json.loads(outcomes_raw_json)
    print(outcomes_raw)

    for key, values in outcomes_raw.items():
        for v in values:
            outcomes.append({
                f"{key}": {
                    "when": f"{v}",
                    "message": chatgpt.rewrite_text(f"{prefix}current {v} ,{suffix}").strip()
                }
            })

    support_yaml["spec"]["hostAnalyzers"] = [
        {
            f"{metric_label}": {
                "checkName": f"Amount of {metric_label}",
                "outcomes": outcomes
            }
        }
    ]

    return support_yaml