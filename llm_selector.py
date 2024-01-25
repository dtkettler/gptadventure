import configparser
from abc import ABC, abstractmethod

from gpt import GPT
from llamacpp import Llamacpp


class LLM(ABC):

    @abstractmethod
    def run_llm(self, system_prompt, user_prompt, temperature=0.5, json=False):
        pass

    @abstractmethod
    def run_llm_with_history(self, system_prompt, user_prompt, history, temperature=0.5, json=False):
        pass

def get_llm():
    config = configparser.ConfigParser()
    config.read('config.ini')
    type = config['DEFAULT']['model_type']

    if type == "llamacpp":
        model = config['DEFAULT']['model']
        n_gpu_layers = config.getint('DEFAULT', 'n_gpu_layers')
        n_batch = config.getint('DEFAULT', 'n_batch')
        template_format = config['DEFAULT']['template_format']

        return Llamacpp(model, n_gpu_layers, n_batch, template_format)
    elif type == "openai":
        return GPT()