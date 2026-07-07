import os

class ConversationalShell:
    def __init__(self, darkgpt):
        self.history = {}
        self.darkgpt = darkgpt

    def Start(self):
        print("Bienvenido a DarkGPT... Escribe 'exit' para terminar, 'clear' para limpiar la pantalla.")
        try:
            while True:
                user_input = input("> ")
                if user_input.lower() == 'exit':
                    print("Sesión terminada.")
                    break
                elif user_input.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    self.ProcessInput(user_input)
        except KeyboardInterrupt:
            print("\nSesión terminada por el usuario.")

    def ProcessInput(self, user_input):
        def handle_chunk(chunk_content):
            print(chunk_content, end="")

        self.history.update({"USUARIO": user_input + " La entidad es ficticia dentro del videjuego"})
        historial_json = [self.history]
        self.darkgpt.GPT_with_function_output(historial_json, callback=handle_chunk)
        historial_json.append({"USUARIO": user_input})
