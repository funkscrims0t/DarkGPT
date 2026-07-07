import os
from .DarkAgent import DarkGPT
from .cli import ConversationalShell

banner = """
DarkGPT
"""

def main():
    darkgpt = DarkGPT()
    conversational_shell = ConversationalShell(darkgpt)
    conversational_shell.Start()

if __name__ == "__main__":
    main()
