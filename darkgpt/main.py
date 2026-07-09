import os

from darkgpt.DarkAgent import DarkGPT
from darkgpt.cli import ConversationalShell
from darkgpt.main_1 import main

banner = """
DarkGPT
"""

def main():
    darkgpt = DarkGPT()
    conversational_shell = ConversationalShell(darkgpt)
    conversational_shell.Start()

if __name__ == "__main__":
    main()
