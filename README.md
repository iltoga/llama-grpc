# LLaMA-grpc

This is a gRPC server that provides an API for interacting with a Llama-based language model built by [Meta AI](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/). It allows users to generate text based on a give prompt template.

This example project uses a fine tuned LLM called [gpt4all](https://huggingface.co/LLukas22/gpt4all-lora-quantized-ggjt), obtained from the original LLamA 7B model and should perform better than the original one for generating 'chat-like' answers.

### IMPORTANT note about the license
This example application is released under MIT license, meaning you can do whatever you want with it and its code, but as of April 2023, Meta AI (Facebook) and openai only allows using GPT-like LLM models (or models trained with data from GPT) to be used for `research purpose`. So if you plan to use it in your commercial application, somebody,  some day, could knock at your door and ask a ridiculous amount of money ;)  

## Features

-   Generate text using a custom Llama model, (automaically downloads the model from [Hugging Face](https://huggingface.co/models)).
-   Update model parameters at runtime.
-   Custom prompt templates to be used in different context (eg. "The story teller" and "Fun Fact Generator").
-   Automatic translaction of generated text.

## Requirements

-   Python 3.7+
-   grpcio
-   grpcio-tools
-   huggingface_hub
-   Jinja2
-   pyllamacpp
-   duckduckgo_search

## Installation

1.  Clone this repository.
2.  Install the required packages:

bashCopy code

```bash
pip install -r requirements.txt

or

make install
```

3.  Create a `.env` file with the necessary environment variables (examples below).
    
4.  Start the server:
```bash
python main.py

or 

make run
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
2.  `UpdateParameters`: (TODO) Updates the Llama context parameters and reloads the model. Returns a success status.

## Examples
After running the server, open a grpc client application (such as BloomRPC), import `pyllamacpp.proto`, open `ptllamacpp.LlamaModel.GenerateText` and try these payloads (note that you can change the language of the answer and use any language for the product description):

### Fun fact generator
this prompt template will generate a fun fact about the product
```json
{
  "productName": "Indomie Mi Goreng",
  "productDescription": "Indomie Mi Goreng adalah rasa Indomie paling populer di seluruh dunia. Dibuat dengan tepung terigu berkualitas dan bahan serta bumbu segar pilihan, sepiring Indomie Mi Goreng pasti akan mencerahkan hari Anda.",
  "template": "funfact-generator-w-description",
  "language": "id"
}
```

example of answer:
```json
{
  "text": "Indomie Mi Goreng adalah rasa Indomie paling populer di seluruh dunia. Dibuat dengan tepung terigu berkualitas dan bahan-bahan segar pilihan serta rempah-rempah, sepiring Indomie Mi Goreng pasti akan mencerahkan hari Anda."
}
```

### The story teller
this prompt template will generate a short story of the product

```json
{
  "productName": "Indomie Mi Goreng",
  "productDescription": "Indomie Mi Goreng adalah rasa Indomie paling populer di seluruh dunia. Dibuat dengan tepung terigu berkualitas dan bahan serta bumbu segar pilihan, sepiring Indomie Mi Goreng pasti akan mencerahkan hari Anda.",
  "template": "story-teller",
  "language": "id",
  "gptParameters": {
    "nPredict": "200"
  }  
}
```

example of answer:
```json
{
  "text": "Dahulu kala, ada seorang anak kecil bernama Indomie. Dia suka makan mie Indomie untuk makan malam, tetapi dia tidak punya cukup uang untuk membelinya sepanjang waktu. Suatu hari, orang tuanya membawanya ke supermarket dan mengatakan kepadanya bahwa mereka akan membeli beberapa bahan makanan. Mereka mengatakan bahwa dia bisa memilih satu item dari toko. Dia bersemangat karena dia tahu persis apa yang dia inginkan: mie Indomie Mi Goreng! Mie Indomie Mi Goreng adalah makanan favorit Indomie, dan dia tidak sabar untuk mencobanya sendiri! Orang tuanya membawanya ke bagian Indomie di toko dan membiarkannya memilih favoritnya sendiri. Dia sangat senang sehingga dia berlari ke rak dan mengambil sekotak mie Indomie Mi Goreng dengan kedua tangan! Orang tua Indomie terkejut dengan antusiasmenya"
}
```



## License

This project is licensed under the [MIT License](https://chat.openai.com/LICENSE).

## Contribute
[Contribute to LLaMA-grpc](CONTRIBUTE.md)
