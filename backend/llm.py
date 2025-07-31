from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(
        model="gpt-3.5-turbo-0125",
        temperature=0,
    )
