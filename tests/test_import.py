import darkgpt

def test_import():
    assert hasattr(darkgpt, 'DarkGPT')
    assert hasattr(darkgpt, 'ConversationalShell')

if __name__ == '__main__':
    print('DarkGPT:', darkgpt.DarkGPT)
    print('ConversationalShell:', darkgpt.ConversationalShell)
    print('Leak_Function:', getattr(darkgpt, 'Leak_Function', None))
