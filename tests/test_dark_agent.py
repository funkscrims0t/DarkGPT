from types import SimpleNamespace

from darkgpt.DarkAgent import DarkGPT


class FakeResponses:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return next(self.responses)


def test_no_api_key_returns_a_clear_message(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    agent = DarkGPT()

    assert "not configured" in agent.execute_function_call("hello")


def test_responses_function_call_round_trip(monkeypatch):
    first_response = SimpleNamespace(
        output=[
            SimpleNamespace(
                type="function_call",
                name="dehashed_search",
                arguments='{"mail":"user@example.com","nickname":null}',
                call_id="call_123",
            )
        ],
        output_text="",
    )
    final_response = SimpleNamespace(output=[], output_text="Lookup summary")
    fake_responses = FakeResponses([first_response, final_response])
    agent = DarkGPT()
    agent.openai_client = SimpleNamespace(responses=fake_responses)
    monkeypatch.setattr(
        "darkgpt.DarkAgent.consultar_dominio_dehashed",
        lambda arguments: {"email": arguments["mail"]},
    )
    chunks = []

    result = agent.GPT_with_function_output(
        [{"USUARIO": "look up user@example.com"}], callback=chunks.append
    )

    assert result == "Lookup summary"
    assert chunks == ["Lookup summary"]
    assert fake_responses.calls[0]["model"] == agent.model_name
    assert fake_responses.calls[0]["tools"][0]["name"] == "dehashed_search"
    tool_output = fake_responses.calls[1]["input"][-1]
    assert tool_output == {
        "type": "function_call_output",
        "call_id": "call_123",
        "output": '{"email": "user@example.com"}',
    }
