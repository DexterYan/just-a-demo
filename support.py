import os
import openai
import re
import yaml
import spacy

def chatGPTSummarize(text):
  openai.api_key = os.getenv("OPENAI_API_KEY")

  response = openai.Completion.create(
    model="text-davinci-003",
    # prompt="Human: Try to summarize the following text\n\nwrite a support bundle to retrive logs from pod with app=api selector\nAI:",
    prompt="Human: Try to summarize the following text\n\nretrive logs from pod with app=api selector, then write a support bundle to analyzer it\nAI:",
    temperature=0.5,
    max_tokens=250,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=[" Human:", " AI:"]
  )

  return response.choices[0].text

support_yaml = {
  "apiVersion": "troubleshoot.sh/v1beta2",
  "kind": "",
  "metadata":
    {"name": "my-application-name"},
  "spec":
    {"collectors": []},
}

log_collector = {
  "logs": {
    "selector": [],
    "namespace": "default",
  },
}

def synctaxAnalyze(text):
  nlp = spacy.load("en_core_web_sm")

  doc = nlp(text)
  for entity in doc.ents:
      print(entity.text, entity.label_)

  return {
    "noun_phrases": [chunk.text for chunk in doc.noun_chunks],
    "verbs": [token.lemma_ for token in doc if token.pos_ == "VERB"]
  }

def supportBundleGenerator(entities):
  for e in entities["noun_phrases"]:
    if re.search(r"support.+bundle", e):
      support_yaml["kind"] = "SupportBundle"
    if re.search(r"log(s|)", e):
      log_collector["logs"]["selector"] = []
    if re.search(r".*=.* selector", e):
      selectorAbstract = re.search(r'(?:an|the) (\w*=\w*) selector', e)
      selector = selectorAbstract.group(1)
  
  log_collector["logs"]["selector"] = [selector]
  support_yaml["spec"]["collectors"].append(log_collector)
  print(yaml.dump(support_yaml))

text = chatGPTSummarize("write a support-bundle yaml to get logs from pod has api=app selector")
# text = "This text describes how to create a support bundle to collect logs from a pod with an app=api selector."
text = re.sub('[!,*)@#%(&$_?.^`\']','', text)
print(text)

entities = synctaxAnalyze(text)

supportBundleGenerator(entities)
