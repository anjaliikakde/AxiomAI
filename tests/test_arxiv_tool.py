from backend.tools.arxiv_tool import get_arxiv_tool

def test_arxiv_tool_runs():
    tool = get_arxiv_tool()
    query = "attention is all you need"
    result = tool.run(query)
    
    assert isinstance(result, str)
    assert len(result) > 0
    assert "attention" in result.lower() or "neural" in result.lower()
