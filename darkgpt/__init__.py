"""Lightweight package wrapper exposing the project's main symbols.

This module dynamically loads the top-level .py modules in the repository so you
can `import darkgpt` without moving or duplicating the original source files.
"""
"""Public package API for darkgpt."""
try:
    from .DarkAgent import DarkGPT
except Exception:
    DarkGPT = None
try:
    from .cli import ConversationalShell
except Exception:
    ConversationalShell = None
try:
    from .dehashed_api import consultar_dominio_dehashed
except Exception:
    consultar_dominio_dehashed = None
try:
    from .functions import Leak_Function
except Exception:
    Leak_Function = None

__all__ = [
    'DarkGPT', 'ConversationalShell', 'consultar_dominio_dehashed', 'Leak_Function',
]
