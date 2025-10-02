# Tutorial: Enseñando SonataFlow paso a paso

Este tutorial enseña SonataFlow mediante un ejemplo práctico y un runner mínimo que simula la ejecución de un flujo. Está pensado para fines didácticos: entender conceptos, cómo se definen flujos y cómo pasar datos entre tareas.

## Objetivo
- Mostrar cómo diseñar un flujo simple (saludo -> transformación -> notificación).
- Implementar un *mini-runner* en Python que interprete un YAML de flujo y ejecute tareas.
- Explicar cada paso y cómo extender el flujo.

## Contrato del ejemplo
- Input: un objeto JSON con `name` (string).
- Output: impresión en consola del saludo final.
- Comportamiento: las tareas deben ejecutarse en orden; los datos de salida de una tarea estarán disponibles para la siguiente.

## Casos borde a considerar
- Input vacío (sin `name`)
- Valores nulos
- Fallos en una tarea (la ejecución debe detenerse y mostrar error)

## Estructura del proyecto (relevante)
- `docs/sonataflow-tutorial.md` (este documento)
- `examples/sample-workflow.yaml` (definición del flujo)
- `examples/mini_sonataflow_runner.py` (runner que interpreta el YAML)
- `examples/tasks.py` (implementación de tareas usadas en el ejemplo)
- `requirements.txt` (dependencias para el ejemplo)

## Definición del flujo (explicación)
El flujo de ejemplo tiene estas etapas:
1. start: punto de entrada
2. greet: crea un saludo usando `name` de entrada
3. transform: transforma el saludo a mayúsculas
4. log: escribe el resultado final en consola
5. end: fin

Cada tarea puede devolver un `result` que se guarda en el contexto con la clave `{taskId}.result`.

## YAML de ejemplo
Consulta `examples/sample-workflow.sw.yaml` para la definición exacta.

## Mini-runner: cómo funciona
El runner lee el YAML y ejecuta nodos secuencialmente según la clave `next`. Soporta tipos de nodo:
- `start`, `end` (marcadores)
- `function` (llama a una función de `examples/tasks.py`)
- `http` (simulado si `simulate: true`)
- `log` (imprime en consola)

Los parámetros usan formato `${path}` para referirse a valores en el contexto. Por ejemplo `${input.name}` lee del input.

## Cómo ejecutar el ejemplo (rápido)
En macOS (zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 examples/mini_sonataflow_runner.py examples/sample-workflow.sw.yaml
```

El runner imprimirá el progreso y el resultado final.

## Extensiones sugeridas
- Añadir paralelismo y `join` de resultados
- Soporte a condiciones (branching)
- Persistencia del estado del flujo
- Integración con un motor real de SonataFlow si lo tienes disponible

---

### Notas finales
Asumo que SonataFlow usa un formato YAML similar al mostrado; este tutorial produce una implementación didáctica (mini-runner) en Python para experimentar localmente sin depender de un motor externo.
