import yaml
import argparse
import re

from analyzers import chatgpt,spacy
from utils import tools
from generators import support_bundle, preflight

# input = "write a support-bundle yaml to get logs from pod has api=app, app.kubernetes.io/name=service1 and kurl.io/app=hi labels in app namespace"

argParser = argparse.ArgumentParser()

argParser.add_argument('-i', '--input', help='input text') 
args = argParser.parse_args()

input = args.input
stages_input = tools.split_to_stages(input)
# print(stages_input)

if len(stages_input) < 1:
    raise Exception("Please input right syntax")

synctaxAnalyzer = [spacy.synctaxAnalyze(i) for i in stages_input]

support_yaml, input_target = tools.init_sb_template(synctaxAnalyzer[0], stages_input[0])
if support_yaml["kind"] == "SupportBundle":
    support_yaml, metric_label = support_bundle.create_collectors(support_yaml, input_target)
if support_yaml["kind"] == "Preflight":
    support_yaml = preflight.create_analyzers(support_yaml, input_target)

if len(stages_input) == 2:
    if support_yaml["kind"] == "Preflight":
        if support_yaml["metadata"]["name"] == "pods-are-healthy":
            support_yaml = preflight.create_outcomes(support_yaml, stages_input[1], "Pod {{ .Namespace }}/{{ .Name }} is in a ", " state.")

    if support_yaml["kind"] == "SupportBundle":
        if re.search(r"get-metrics-from-cpu", support_yaml["metadata"]["name"]):
            support_yaml = support_bundle.create_metrics_outcomes(support_yaml, stages_input[1], metric_label, "At least 2 CPU cores are required, ", " 4 CPU cores are recommended.")
        if re.search(r"get-metrics-from-memory", support_yaml["metadata"]["name"]):
            support_yaml = support_bundle.create_metrics_outcomes(support_yaml, stages_input[1], metric_label, "At least 4G of memory are required, ", " 8G of memory are recommended.")

print("\n\n========= support bundle yaml: =========\n")
print(yaml.dump(support_yaml))