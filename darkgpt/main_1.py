from darkgpt.DarkAgent import DarkGPT
from darkgpt.cli import ConversationalShell


def main():
    darkgpt = DarkGPT()
    conversational_shell = ConversationalShell(darkgpt)
    conversational_shell.Start()