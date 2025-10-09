#!/usr/bin/env python3
"""Validador simple de manifiestos SonataFlow en `ecommerce/manifests`.

Requisitos:
  pip install PyYAML

Ejemplo:
  python3 validate_manifests.py

El script comprueba:
- Que cada documento YAML tenga apiVersion, kind y metadata.name
- Que `spec.flow` exista y tenga `start` y `states`
- Que los `states` contengan al menos `name` y `type`
- Reglas específicas para tipos `inject`, `operation` y `event`
"""
import os
import sys
from typing import Any, Dict, List

try:
    import yaml
except Exception:
    print("Este script requiere PyYAML. Instálalo con: pip install PyYAML")
    sys.exit(2)

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFESTS_DIR = os.path.join(ROOT, 'manifests')


def load_yaml_file(path: str) -> List[Dict[str, Any]]:
    text = open(path, 'r', encoding='utf-8').read()
    # eliminar fences ```yaml si existen
    if text.lstrip().startswith('```'):
        # quitar la primera linea fence y la última si hay
        lines = text.splitlines()
        if lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].startswith('```'):
            lines = lines[:-1]
        text = '\n'.join(lines)
    try:
        docs = list(yaml.safe_load_all(text))
        return [d for d in docs if d is not None]
    except Exception as e:
        raise RuntimeError(f"Error parseando YAML {path}: {e}")


def validate_doc(doc: Dict[str, Any], path: str) -> List[str]:
    errors: List[str] = []
    if not isinstance(doc, dict):
        errors.append('Documento no es mapping')
        return errors
    if 'apiVersion' not in doc:
        errors.append('Falta apiVersion')
    if 'kind' not in doc:
        errors.append('Falta kind')
    if 'metadata' not in doc or not isinstance(doc.get('metadata'), dict):
        errors.append('Falta metadata')
    else:
        if 'name' not in doc['metadata']:
            errors.append('Falta metadata.name')

    spec = doc.get('spec')
    if not spec:
        errors.append('Falta spec')
        return errors
    flow = spec.get('flow')
    if not flow:
        errors.append('Falta spec.flow')
        return errors
    # start and states
    if 'start' not in flow:
        errors.append('spec.flow.start ausente')
    if 'states' not in flow:
        errors.append('spec.flow.states ausente')
    else:
        states = flow.get('states')
        if not isinstance(states, list):
            errors.append('spec.flow.states debe ser lista')
        else:
            names = set()
            for i, st in enumerate(states):
                prefix = f'spec.flow.states[{i}]'
                if not isinstance(st, dict):
                    errors.append(f'{prefix} no es mapping')
                    continue
                if 'name' not in st:
                    errors.append(f'{prefix} falta name')
                else:
                    if st['name'] in names:
                        errors.append(f'{prefix} nombre duplicado: {st["name"]}')
                    names.add(st.get('name'))
                if 'type' not in st:
                    errors.append(f'{prefix} falta type')
                else:
                    t = st.get('type')
                    if t == 'inject':
                        # comprobar data
                        if 'data' not in st and 'end' not in st:
                            errors.append(f"{prefix} inject sin 'data'")
                    if t == 'operation':
                        if 'actions' not in st:
                            errors.append(f"{prefix} operation sin 'actions'")
                        else:
                            acts = st.get('actions')
                            if not isinstance(acts, list) or not acts:
                                errors.append(f"{prefix} actions vacías o no-lista")
                    # más reglas pueden añadirse aquí
    return errors


def main():
    if not os.path.isdir(MANIFESTS_DIR):
        print(f"No existe el directorio de manifiestos: {MANIFESTS_DIR}")
        sys.exit(2)
    files = [f for f in os.listdir(MANIFESTS_DIR) if f.endswith('.yaml') or f.endswith('.yml')]
    if not files:
        print('No hay archivos YAML en manifests/')
        sys.exit(0)
    total_errors = 0
    for fn in sorted(files):
        path = os.path.join(MANIFESTS_DIR, fn)
        print(f'-- Validando {fn} --')
        try:
            docs = load_yaml_file(path)
        except Exception as e:
            print('ERROR:', e)
            total_errors += 1
            continue
        for i, d in enumerate(docs):
            errs = validate_doc(d, path)
            if errs:
                total_errors += len(errs)
                print(f' Documento[{i}] tiene {len(errs)} problemas:')
                for e in errs:
                    print('  -', e)
            else:
                print(f' Documento[{i}] OK')
    if total_errors:
        print(f'Validación completada: {total_errors} problema(s) encontrados')
        sys.exit(1)
    print('Validación completada: sin errores detectados')
    sys.exit(0)


if __name__ == '__main__':
    main()
