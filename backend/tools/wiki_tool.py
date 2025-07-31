from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

def get_wikipedia_tool():
    wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=250)
    return WikipediaQueryRun(api_wrapper=wrapper)


