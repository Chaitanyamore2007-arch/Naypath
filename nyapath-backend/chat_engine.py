import os
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def run_chat(question: str, profile: Optional[dict], history: List[dict]):
    import rag_engine
    
    # 1. Retrieve Context
    context_text, sources = rag_engine.retrieve_context(question)
    if not context_text.strip():
        context_text = "No specific regulations found. Use general Maharashtra industrial compliance knowledge."
        
    # 2. Setup LLM
    llm = rag_engine.get_llm()
    
    # 3. Format history
    messages = [
        SystemMessage(content=f"You are Nyapath, an expert compliance assistant for Maharashtra, India.\n"
                              f"Use this context to answer the user: {context_text}\n"
                              f"User Profile: {profile or 'Not provided'}")
    ]
    
    for turn in history[-5:]:
        if turn["role"] == "user":
            messages.append(HumanMessage(content=turn["content"]))
        elif turn["role"] == "assistant":
            messages.append(AIMessage(content=turn["content"]))
            
    messages.append(HumanMessage(content=question))
    
    # 4. Generate response
    try:
        response = llm.invoke(messages)
        return {
            "answer": response.content,
            "sources": sources
        }
    except Exception as e:
        print(f"Chat failed: {e}")
        return {
            "answer": "I'm having trouble connecting to my knowledge base right now. Please try again.",
            "sources": []
        }
