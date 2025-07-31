from langchain_community.tools.arxiv import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper

def get_arxiv_tool():
    wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=250)
    return ArxivQueryRun(tool=wrapper)
