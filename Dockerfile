FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# 1) Copia requirements primero (mejor caché)
COPY requirements.txt .

# 2) Instala deps y valida imports en un one-liner
RUN python -m pip install --no-cache-dir -r requirements.txt \
 && python -c "import flask_sqlalchemy, flask, sqlalchemy; print('Flask-SQLAlchemy OK')"

# 3) Copia el resto del código
COPY . .

EXPOSE 8080
ENV PORT=8080
CMD ["gunicorn","-w","2","-k","gthread","-b","0.0.0.0:8080","index:app"]

