from backend.tools.retriever_tool import get_retriever_tool

def test_retriever_tool_runs():
    tool = get_retriever_tool()
    query = "What is an agent in LangChain?"
    result = tool.run(query)

    assert isinstance(result, str)
    assert len(result) > 0
    assert "LangChain" in result or "agent" in result.lower()
