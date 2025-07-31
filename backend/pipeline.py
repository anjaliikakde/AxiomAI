from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor
from .llm import get_llm
from .tools.wiki_tool import get_wikipedia_tool
from .tools.arxiv_tool import get_arxiv_tool
from .tools.retriever_tool import get_retriever_tool

def get_agent_executor():
    prompt = hub.pull("hwchase17/openai-functions-agent")

    tools = [
        get_wikipedia_tool(),
        get_arxiv_tool(),
        get_retriever_tool(),
    ]

    agent = create_openai_tools_agent(
        llm=get_llm(),
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(agent=agent, tools=tools, verbose=True)
