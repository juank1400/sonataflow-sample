# SonataFlow — Tutorial y ejemplo

Este repositorio contiene un tutorial didáctico para aprender los conceptos básicos de SonataFlow mediante un ejemplo ejecutable.

Archivos importantes:

- `docs/sonataflow-tutorial.md` — guía paso a paso y explicación.
- `examples/sample-workflow.sw.yaml` — definición del flujo de ejemplo.
- `examples/mini_sonataflow_runner.py` — runner didáctico que interpreta el YAML y ejecuta las tareas.
- `examples/tasks.py` — tareas del ejemplo (greet, uppercase).

Cómo ejecutar (macOS / zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 examples/mini_sonataflow_runner.py examples/sample-workflow.sw.yaml
```

Lee `docs/sonataflow-tutorial.md` para más detalles.
# sonataflow-sample