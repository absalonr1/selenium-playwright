## Con Docker

```
# local
docker build -t playwright-python .
docker run -it --rm playwright-python /bin/bash
docker run -it --env-file .env --rm playwright-python /bin/bash

#interactivo
docker run -it --cpus 1 --rm playwright-python /bin/bash

# ejecucion desde host

docker run -it --env-file .env --cpus 1 --rm playwright-python python login-crm-pw.py
docker run -it --env-file .env --cpus 1 --rm playwright-python python login-empleadores-bm-pw.py
docker run -it --env-file .env --cpus 1 --rm playwright-python python login-empleadores-vt-pw.py
docker run -it --env-file .env --cpus 1 --rm playwright-python python login-helpseguros-pw.py
docker run -it --env-file .env --cpus 1 --rm playwright-python python login-vidatres-pw-iframe.py

docker pull mcr.microsoft.com/playwright/python:v1.49.1-noble
docker run -it --rm --ipc=host mcr.microsoft.com/playwright/python:v1.49.1-noble /bin/bash


# uso de CPU del contenedor

docker stats

```

## Directo con Playwright

```
python -m venv pw
source pw/in/activate
pip install playwright
playwright install
pip install pyinstaller

#generar ejecutable
pyinstaller --onefile login-vsp.py
deactivate
```
