# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Рабочая директория
WORKDIR /app

# Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код (без .env благодаря .dockerignore)
COPY . .

# Собираем статику
RUN python store/manage.py collectstatic --noinput

# Порт
EXPOSE 8000

# Запуск через Gunicorn (не runserver!)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "store.wsgi:application"]
