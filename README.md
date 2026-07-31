# 📖 RAG-система по Библии

Локальная RAG-система, которая отвечает на вопросы по тексту Библии (King James Version).  
Использует **Ollama** (gemma3:4b + nomic-embed-text), **LangChain** и **ChromaDB**.

## 🚀 Как запустить

### 1. Установка зависимостей

```bash
conda create -n rag_env python=3.11 -y
conda activate rag_env
pip install -r requirements.txt
