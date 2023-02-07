import openai
import os
from decouple import config


openai.api_key = config("OPENAI_API_KEY")

def summarize(text):
  
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Human: Try to summarize the following text\n\n{text}\nAI:",
    temperature=0.5,
    max_tokens=250,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=[" Human:", " AI:"]
  )

  return response.choices[0].text

def get_labels(text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Human: what label in following text\n\n{text}\nAI:",
    temperature=0.2,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=[" Human:", " AI:"]
  )

  return response.choices[0].text
  
def get_namespace(text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Human: abstract namespace in following text\n\n{text}\nAI:",
    temperature=0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=[" Human:", " AI:"]
  )

  return response.choices[0].text

def create_k8s_yaml(text, type, additional_text=""):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Convert this text to a k8s {type} yaml {additional_text}:\n\n{text}",
    temperature=0,
    max_tokens=500,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.0
  )
  # print(response.choices[0].text)
  return response.choices[0].text

def create_kubectl_cmd(text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Convert this text to a kubectl command:\n\n{text}",
    temperature=0,
    max_tokens=250,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.0
  )

  return response.choices[0].text

def create_kubectl_cmd_formated(text, format):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Convert this text to a kubectl command:\n\n{text}\n\n{format}",
    temperature=0,
    max_tokens=250,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0.0
  )

  # print(response.choices[0].text)
  return response.choices[0].text

def create_json(text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Convert this text to json:\n\n{text}",
    temperature=0,
    max_tokens=500,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0.0
  )

  # print(response.choices[0].text)
  return response.choices[0].text

def rewrite_text(text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Rewrite this text:\n\n{text}",
    temperature=0,
    max_tokens=500,
    top_p=1,
    frequency_penalty=0.2,
    presence_penalty=0.0
  )

  # print(response.choices[0].text)
  return response.choices[0].text