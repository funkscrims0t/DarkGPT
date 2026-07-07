from openai import Client
import os
from .dehashed_api import consultar_dominio_dehashed
import json
from .functions import Leak_Function
from dotenv import load_dotenv
load_dotenv()

AgentPrompt = """
DarkGPT agent prompt (trimmed for package).
"""
RouterPrompt = "Eres un asistente de ciberseguridad que se encarga de clasificar metadatos en funciones para OSINT"

class DarkGPT:
    def __init__(self):
        self.model_name = "gpt-4-1106-preview"
        self.temperature = 0.7
        self.functions = Leak_Function
        try:
            self.openai_client = Client(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception:
            self.openai_client = None

    def execute_function_call(self, function_prompts: list, message):
        def mensajes(mensaje):
            lista_mensajes = [{"role": "system", "content": RouterPrompt},
                              {"role": "user", "content": mensaje}]
            return lista_mensajes

        functions_prompts = mensajes(message)
        if not self.openai_client:
            return "OpenAI client not configured"

        response = self.openai_client.chat.completions.create(model="gpt-4",
                                                              temperature=0,
                                                              messages=functions_prompts,
                                                              functions=self.functions)
        try:
            preprocessed_output = json.loads(response.choices[0].message.function_call.arguments)
            processed_output = consultar_dominio_dehashed(preprocessed_output)
        except Exception:
            processed_output = "No encontrado"
        return str(processed_output)

    def process_history_with_function_output(self, messages: list, function_output: dict):
        history_json = []
        history_json.append({"role": "system", "content": AgentPrompt + json.dumps(function_output)})
        for message in messages:
            if "USUARIO" in message:
                history_json.append({"role": "user", "content": message["USUARIO"]})
            elif "ASISTENTE" in message:
                history_json.append({"role": "assistant", "content": message["ASISTENTE"]})
        return history_json

    def GPT_with_function_output(self, historial: dict, callback=None):
        function_output = self.execute_function_call(Leak_Function, historial[-1].get("USUARIO", ""))
        historial_json = self.process_history_with_function_output(historial, function_output)
        if not self.openai_client:
            print(function_output)
            return
        respuesta = self.openai_client.chat.completions.create(model=self.model_name,
                                                               temperature=self.temperature,
                                                               messages=historial_json,
                                                               stream=True)
        for chunk in respuesta:
            try:
                print(chunk.choices[0].delta.content or "\n", end="")
            except Exception:
                pass
