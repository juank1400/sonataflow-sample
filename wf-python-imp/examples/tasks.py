import time

def greet(name: str) -> dict:
    """Devuelve un saludo como diccionario con clave 'result'"""
    if name is None or name == "":
        raise ValueError("name is required")
    time.sleep(0.2)
    return {"result": f"Hola, {name}!"}


def uppercase(message: str) -> dict:
    """Transforma el mensaje a mayúsculas y devuelve {'result': ...} """
    if message is None:
        raise ValueError("message is required")
    time.sleep(0.1)
    return {"result": message.upper()}
