"""
Local Llama.cpp model wrapper for LiveKit agents

This module provides a wrapper for using local Llama.cpp models
with the LiveKit agents framework.
"""

import os
import logging
from typing import Optional, List, Dict, Any, AsyncIterator
from llama_cpp import Llama
from livekit.agents import llm, APIConnectOptions
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)


class LlamaCppModel(llm.LLM):
    """Local Llama.cpp model wrapper for LiveKit agents"""
    
    def __init__(
        self,
        model_path: str,
        n_ctx: int = 2048,
        n_threads: int = 4,
        n_gpu_layers: int = 0,
        temperature: float = 0.8,
        max_tokens: int = 512,
        top_p: float = 0.95,
        top_k: int = 40,
        verbose: bool = False,
        **kwargs
    ):
        """
        Initialize the Llama.cpp model
        
        Args:
            model_path: Path to the .gguf model file
            n_ctx: Context size
            n_threads: Number of threads to use
            n_gpu_layers: Number of layers to offload to GPU
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            top_p: Top-p sampling parameter
            top_k: Top-k sampling parameter
            verbose: Enable verbose logging
        """
        super().__init__()
        
        self.model_path = Path(model_path)
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.n_gpu_layers = n_gpu_layers
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.top_k = top_k
        self.verbose = verbose
        
        # Initialize the model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Llama.cpp model"""
        try:
            if not self.model_path.exists():
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            logger.info(f"Loading Llama.cpp model from: {self.model_path}")
            
            self.model = Llama(
                model_path=str(self.model_path),
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                n_gpu_layers=self.n_gpu_layers,
                verbose=self.verbose,
                chat_format="chatml"  # Use ChatML format for better chat performance
            )
            
            logger.info("Llama.cpp model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load Llama.cpp model: {e}")
            raise
    
    def chat(
        self,
        *,
        chat_ctx: llm.ChatContext,
        tools: Optional[List[llm.FunctionTool]] = None,
        conn_options: APIConnectOptions = APIConnectOptions(),
        **kwargs
    ) -> "LlamaCppChatStream":
        """Start a chat completion with the model"""
        return LlamaCppChatStream(
            model=self.model,
            chat_ctx=chat_ctx,
            tools=tools,
            conn_options=conn_options,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            top_k=self.top_k,
            llm_instance=self,
        )
    
    async def generate_response(self, prompt: str) -> str:
        """Generate a simple response from a prompt"""
        try:
            response = self.model(
                prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                top_k=self.top_k,
                stop=["<|im_end|>", "\n\n"],
                echo=False
            )
            
            return response['choices'][0]['text'].strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error generating a response."


class LlamaCppChatStream(llm.LLMStream):
    """Chat stream implementation for Llama.cpp"""
    
    def __init__(
        self,
        model: Llama,
        chat_ctx: llm.ChatContext,
        tools: Optional[List[llm.FunctionTool]],
        conn_options: APIConnectOptions,
        temperature: float,
        max_tokens: int,
        top_p: float,
        top_k: int,
        llm_instance: 'LlamaCppModel',
    ):
        super().__init__(llm_instance, chat_ctx=chat_ctx, tools=tools or [], conn_options=conn_options)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.top_k = top_k
        self._response_future: Optional[asyncio.Future] = None
    
    async def _run(self):
        """Main task for processing the chat stream"""
        try:
            # Convert chat context to prompt
            prompt = self._build_prompt_from_context()
            
            # Generate response using the model
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                self._generate_response,
                prompt
            )
            
            # Create and emit chat chunks
            chunk_id = "chat_chunk"
            
            # Emit the response as a single chunk
            delta = llm.ChoiceDelta(
                content=response,
                role="assistant"
            )
            
            usage = llm.CompletionUsage(
                completion_tokens=len(response.split()),
                prompt_tokens=len(prompt.split()),
                total_tokens=len(prompt.split()) + len(response.split())
            )
            
            chunk = llm.ChatChunk(
                id=chunk_id,
                delta=delta,
                usage=usage
            )
            
            # Send the chunk through the event channel
            self._event_ch.send_nowait(chunk)
            
        except Exception as e:
            logger.error(f"Error in chat stream: {e}")
            # Create an error chunk
            error_chunk = llm.ChatChunk(
                id="error_chunk",
                delta=llm.ChoiceDelta(
                    content=f"Error: {e}",
                    role="assistant"
                )
            )
            self._event_ch.send_nowait(error_chunk)
    
    def _build_prompt_from_context(self) -> str:
        """Build a prompt from the chat context"""
        try:
            # Convert messages to a format suitable for the model
            messages = []
            
            for msg in self._chat_ctx.messages:
                if msg.role == "system":
                    messages.append(f"<|im_start|>system\n{msg.content}<|im_end|>")
                elif msg.role == "user":
                    messages.append(f"<|im_start|>user\n{msg.content}<|im_end|>")
                elif msg.role == "assistant":
                    messages.append(f"<|im_start|>assistant\n{msg.content}<|im_end|>")
            
            # Add assistant start token
            messages.append("<|im_start|>assistant")
            
            return "\n".join(messages)
            
        except Exception as e:
            logger.error(f"Error building prompt: {e}")
            return "Please respond as a helpful assistant."
    
    def _generate_response(self, prompt: str) -> str:
        """Generate response using the model (synchronous)"""
        try:
            response = self.model(
                prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                top_k=self.top_k,
                stop=["<|im_end|>", "<|im_start|>"],
                echo=False
            )
            
            return response['choices'][0]['text'].strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error generating a response."


def create_local_llm(
    model_name: str = None,
    model_path: str = None,
    **kwargs
) -> LlamaCppModel:
    """
    Create a local Llama.cpp model instance
    
    Args:
        model_name: Name of the model from model_config.py
        model_path: Direct path to the model file (overrides model_name)
        **kwargs: Additional arguments for the model
    
    Returns:
        LlamaCppModel instance
    """
    from model_config import get_model_config, DEFAULT_MODEL
    
    if model_path:
        # Use direct path
        if not os.path.isabs(model_path):
            model_path = os.path.join(os.path.dirname(__file__), model_path)
        
        # Use default config but override with kwargs
        config = get_model_config(DEFAULT_MODEL)
        config.update(kwargs)
        config["model_path"] = model_path
        
    else:
        # Use named model configuration
        if model_name is None:
            model_name = DEFAULT_MODEL
        
        config = get_model_config(model_name)
        config.update(kwargs)
        
        # Convert Path to string
        config["model_path"] = str(config.pop("path"))
    
    return LlamaCppModel(**config)
