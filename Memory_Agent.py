from typing import TypedDict,List,Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END, START
from dotenv import load_dotenv
import os 

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm=ChatGroq(model="qwen/qwen3-32b",api_key=os.getenv("GROQ_API_KEY"))

def process(state: AgentState)-> AgentState:
    """This node will solve the request you input"""
    response=llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    print("CURRENT STATE: ",  state["messages"])
    return state
graph=StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START,"process")
graph.add_edge("process", END)
agent=graph.compile()

conversation_history=[]
user_input=input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    
    result=agent.invoke({"messages":conversation_history })
    # print(result["messages"])
    conversation_history=result["messages"]
    
    user_input= input("Enter: ")

with open ("logging.txt", "w",encoding="utf-8") as file:
    file.write("Your conversation Log:\n")
    for message in conversation_history:
        if isinstance(message,HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message,AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of Conversation")
print("Conversation saved to logging.txt")