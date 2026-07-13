import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from .dehashed_api import consultar_dominio_dehashed
from .functions import Leak_Function

load_dotenv()

AgentPrompt = """
You are DarkGPT, a cybersecurity assistant. Use any supplied lookup results only
to answer the user's question. Do not claim a lookup succeeded when it did not.
""".strip()

RouterPrompt = (
    "You are a cybersecurity assistant. Use the dehashed_search tool only when "
    "the user asks for an authorized OSINT-style lookup."
)


class DarkGPT:
    """CLI-facing wrapper around the OpenAI Responses API."""

    def __init__(self):
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-5.6")
        self.functions = Leak_Function
        api_key = os.getenv("OPENAI_API_KEY")
        try:
            self.openai_client = OpenAI(api_key=api_key) if api_key else None
        except Exception:
            self.openai_client = None

    def execute_function_call(self, message: str) -> str:
        """Run the model/tool loop and return the final response text.

        Responses function calls are returned as output items. Each local tool
        result must be submitted with its call ID before the model can continue.
        """
        if not self.openai_client:
            return "OpenAI client not configured. Set OPENAI_API_KEY and try again."

        response = self.openai_client.responses.create(
            model=self.model_name,
            instructions=f"{RouterPrompt}\n\n{AgentPrompt}",
            input=message,
            tools=self.functions,
        )

        # A bounded loop supports a follow-up tool request without allowing an
        # accidental infinite cycle from a faulty model response.
        for _ in range(3):
            function_calls = [
                item for item in response.output if getattr(item, "type", None) == "function_call"
            ]
            if not function_calls:
                return response.output_text or "No response returned."

            tool_outputs = []
            for call in function_calls:
                if call.name != "dehashed_search":
                    result = {"error": f"Unsupported tool: {call.name}"}
                else:
                    try:
                        result = consultar_dominio_dehashed(json.loads(call.arguments))
                    except (TypeError, json.JSONDecodeError, ValueError) as error:
                        result = {"error": f"Invalid tool arguments: {error}"}
                    except Exception as error:
                        result = {"error": f"Lookup failed: {error}"}
                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": json.dumps(result),
                    }
                )

            response = self.openai_client.responses.create(
                model=self.model_name,
                instructions=AgentPrompt,
                input=[*response.output, *tool_outputs],
                tools=self.functions,
            )

        return "The lookup could not be completed after multiple tool requests."

    def GPT_with_function_output(self, historial: list, callback=None) -> str:
        message = historial[-1].get("USUARIO", "") if historial else ""
        response_text = self.execute_function_call(message)
        if callback:
            callback(response_text)
        else:
            print(response_text)
        return response_text
