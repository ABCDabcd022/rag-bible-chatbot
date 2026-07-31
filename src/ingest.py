import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Конфигурация
DATA_DIR = "data"
CHROMA_DIR = "chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def load_documents():
    """Загружает все текстовые файлы из папки data"""
    documents = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(('.txt', '.md')):
            filepath = os.path.join(DATA_DIR, filename)
            loader = TextLoader(filepath, encoding='utf-8')
            documents.extend(loader.load())
            print(f"✅ Загружен файл: {filename}")
    return documents

def split_documents(documents):
    """Разбивает документы на чанки"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Создано {len(chunks)} фрагментов (чанков)")
    return chunks

def create_vector_store(chunks):
    """Создаёт векторную базу данных и сохраняет её"""
    # ИСПРАВЛЕНО: используем nomic-embed-text вместо gemma3:4b
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    print(f"✅ Векторная база сохранена в {CHROMA_DIR}")
    return vector_store

def main():
    print("🚀 Начинаем индексацию документов...")
    
    # Проверяем, есть ли файлы в папке data
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        print("❌ Папка data пуста или не существует!")
        print("📁 Положите свой роман (в формате .txt) в папку data/")
        return
    
    # Загружаем документы
    documents = load_documents()
    if not documents:
        print("❌ Не найдено текстовых файлов в папке data/")
        return
    
    # Разбиваем на чанки
    chunks = split_documents(documents)
    
    # Создаём векторную базу
    vector_store = create_vector_store(chunks)
    
    print("🎉 Индексация завершена успешно!")

if __name__ == "__main__":
    main()