
from langchain_community.llms import Ollama

llm = Ollama(base_url="http://144.6.107.170:19999", model="transkatgirl/Yi-1.5-34B:q8_0")

def send_to_llama(prompt):
    return llm.invoke(prompt)
