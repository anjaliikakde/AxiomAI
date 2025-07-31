from dotenv import load_dotenv
from backend.pipeline import setup_research_assistant

def main():
    """Main entry point for the research assistant application."""
    load_dotenv()
    assistant = setup_research_assistant()
    
    print("Research Assistant is ready. Type 'exit' to quit.")
    while True:
        query = input("\nEnter your research question: ")
        if query.lower() == 'exit':
            break
        response = assistant.invoke({"input": query})
        print(f"\nAnswer: {response['output']}")

if __name__ == "__main__":
    main()