import yaml
import argparse

from analyzers import chatgpt,spacy


argParser = argparse.ArgumentParser()

argParser.add_argument('-i', '--input', help='input text') 
args = argParser.parse_args()

input = args.input
synctaxAnalyzer = spacy.synctaxAnalyze(input)

svc_yaml = chatgpt.create_deployment_yaml(input)