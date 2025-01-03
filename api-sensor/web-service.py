
from fastapi import FastAPI, HTTPException
import subprocess

app = FastAPI()

@app.get("/execute/{script_name}")
def execute_command(script_name: str):
    try:
        # Define comandos según el script_name usando un switch-like estructura
        command = []
        if script_name == "login-crm-pw.py":
            command = [
                "podman", "run",  "--env-file", ".env", "--cpus", "0.5", "--rm", 
                "playwright-python", "python", "login-crm-pw.py"
            ]
        elif script_name == "login-empleadores-bm-pw.py":
            command = [
                "podman", "run",  "--env-file", ".env", "--cpus", "0.5", "--rm", 
                "playwright-python", "python", "login-empleadores-bm-pw.py"
            ]
        elif script_name == "login-empleadores-vt-pw.py":
            command = [
                "podman", "run",  "--env-file", ".env", "--cpus", "0.5", "--rm", 
                "playwright-python", "python", "login-empleadores-vt-pw.py"
            ]
        elif script_name == "login-helpseguros-pw.py":
            command = [
                "podman", "run",  "--env-file", ".env", "--cpus", "0.5", "--rm", 
                "playwright-python", "python", "login-helpseguros-pw.py"
            ]
        elif script_name == "login-vidatres-pw-iframe.py":
            command = [
                "podman", "run",  "--env-file", ".env", "--cpus", "0.5", "--rm", 
                "playwright-python", "python", "login-vidatres-pw-iframe.py"
            ]
        else:
            raise HTTPException(status_code=400, detail="Invalid script name specified")

        # Ejecuta el comando y captura la salida
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout.strip()

        # Verifica si la salida comienza con "0:"
        if output.startswith("0:"):
            return {"status": "success", "output": output}
        else:
            raise HTTPException(status_code=400, detail="Invalid output: does not start with '0:'")

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=f"Command failed: {e.stderr.strip()}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
