FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY src/ ./src/
COPY data/ ./data/
COPY chroma_db/ ./chroma_db/

# Создаём папки, если их нет
RUN mkdir -p data chroma_db

# Команда по умолчанию (запуск чата)
CMD ["python", "src/main.py"]
