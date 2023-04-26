import openai
import os
from decouple import config

openai.api_key = config("OPENAI_API_KEY")

def chat_gpt(message, temperature=1.0, max_tokens=None, top_p=1.0, stop=None, presence_penalty=0.0, frequency_penalty=0.0):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stop=stop,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty
    )
    return response.choices[0].message['content']

def summarize(text):
    return chat_gpt(f"Try to summarize the following text: {text}", temperature=0.5, max_tokens=250, stop=[" Human:", " AI:"])

def get_labels(text):
    return chat_gpt(f"what label in following text: {text}", temperature=0.2, max_tokens=100, stop=[" Human:", " AI:"])

def get_namespace(text):
    return chat_gpt(f"abstract namespace in following text: {text}", temperature=0, max_tokens=100, stop=[" Human:", " AI:"])

def create_k8s_yaml(text, type, additional_text=""):
    return chat_gpt(f"Convert this text to a k8s {type} yaml {additional_text}: {text}", temperature=0, max_tokens=500, frequency_penalty=0.5)

def create_kubectl_cmd(text):
    return chat_gpt(f"Convert this text to a kubectl command: {text}", temperature=0, max_tokens=250, frequency_penalty=0.5)

def create_kubectl_cmd_formated(text, format):
    return chat_gpt(f"Convert this text to a kubectl command: {text}\n\n{format}", temperature=0, max_tokens=250, frequency_penalty=0.2)

def create_json(text):
    return chat_gpt(f"Convert this text to json: {text}", temperature=0, max_tokens=500, frequency_penalty=0.2)

def rewrite_text(text):
    return chat_gpt(f"Rewrite this text: {text}", temperature=0, max_tokens=500, frequency_penalty=0.2)
