# Llama-grpc

This is a gRPC server that provides an API for interacting with a Llama-based language model built by [Meta AI](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/). It allows users to generate text, and update model parameters.

This example project uses a fine tuned model, obtained from the original LLamA 7B model.

### IMPORTANT note about the license
This example application is released under MIT license, meaning you can do whatever you want with it and its code, but as of April 2023, Meta AI (Facebook) and openai only allows using GPT-like LLM models (or models trained with data from GPT) to be used for `research purpose`. So if you plan to use it in your commercial application, somebody,  some day, could knock at your door and ask a ridiculous amount of money ;)  

## Features

-   Generate text using a custom Llama model.
-   Update model parameters.
-   Custom prompt templates with Jinja2.
-   Easy integration with Hugging Face Hub for model hosting.

## Requirements

-   Python 3.7+
-   grpcio
-   grpcio-tools
-   huggingface_hub
-   Jinja2
-   pyllamacpp

## Installation

1.  Clone this repository.
2.  Install the required packages:

bashCopy code

```bash
pip install -r requirements.txt
```

3.  Create a `.env` file with the necessary environment variables (examples below).
    
4.  Start the server:
```bash
python main.py
``` 

## Environment Variables

The server uses environment variables to customize the behavior. Here are the available options:

-   `DEFAULT_PROMPT_TEMPLATE`: The default template name (without the .j2 extension) to use for generating prompts (default: "funfact-generator").
-   `GGML_MODEL`: The name of the GGML model file (default: "ggjt-model.bin").
-   `REPO_ID`: The Hugging Face Hub repository ID containing the model (default: "LLukas22/gpt4all-lora-quantized-ggjt").
-   `LLAMA_CONTEXT_PARAMETERS`: A JSON string containing custom Llama context parameters.

Example `.env` file:
```makefile
DEFAULT_PROMPT_TEMPLATE=my-template
GGML_MODEL=my-ggml-model.bin
REPO_ID=myuser/my-model-repo
LLAMA_CONTEXT_PARAMETERS={"n_ctx": 2500}
``` 

## API

The gRPC service provides two methods:

1.  `GenerateText`: Generates text based on a given product name and description. It accepts an optional template name and GPT parameters. Returns the generated text.
2.  `UpdateParameters`: Updates the Llama context parameters and reloads the model. Returns a success status.

## License

This project is licensed under the [MIT License](https://chat.openai.com/LICENSE).