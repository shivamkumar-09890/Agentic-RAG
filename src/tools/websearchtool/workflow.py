"""
Workflow for performing web searches using available search tools.
"""
from typing import Optional, List
from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

from llms.huggingface_api import get_huggingface_llm
import web_search

class WebSearchWorkflow:
    def __init__(
        self, 
        input_text: str, 
        tools: Optional[List[BaseTool]] = None
    ):
        self.llm = get_huggingface_llm()
        
        self.input_text = input_text
        
        self.tools = tools or [
            tool_config['tool']() for tool_config in nodes.AVAILABLE_TOOLS 
            if tool_config['id'] == 'web_search'
        ]
        
        tools_description = "\n".join([
            f"- {tool_config['id']}: {tool_config['description']}" 
            for tool_config in nodes.AVAILABLE_TOOLS
        ])
        
        self.prompt = ChatPromptTemplate.from_template(
            "You are an AI research assistant tasked with gathering web information.\n\n"
            f"Available tools:\n{tools_description}\n\n"
            "Context: You need to find relevant web information based on the input query.\n\n"
            "Guidelines:\n"
            "1. Carefully analyze the input query\n"
            "2. Determine if web search would be helpful\n"
            "3. If web search is appropriate, explicitly mention 'web_search'\n"
            "4. Provide context for why web search is needed\n\n"
            "Input query:\n{text}"
        )
    
    def run(self) -> str:
        workflow = (
            RunnablePassthrough.assign(
                llm_output=self.prompt | self.llm
            )
        )
        
        result = workflow.invoke({
            "text": self.input_text
        })
        
        output = result['llm_output'].content
        
        for tool_config in nodes.AVAILABLE_TOOLS:
            tool_name = tool_config['id']
            if tool_name in output.lower():
                try:
                    tool = tool_config['tool']()
                    if tool_name == 'web_search':
                        output = tool.run(self.input_text)
                except Exception as e:
                    print(f"Tool {tool_name} failed: {e}")
        
        return output

def create_workflow(
    input_text: str, 
    tools: Optional[List[BaseTool]] = None
):
    return WebSearchWorkflow(input_text, tools) 