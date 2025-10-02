# CNCF Workflow implementation

## Implementando un workplow con SonotaFlow

### Prerequisitos

Instalar:

* Podman
* Minikube
* Knative
* Knative workflow

# Crear el proyecto base

```bash
kn workflow create --name ecommerce --yaml-workflow
```

> 🛠️ Creating SonataFlow project
> Workflow file created at ./ecommerce/workflow.sw.json
> 🎉 SonataFlow project successfully created

```bash
kn workflow run
````


## Tutorial de implementación usando Python

Entra en la carpeta wf-python-imp se pordrá ver un tutotial de implementación en Python leer el tutorial y ejecutar el ejemplo:

```bash
cd wf-python-imp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 examples/mini_sonataflow_runner.py examples/sample-workflow.sw.yaml
```

Encontraras un `README.md` dentro de `wf-python-imp/` con más detalles.
