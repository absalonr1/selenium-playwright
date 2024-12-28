# Base image con Python
FROM mcr.microsoft.com/playwright/python:v1.49.1-noble

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar Playwright
RUN pip install --no-cache-dir playwright

# Instalar navegadores de Playwright (incluyendo Firefox y WebKit)
#RUN playwright install firefox webkit

# Copiar los archivos de la aplicación al contenedor
COPY ./*.py .

# Comando predeterminado para ejecutar un script
CMD ["python", "script.py"]
