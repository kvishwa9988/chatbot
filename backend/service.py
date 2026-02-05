import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch #search engine to give real time facts
# Using langchain-classic for stable Memory and Agent support in 2026/Python 3.14
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_classic.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

# This is a global dictionary. It acts as a "short-term memory" storage for all users using the app simultaneously.
memories = {}


class ChatService:
    @staticmethod
    def get_executor(session_id: str):
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
        
        tools = [TavilySearch(max_results=2)]

        if session_id not in memories:
            memories[session_id] = ConversationBufferMemory(
                 
                llm=llm, # Needs an LLM to perform the summarization
                max_token_limit=500, # Only keep 500 tokens of raw chat; summarize the rest
                memory_key="chat_history",
                return_messages=True
            )
        
        # Domain Guard via System Prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a specialized assistant for Cyber Security. "
                       "ONLY answer questions within this domain. "
                       "If a user asks about anything else, politely explain that "
                       "your expertise is limited to Cyber Security."),
            #message place holder : special placeholder used inside a chat prompt template to dynamically insert a list of messages at runtime. instead of hardcoding them
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"), #"""Inserts the user’s current message at runtime"""
            #scratchpad stores Chain Links
            MessagesPlaceholder(variable_name="agent_scratchpad"), 
        ])

        agent = create_openai_tools_agent(llm, tools, prompt)
        return AgentExecutor(
            agent=agent, 
            tools=tools, 
            memory=memories[session_id], 
            verbose=True
        )

    @staticmethod
    def run_chat(session_id: str, user_input: str):
        executor = ChatService.get_executor(session_id)
        response = executor.invoke({"input": user_input})
        
        raw_output = response["output"]

        if isinstance(raw_output,dict):
            
            text_parts = [part['text'] for part in raw_output if isinstance(part, dict) and 'text' in part]
            return " ".join(text_parts)
        
        return str(raw_output)