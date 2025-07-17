"""
Configuration for local LLM models

This file contains configuration settings for different local models
that can be used with the Baymax agent.
"""

import os
from pathlib import Path

# Base directory for models
MODELS_DIR = Path(__file__).parent / "models"

# Model configurations
MODEL_CONFIGS = {
    "gemma-3n-E2B-it-IQ4_XS": {
        "path": MODELS_DIR / "gemma-3n-E2B-it-IQ4_XS.gguf",
        "n_ctx": 2048,
        "n_threads": 4,
        "n_gpu_layers": 0,  # Increase for GPU support
        "temperature": 0.8,
        "max_tokens": 512,
        "top_p": 0.95,
        "top_k": 40,
        "chat_format": "chatml",
        "description": "Gemma 3n model optimized for chat"
    },
    
    # Add more model configurations here
    "llama-7b-chat": {
        "path": MODELS_DIR / "llama-7b-chat.gguf",
        "n_ctx": 4096,
        "n_threads": 6,
        "n_gpu_layers": 0,
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 0.9,
        "top_k": 50,
        "chat_format": "llama-2",
        "description": "Llama 7B Chat model"
    },
    
    "mistral-7b-instruct": {
        "path": MODELS_DIR / "mistral-7b-instruct.gguf",
        "n_ctx": 4096,
        "n_threads": 6,
        "n_gpu_layers": 0,
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 0.9,
        "top_k": 50,
        "chat_format": "mistral",
        "description": "Mistral 7B Instruct model"
    }
}

# Default model to use
DEFAULT_MODEL = "gemma-3n-E2B-it-IQ4_XS"

# GPU configuration
GPU_CONFIG = {
    "auto_detect": True,  # Automatically detect GPU support
    "n_gpu_layers": 0,    # Number of layers to offload to GPU (0 = CPU only)
    "gpu_memory_fraction": 0.8,  # Fraction of GPU memory to use
}

# Performance settings
PERFORMANCE_CONFIG = {
    "n_threads": None,  # None = auto-detect
    "n_batch": 512,     # Batch size for processing
    "use_mlock": True,  # Lock memory to prevent swapping
    "use_mmap": True,   # Use memory mapping for model loading
}

def get_model_config(model_name: str = None) -> dict:
    """
    Get configuration for a specific model
    
    Args:
        model_name: Name of the model (defaults to DEFAULT_MODEL)
    
    Returns:
        Model configuration dictionary
    """
    if model_name is None:
        model_name = DEFAULT_MODEL
    
    if model_name not in MODEL_CONFIGS:
        raise ValueError(f"Model '{model_name}' not found in configurations")
    
    config = MODEL_CONFIGS[model_name].copy()
    
    # Auto-detect number of threads if not specified
    if PERFORMANCE_CONFIG["n_threads"] is None:
        config["n_threads"] = os.cpu_count() or 4
    else:
        config["n_threads"] = PERFORMANCE_CONFIG["n_threads"]
    
    # Apply GPU configuration if enabled
    if GPU_CONFIG["auto_detect"]:
        config["n_gpu_layers"] = GPU_CONFIG["n_gpu_layers"]
    
    return config

def list_available_models() -> list:
    """
    List all available models with their descriptions
    
    Returns:
        List of tuples (model_name, description, exists)
    """
    models = []
    for name, config in MODEL_CONFIGS.items():
        exists = config["path"].exists()
        models.append((name, config["description"], exists))
    
    return models

def validate_model_path(model_name: str) -> bool:
    """
    Validate that a model file exists
    
    Args:
        model_name: Name of the model
    
    Returns:
        True if model file exists, False otherwise
    """
    if model_name not in MODEL_CONFIGS:
        return False
    
    return MODEL_CONFIGS[model_name]["path"].exists()

# Environment-based configuration overrides
def load_env_config():
    """Load configuration from environment variables"""
    # Model selection
    env_model = os.getenv("BAYMAX_MODEL")
    if env_model and env_model in MODEL_CONFIGS:
        global DEFAULT_MODEL
        DEFAULT_MODEL = env_model
    
    # GPU layers
    env_gpu_layers = os.getenv("BAYMAX_GPU_LAYERS")
    if env_gpu_layers:
        try:
            GPU_CONFIG["n_gpu_layers"] = int(env_gpu_layers)
        except ValueError:
            pass
    
    # Number of threads
    env_threads = os.getenv("BAYMAX_THREADS")
    if env_threads:
        try:
            PERFORMANCE_CONFIG["n_threads"] = int(env_threads)
        except ValueError:
            pass

# Load environment configuration on import
load_env_config()

if __name__ == "__main__":
    # Print model information
    print("🤖 Available Local Models:")
    print("=" * 50)
    
    for name, description, exists in list_available_models():
        status = "✅ Available" if exists else "❌ Not found"
        print(f"{name}: {description} - {status}")
    
    print(f"\n🎯 Default model: {DEFAULT_MODEL}")
    print(f"🖥️  GPU layers: {GPU_CONFIG['n_gpu_layers']}")
    print(f"🧵 Threads: {PERFORMANCE_CONFIG['n_threads'] or 'auto'}")
