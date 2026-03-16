# Используем официальный образ Python 3.10
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Отключаем буферизацию и генерацию .pyc-файлов
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Устанавливаем системные зависимости для компиляции psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Собираем статику (если нужно)
RUN python store/manage.py collectstatic --noinput

# Открываем порт 8000
EXPOSE 8000

# Запускаем сервер
CMD ["python", "store/manage.py", "runserver", "0.0.0.0:8000"]
