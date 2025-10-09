Validación de manifiestos SonataFlow (ecommerce)

Requisitos locales:
- Python 3
- PyYAML (pip install PyYAML)
- kubectl configurado para tu cluster
- kn (Knative CLI) si vas a aplicar los workflows con kn

Comprobaciones locales rápidas:

1. Ejecutar el validador de manifiestos:

```bash
python3 validate_manifests.py
```

2. Validar sintaxis YAML (opcional):

```bash
yq eval --prettyPrint . manifests/*.yaml
```

Despliegue de prueba en cluster (Knative + SonataFlow operator):

1. Aplicar manifiesto:

```bash
kubectl apply -f manifests/01-sonataflow_hello.yaml
```

2. Ver estados:

```bash
kubectl get sonataflows -n <namespace>
kubectl describe sonataflow hello -n <namespace>
```

3. Revisar logs del operator y del workflow para depuración.

Notas:
- Asegúrate de que el cluster tenga el SonataFlow Operator instalado si vas a crear recursos `SonataFlow`.
- Si usas `kn workflow gen-manifest`, verifica el contenido generado y adáptalo a tu profile/namespace.
