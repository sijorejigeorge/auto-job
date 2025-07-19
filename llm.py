from langchain_community.llms import Ollama

llm = Ollama(base_url="http://host.docker.internal:11434", model="gemma3")

def send_to_llama(prompt):
    return llm.invoke(prompt)
