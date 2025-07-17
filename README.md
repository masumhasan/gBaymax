# 🧠 Friday - Your Personal AI Assistant

This is a Python-based AI assistant inspired by _Jarvis_, capable of:

- 🔍 Searching the web
- 🌤️ Weather checking
- 📨 Sending Emails
- 📷 Vision through camera (Web app)
- 🗣️ Speech
- 📝 Chat (Web app)
- 💬 **Text Chat** - Send and receive text messages

This agent uses LiveKit that is 100% free!

---

## 💬 Text Chat Feature

The agent now supports text chat functionality! You can send text messages to Baymax and receive responses without using voice.

### How Text Chat Works:

1. **Data Channel**: Uses LiveKit's data channel for real-time text messaging
2. **Tool Integration**: Text messages can trigger the same tools as voice (weather, web search, email)
3. **Bidirectional**: Send messages to Baymax and receive responses in text format

### Testing Text Chat:

1. **HTML Client**: Use `test_client.html` for a simple web interface
2. **Python Client**: Run `text_chat_example.py` for a command-line interface
3. **Custom Integration**: Use the LiveKit client SDK in your preferred language

### Example Usage:

```python
# Send a message via data channel
message = "What's the weather in New York?"
await room.local_participant.publish_data(
    message.encode('utf-8'),
    kind=DataPacket_Kind.RELIABLE
)

# Receive response via data_received event
@room.on("data_received")
async def on_data_received(data, participant):
    response = data.decode('utf-8')
    print(f"Baymax: {response}")
```

---

## 🚀 Setup Instructions

### 🪟 Windows Users (Quick Start)

**Option 1: Batch Script (Easiest)**

```batch
# Run this in your activated virtual environment
install.bat
```

**Option 2: Manual Installation**

```bash
# 1. Install basic requirements
pip install -r requirements.txt

# 2. Install llama-cpp-python (precompiled wheels)
python quick_fix.py

# 3. Test the installation
python test_local_llm.py

# 4. Run the agent
python nagent.py
```

**Option 3: If compilation issues persist**

```bash
# Use the comprehensive installer
python install_windows.py
```

### 🐧 Linux/Mac Users

**Local LLM Installation:**

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac

# 2. Run the auto-installer
python install_local_llm.py

# 3. Test the local model
python test_local_llm.py

# 4. Run the agent
python nagent.py
```

### ☁️ Cloud LLM (Alternative)

Use Google's cloud-based model:

1. Create the Virtual Environment first!
2. Activate it
3. Install all the required libraries in the requirements.txt file
4. In the .ENV - File you should paste your API-Keys and your LiveKit Secret, LiveKit URL.
   If you want to use the Send Email Tool also specify your Gmail Account and App Password.
5. Make sure that your LiveKit Account is set-up correctly.
6. Run the agent: `python agent.py`

---

## 🤖 Local LLM Configuration

### Model Settings

The local model configuration is in `model_config.py`:

```python
# Current model: Gemma 3n E2B IT (4-bit quantized)
"gemma-3n-E2B-it-IQ4_XS": {
    "path": "models/gemma-3n-E2B-it-IQ4_XS.gguf",
    "n_ctx": 2048,        # Context window size
    "n_threads": 4,       # CPU threads
    "n_gpu_layers": 0,    # GPU layers (increase for GPU support)
    "temperature": 0.8,   # Response creativity
    "max_tokens": 512,    # Maximum response length
}
```

### GPU Support

To enable GPU acceleration:

1. **NVIDIA GPU**: The installation script will automatically detect and configure CUDA
2. **AMD GPU**: ROCm support is automatically detected on Linux
3. **Manual Configuration**: Set `n_gpu_layers` in the model config (e.g., 20-40 layers)

### Environment Variables

You can override settings with environment variables:

```bash
# Windows
set BAYMAX_MODEL=gemma-3n-E2B-it-IQ4_XS
set BAYMAX_GPU_LAYERS=20
set BAYMAX_THREADS=8

# Linux/Mac
export BAYMAX_MODEL=gemma-3n-E2B-it-IQ4_XS
export BAYMAX_GPU_LAYERS=20
export BAYMAX_THREADS=8
```

### Testing Local Model

```bash
# Test the local model
python test_local_llm.py

# Test text chat with local model
python text_chat_example.py

# Check available models
python model_config.py
```

---

## 🛠️ Troubleshooting

### Common Issues on Windows

**1. llama-cpp-python installation fails**

```
Error: Building wheel for llama-cpp-python failed
```

**Solutions:**

- Use precompiled wheels: `python quick_fix.py`
- Install Visual Studio Build Tools with C++ support
- Use the comprehensive installer: `python install_windows.py`
- Try conda: `conda install -c conda-forge llama-cpp-python`

**2. CMake errors**

```
CMake Error: CMAKE_C_COMPILER not set
```

**Solutions:**

- Install Visual Studio Build Tools
- Use precompiled wheels (recommended)
- Install CMake manually

**3. Model file not found**

```
FileNotFoundError: Model file not found
```

**Solutions:**

- Ensure `models/gemma-3n-E2B-it-IQ4_XS.gguf` exists
- Check model path in `model_config.py`
- Download model from Hugging Face

**4. Out of memory**

```
RuntimeError: Out of memory
```

**Solutions:**

- Reduce `n_ctx` in model config
- Use smaller model variant
- Close other applications

### Performance Tips

**CPU Optimization:**

- Set `n_threads` to your CPU core count
- Use `n_ctx=1024` for faster responses
- Enable `use_mlock=True` for better memory management

**GPU Acceleration:**

- Set `n_gpu_layers=20-40` for NVIDIA GPUs
- Install CUDA toolkit for better performance
- Monitor GPU memory usage

**Memory Management:**

- Use 4-bit quantized models (IQ4_XS)
- Reduce context window if memory limited
- Close unnecessary applications

---

## 🛠️ Text Chat Implementation Details

The text chat feature is implemented in the `agent.py` file:

- **Data Channel Handler**: Listens for incoming text messages
- **Message Processing**: Processes text input through the same LLM and tools
- **Response Generation**: Sends responses back through the data channel
- **Error Handling**: Gracefully handles connection and processing errors

### Key Components:

1. **Message Reception**: `@ctx.room.on("data_received")`
2. **LLM Integration**: Uses Local Llama.cpp model for text processing
3. **Tool Execution**: Same tools available for both voice and text
4. **Response Formatting**: Prefixes responses with "Baymax:" for clarity

### Performance Notes:

- **Local Model**: No API costs, privacy-focused, works offline
- **Response Time**: ~1-3 seconds on CPU, ~0.5-1 second with GPU
- **Memory Usage**: ~4-8GB RAM for the Gemma model
- **Context Window**: 2048 tokens (adjustable in config)
