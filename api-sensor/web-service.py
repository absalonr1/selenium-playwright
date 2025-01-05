from fastapi import FastAPI, HTTPException
import subprocess

app = FastAPI()

@app.get("/execute/{cpu}/{script_name}")
def execute_command(cpu: str, script_name: str):
    try:
        # Define comandos según el script_name usando un switch-like estructura
        command = [
            "docker", "run",  "--env-file", ".env", "--cpus", cpu, "--rm", 
            "playwright-python", "python", script_name
        ]

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
