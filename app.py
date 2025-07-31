import streamlit as st
from langchain import hub
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from backend.tools.wiki_tool import get_wikipedia_tool
from backend.tools.arxiv_tool import get_arxiv_tool
from backend.tools.retriever_tool import get_retriever_tool
from urllib.parse import urlparse
import time
import os

# --- Black Theme Configuration ---
st.set_page_config(
    page_title="Research Assistant",
    page_icon="🎀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Dark Theme CSS ---
st.markdown("""
    <style>
        :root {
            --primary: #3b82f6;
            --background: #0e1117;
            --card: #1e293b;
            --text: #f8fafc;
            --border: #334155;
        }
        
        .stApp {
            background: var(--background);
            color: var(--text);
        }
        
        .stChatMessage {
            background: var(--card) !important;
            border: 1px solid var(--border);
            border-radius: 12px;
        }
        
        [data-testid="stChatMessage-user"] {
            border-left: 4px solid var(--primary);
        }
        
        .stTextInput input {
            background: var(--card) !important;
            color: var(--text) !important;
            border-color: var(--border) !important;
        }
        
        .stButton button {
            background: var(--primary) !important;
            color: white !important;
            border: none;
        }
        
        .stMarkdown p {
            color: var(--text) !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Tool Initialization ---
@st.cache_resource
def init_tools(source_url):
    return [
        get_wikipedia_tool(),
        get_arxiv_tool(),
        get_retriever_tool(source_url)
    ]

def get_agent_executor(source_url):
    tools = init_tools(source_url)
    agent = create_openai_tools_agent(
        llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3),
        tools=tools,
        prompt=hub.pull("hwchase17/openai-functions-agent")
    )
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- UI Components ---
def render_header():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: #f8fafc;'>📑 Research Assistant</h1>
            <p style='color: #94a3b8;'>Search Wikipedia, ArXiv, and custom web pages</p>
        </div>
    """, unsafe_allow_html=True)

def main():
    render_header()
    
    # URL Input
    source_url = st.text_input(
        "Enter a URL to include in research:",
        value="https://python.langchain.com",
        help="Must start with http:// or https://"
    )
    
    # Initialize agent
    if "agent" not in st.session_state or st.session_state.current_url != source_url:
        with st.spinner("🔄 Initializing tools..."):
            st.session_state.agent = get_agent_executor(source_url)
            st.session_state.current_url = source_url
            st.session_state.chat_history = []
    
    # Chat display
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # User input
    if query := st.chat_input("Ask your research question..."):
        with st.chat_message("user"):
            st.markdown(query)
        
        st.session_state.chat_history.append({"role": "user", "content": query})
        
        with st.chat_message("assistant"):
            response = st.session_state.agent.invoke({"input": query})
            st.markdown(response["output"])
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": response["output"]
            })

if __name__ == "__main__":
    main()