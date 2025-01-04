## EC2 Setup

```
sudo apt-get update
sudo apt install -y qemu-system
sudo apt-get -y install podman
#which qemu-system-x86_64
#sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
podman machine init

sudo apt install python3.12-venv -y
```

## VENV setup
```
pip install fastapi uvicorn
```

## Local test
```
uvicorn web-service:app --reload --workers 4 --host 0.0.0.0 --port 8000
curl http://ec2-a-b-c-d.compute-1.amazonaws.com:8000/execute/login-vidatres-pw-iframe.py
```

## systemd

Service file "/etc/systemd/system/uvicorn.service"

```
[Unit]
Description=FastAPI Service with Uvicorn
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/pw/ws
ExecStart=/bin/bash -c "source /home/ubuntu/pw/ws/api-sensor/bin/activate && uvicorn web-service:app --reload --workers 4 --host 0.0.0.0 --port 8000"
Restart=always
# Cuando usas PYTHONUNBUFFERED=1, cada mensaje se imprime inmediatamente despues de ser generado, sin esperar a que se llene el bufer
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Commands:
```
sudo systemctl daemon-reload
sudo systemctl enable uvicorn.service
sudo systemctl start uvicorn.service
sudo systemctl status uvicorn.service
```

## Instalar un servidor gráfico virtual
Instala y configura un servidor gráfico como Xvfb (X virtual framebuffer), que permitirá ejecutar aplicaciones gráficas sin necesidad de un monitor físico ni una conexión activa.

```
sudo apt update
sudo apt install xvfb -y
# ejemplo ficticio
xvfb-run -a python3 script.py
```
