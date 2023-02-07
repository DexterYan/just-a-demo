import spacy

def synctaxAnalyze(text):
  nlp = spacy.load("en_core_web_sm")

  doc = nlp(text)

  return {
    "noun_phrases": [chunk.text for chunk in doc.noun_chunks],
    "verbs": [token.lemma_ for token in doc if token.pos_ == "VERB"]
  }