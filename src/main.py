from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Конфигурация
CHROMA_DIR = "chroma_db"
MODEL_NAME = "gemma3:4b"  # Модель для генерации ответов

def format_docs(docs):
    """Форматирует найденные документы в один текст для контекста"""
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain():
    """Создаёт RAG-цепочку: поиск + генерация"""
    
    # 1. Загружаем векторную базу с эмбеддингами
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    print("✅ Векторная база загружена")
    
    # 2. Настраиваем LLM для генерации
    llm = ChatOllama(model=MODEL_NAME)
    print(f"✅ Модель {MODEL_NAME} загружена")
    
    # 3. Создаём промпт
    template = """Ты — ассистент, который отвечает на вопросы, используя только предоставленный контекст.
Если ответа нет в контексте — скажи, что не знаешь, и не выдумывай.

Контекст:
{context}

Вопрос: {question}

Ответ:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # 4. Собираем RAG-цепочку
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

def main():
    print("🚀 Запуск RAG-системы...")
    print("📖 Вопросы по Библии. Для выхода введите 'exit' или 'quit'")
    print("-" * 50)
    
    try:
        chain = create_rag_chain()
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return
    
    while True:
        question = input("\n❓ Ваш вопрос: ").strip()
        
        if question.lower() in ['exit', 'quit', 'выход']:
            print("👋 До свидания!")
            break
        
        if not question:
            continue
        
        try:
            print("🔄 Думаю...")
            answer = chain.invoke(question)
            print(f"\n✅ Ответ:\n{answer}")
            print("-" * 50)
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
