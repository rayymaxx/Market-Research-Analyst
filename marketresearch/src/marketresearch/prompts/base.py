"""
Base classes and utilities for advanced prompt management
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)

@dataclass
class FewShotExample:
    """Structure for few-shot learning examples"""
    input: Dict[str, Any]
    output: Dict[str, Any]
    explanation: str

class BasePromptManager(ABC):
    """Abstract base class for advanced prompt management"""
    
    def __init__(self):
        self.prompts = self._load_prompts()
        self.few_shot_examples = self._load_few_shot_examples()
    
    @abstractmethod
    def _load_prompts(self) -> Dict[str, str]:
        """Load all prompts for this category"""
        pass
    
    def _load_few_shot_examples(self) -> Dict[str, List[FewShotExample]]:
        """Load few-shot examples - can be overridden by subclasses"""
        return {}
    
    def get_prompt(self, prompt_name: str, variables: Dict[str, Any] = None) -> str:
        """Get a prompt with variable substitution and few-shot examples"""
        prompt = self.prompts.get(prompt_name)
        if not prompt:
            raise ValueError(f"Prompt '{prompt_name}' not found in {self.__class__.__name__}")
        
        # Add few-shot examples if available
        few_shot_content = self._get_few_shot_content(prompt_name)
        full_prompt = few_shot_content + "\n\n" + prompt if few_shot_content else prompt
        
        try:
            return full_prompt.format(**(variables or {}))
        except KeyError as e:
            logger.error(f"Missing variable in prompt '{prompt_name}': {e}")
            raise
    
    def _get_few_shot_content(self, prompt_name: str) -> str:
        """Generate few-shot examples content for a prompt"""
        examples = self.few_shot_examples.get(prompt_name, [])
        if not examples:
            return ""
        
        few_shot_content = "FEW-SHOT LEARNING EXAMPLES:\n\n"
        for i, example in enumerate(examples, 1):
            few_shot_content += f"EXAMPLE {i}:\n"
            few_shot_content += f"INPUT: {json.dumps(example.input, indent=2)}\n"
            few_shot_content += f"THINKING PROCESS: {example.explanation}\n"
            few_shot_content += f"OUTPUT: {json.dumps(example.output, indent=2)}\n\n"
        
        return few_shot_content
    
    def list_prompts(self) -> list:
        """List all available prompts in this manager"""
        return list(self.prompts.keys())

class ChainOfThoughtMixin:
    """Mixin for chain-of-thought prompting"""
    
    @staticmethod
    def add_chain_of_thought_instructions(base_prompt: str) -> str:
        """Add chain-of-thought reasoning instructions to a prompt"""
        cot_instructions = """
REASONING PROCESS (Chain of Thought):
1. FIRST, analyze the available data and identify key patterns
2. THEN, break down the problem into logical components
3. NEXT, apply relevant analytical frameworks
4. AFTER, synthesize findings and draw conclusions
5. FINALLY, structure the output according to requirements

Please show your reasoning at each step before providing the final answer.
"""
        return base_prompt + cot_instructions

class RoleBasedMixin:
    """Mixin for role-based prompting"""
    
    @staticmethod
    def add_role_context(base_prompt: str, role: str, expertise: List[str]) -> str:
        """Add role-based context to a prompt"""
        role_context = f"""
ROLE CONTEXT:
You are acting as a {role} with expertise in:
{chr(10).join(f'- {exp}' for exp in expertise)}

You must maintain this professional perspective throughout your analysis and recommendations.
"""
        return base_prompt + role_context