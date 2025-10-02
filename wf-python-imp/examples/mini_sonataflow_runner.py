#!/usr/bin/env python3
"""Mini SonataFlow runner didáctico.

Ejecuta un workflow YAML simple con nodos secuenciales.
"""
import sys
import os
import yaml
import re
from importlib import import_module
from typing import Any, Dict

CONTEXT_KEY_PATTERN = re.compile(r"\$\{([^}]+)\}")


def resolve_param(expr: Any, context: Dict[str, Any]):
    """Resuelve parámetros que pueden contener ${...} expresiones."""
    if isinstance(expr, str):
        def repl(m):
            path = m.group(1)
            parts = path.split('.')
            cur = context
            for p in parts:
                if p in cur:
                    cur = cur[p]
                else:
                    raise KeyError(f"No se encontró la ruta '{{path}}' en el contexto")
            return str(cur)
        return CONTEXT_KEY_PATTERN.sub(lambda m: repl(m), expr)
    elif isinstance(expr, dict):
        return {k: resolve_param(v, context) for k, v in expr.items()}
    elif isinstance(expr, list):
        return [resolve_param(v, context) for v in expr]
    else:
        return expr


def normalize_workflow(wf: Dict[str, Any]) -> Dict[str, Any]:
    """Normaliza un workflow que use `states` (formato .sw.yaml) al formato que
    entiende el runner (clave `nodes` con `id`, `type`, `next`, etc.).
    Si el workflow ya contiene `nodes`, se devuelve sin cambios.
    """
    if 'nodes' in wf:
        return wf
    if 'states' not in wf:
        return wf

    nodes = []
    for st in wf.get('states', []):
        nid = st.get('name')
        stype = st.get('type')
        node: Dict[str, Any] = {'id': nid}
        # Mapear tipos comunes
        if stype == 'event':
            if st.get('end'):
                node['type'] = 'end'
            else:
                node['type'] = 'start'
            # transition puede existir
            if 'transition' in st:
                node['next'] = st.get('transition')
        elif stype == 'operation':
            # Tomar la primera acción y mapear functionRef -> function
            actions = st.get('actions', [])
            if actions:
                act = actions[0]
                if 'functionRef' in act:
                    fr = act['functionRef']
                    node['type'] = 'function'
                    node['func'] = fr.get('refName')
                    node['params'] = fr.get('arguments', {})
                else:
                    # Otros tipos de acción no soportados explícitamente
                    node['type'] = 'function'
                    node['func'] = None
            else:
                node['type'] = 'function'
                node['func'] = None
            if 'transition' in st:
                node['next'] = st.get('transition')
        elif stype == 'inject':
            # inject -> log
            node['type'] = 'log'
            data = st.get('data', {})
            # Si data contiene 'message' la usamos; si no, lo convertimos a str
            node['message'] = data.get('message') if isinstance(data, dict) else str(data)
            if 'transition' in st:
                node['next'] = st.get('transition')
        else:
            # Fallback a tipo no soportado
            node['type'] = 'noop'
            if 'transition' in st:
                node['next'] = st.get('transition')

        nodes.append(node)

    new_wf = dict(wf)
    new_wf['nodes'] = nodes
    # Mantener start si existe en el top-level
    if 'start' not in new_wf and nodes:
        new_wf['start'] = nodes[0]['id']
    return new_wf


class MiniRunner:
    def __init__(self, wf: Dict[str, Any]):
        # Normalizar workflows que vengan en formato 'states' (.sw.yaml)
        self.wf = normalize_workflow(wf)
        self.nodes = {n['id']: n for n in self.wf.get('nodes', [])}
        self.context: Dict[str, Any] = {'input': self.wf.get('input', {})}

    def run(self):
        current = self.wf.get('start')
        steps = 0
        while current:
            steps += 1
            if steps > 1000:
                raise RuntimeError('Posible loop infinito')
            node = self.nodes.get(current)
            if node is None:
                raise KeyError(f"Nodo '{current}' no encontrado en el workflow")
            ntype = node.get('type')
            print(f"Ejecutando nodo: {current} (type={ntype})")
            if ntype == 'start':
                current = node.get('next')
                continue
            if ntype == 'end':
                print("Flujo finalizado correctamente.")
                break
            if ntype == 'function':
                func_name = node['func']
                params = resolve_param(node.get('params', {}), self.context)
                result = self.call_function(func_name, params)
                self.context[f"{node['id']}"] = result
                print(f" -> resultado: {result}")
                current = node.get('next')
                continue
            if ntype == 'http':
                # Para este tutorial, soportamos simulación (no llamar a la red)
                params = resolve_param(node.get('params', {}), self.context)
                if node.get('simulate', True):
                    print(f"Simulando HTTP {node.get('method','GET')} {node.get('url')} con body {params}")
                    self.context[f"{node['id']}"] = {'result': 'http_simulated'}
                else:
                    import requests
                    method = node.get('method','GET').upper()
                    url = resolve_param(node.get('url'), self.context)
                    body = params
                    resp = requests.request(method, url, json=body)
                    self.context[f"{node['id']}"] = {'result': resp.text}
                current = node.get('next')
                continue
            if ntype == 'log':
                message = resolve_param(node.get('message',''), self.context)
                print(message)
                self.context[f"{node['id']}"] = {'result': message}
                current = node.get('next')
                continue
            raise NotImplementedError(f"Tipo de nodo no soportado: {ntype}")

    def call_function(self, func_name: str, params: Dict[str, Any]):
        # Asegurarnos de que el root del proyecto esté en sys.path para poder
        # importar el paquete `examples` incluso si se ejecuta desde otra ruta.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, '..'))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        # Intentamos cargar la función desde examples.tasks
        tasks = import_module('examples.tasks')
        if not hasattr(tasks, func_name):
            raise AttributeError(f"Función '{func_name}' no encontrada en examples.tasks")
        func = getattr(tasks, func_name)
        # Llamamos con parámetros por nombre si es dict
        if isinstance(params, dict):
            return func(**params)
        else:
            return func(params)


def main():
    if len(sys.argv) < 2:
        print('Uso: mini_sonataflow_runner.py <workflow.yaml>')
        sys.exit(2)
    path = sys.argv[1]
    with open(path, 'r') as f:
        wf = yaml.safe_load(f)
    runner = MiniRunner(wf)
    try:
        runner.run()
    except Exception as e:
        print('Error durante la ejecución:', e)
        sys.exit(1)

if __name__ == '__main__':
    main()
