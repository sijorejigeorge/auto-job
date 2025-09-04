
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv

load_dotenv()
base_url = os.getenv("LLM_BASE_URL")
model = os.getenv("LLM_MODEL")
llm = Ollama(base_url=base_url, model=model)

def send_to_llama(prompt):
    return llm.invoke(prompt)
