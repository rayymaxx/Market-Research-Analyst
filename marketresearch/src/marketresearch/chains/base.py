"""
Base LCEL chain implementation
"""
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Optional, Any, Dict
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class BaseChain(Generic[T]):
    """Base LCEL chain with error handling and validation"""
    
    def __init__(self, llm, output_model: type[T], system_prompt: str):
        self.llm = llm
        self.output_parser = PydanticOutputParser(pydantic_object=output_model)
        self.system_prompt = system_prompt
    
    def create_chain(self) -> Runnable:
        """Create LCEL chain: Prompt -> LLM -> Parser"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt + "\n\n{format_instructions}"),
            ("human", "{input}")
        ])
        
        return prompt | self.llm | self.output_parser
    
    def invoke(self, input_data: Dict[str, Any]) -> T:
        """Invoke chain with proper error handling"""
        try:
            chain = self.create_chain()
            
            # Prepare final input with format instructions
            final_input = {
                **input_data,
                "format_instructions": self.output_parser.get_format_instructions()
            }
            
            result = chain.invoke(final_input)
            logger.info(f"✅ Chain {self.__class__.__name__} executed successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Chain {self.__class__.__name__} failed: {str(e)}")
            raise

class ChainInput(BaseModel):
    """Base input for all chains"""
    research_topic: str = Field(description="Research topic")
    current_date: str = Field(description="Current date for reporting")