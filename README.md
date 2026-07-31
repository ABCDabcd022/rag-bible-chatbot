# 📖 RAG Bible Chatbot

Локальный RAG-чат-бот, который отвечает на вопросы по тексту Библии (или любой другой книге) полностью офлайн.

[![Docker Hub](https://img.shields.io/badge/Docker_Hub-actualcondor%2Frag--bible--chatbot-blue?logo=docker)](https://hub.docker.com/r/actualcondor/rag-bible-chatbot)

## 🧠 Как это работает

1. Текст книги разбивается на фрагменты (чанки) и превращается в векторы с помощью `nomic-embed-text`.
2. Векторы сохраняются в ChromaDB.
3. При вопросе система находит самые похожие по смыслу фрагменты.
4. Найденный контекст передаётся в `gemma3:4b`, которая генерирует ответ.

## 🛠️ Технологии

- **Ollama** — локальный запуск LLM
- **gemma3:4b** — модель для генерации ответов
- **nomic-embed-text** — модель для эмбеддингов
- **LangChain** — оркестрация RAG-пайплайна
- **ChromaDB** — векторная база данных
- **Docker** — контейнеризация

---

## 🐳 Запуск с Docker (рекомендуемый способ)

### 1. Клонируй репозиторий

```bash
git clone https://github.com/ABCDabcd022/rag-bible-chatbot.git
cd rag-bible-chatbot
```

### 2. Запусти контейнеры

```bash
docker-compose up -d
```

### 3. Запусти сервер Ollama внутри контейнера

```bash
docker exec -d ollama ollama serve
```

### 4. Скачай модели

```bash
docker exec -it ollama bash
ollama pull gemma3:4b
ollama pull nomic-embed-text
exit
```

### 5. Зайди в контейнер с приложением

```bash
docker exec -it rag-app bash
```

### 6. Проиндексируй книгу

```bash
python src/ingest.py
```

### 7. Запусти чат

```bash
python src/main.py
```

### 8. Остановка системы

Выйди из чата (`exit` или `Ctrl+C`), затем выполни:

```bash
docker-compose down
```

---

## 🖥️ Запуск без Docker (локально)

### 1. Установи Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Запусти сервер Ollama

```bash
ollama serve
```

### 3. Скачай модели

```bash
ollama pull gemma3:4b
ollama pull nomic-embed-text
```

### 4. Создай окружение и установи зависимости

```bash
conda create -n rag_env python=3.11 -y
conda activate rag_env
pip install -r requirements.txt
```

### 5. Индексация

Положи свою книгу (`.txt`) в папку `data/`:

```bash
python src/ingest.py
```

### 6. Запуск чата

```bash
python src/main.py
```

### 7. Остановка сервера

В терминале с `ollama serve` нажми `Ctrl+C`.

---

## 📚 Как заменить книгу

### С Docker

1. Положи новый файл `.txt` в папку `data/` на хосте
2. Удали старую векторную базу:
   ```bash
   rm -rf chroma_db/
   ```
3. Зайди в контейнер:
   ```bash
   docker exec -it rag-app bash
   ```
4. Переиндексируй:
   ```bash
   python src/ingest.py
   ```

### Без Docker

1. Положи новый файл `.txt` в папку `data/`
2. Удали старую базу:
   ```bash
   rm -rf chroma_db/
   ```
3. Запусти индексацию:
   ```bash
   python src/ingest.py
   ```

---

## 📝 Примеры вопросов

- `Who created the heavens and the earth?`
- `How many young men were in the fiery furnace?`
- `What did the ravens bring to Elijah?`
- `Who was the first king of Israel?`

---

## 📁 Структура проекта

```
rag-bible-chatbot/
├── src/
│   ├── ingest.py      # индексация текста
│   └── main.py        # основной чат
├── data/              # исходные тексты (в .gitignore)
├── chroma_db/         # векторная БД (в .gitignore)
├── requirements.txt   # Python-зависимости
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 📄 Лицензия

MIT