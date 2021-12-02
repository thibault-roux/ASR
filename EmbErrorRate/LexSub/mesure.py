from transformers import FlaubertTokenizer, FlaubertModel
import torch
from scipy import spatial

"""
Il faut faire attention, la valeur de similarité est très élevé
(exemple: 0.80 pour dog et cat) pour certains mots qui ne devraient pas
"""

tokenizer = FlaubertTokenizer.from_pretrained('flaubert/flaubert_base_cased')
model = FlaubertModel.from_pretrained('flaubert/flaubert_base_cased')

inputs = tokenizer("Bonjour, mon chien est mignon", return_tensors="pt")
outputs = model(**inputs)

inputs2 = tokenizer("Bonjour, mon chat est mignon", return_tensors="pt")
outputs2 = model(**inputs2)

last_hidden_states = outputs.last_hidden_state
last_hidden_states2 = outputs2.last_hidden_state

def similarite(v1, v2):
    return 1 - spatial.distance.cosine(v1, v2)



for i in range(8):
    print(similarite(last_hidden_states.detach().numpy()[0][i], last_hidden_states2.detach().numpy()[0][i]))
