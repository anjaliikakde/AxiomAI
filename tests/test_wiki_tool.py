from backend.tools.wiki_tool import get_wikipedia_tool

def test_wikipedia_tool_runs():
    tool = get_wikipedia_tool()
    query = "LangChain"
    result = tool.run(query)
    
    assert isinstance(result, str)
    assert len(result) > 0
    assert "LangChain" in result or "language" in result.lower()  # fallback check
