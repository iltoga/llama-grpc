from huggingface_hub import hf_hub_download
from pyllamacpp.model import Model

def new_text_callback(text):
    print(text, end="")
    return True

#Download the model
repo_id="LLukas22/gpt4all-lora-quantized-ggjt"
ggml_model="ggjt-model.bin"
hf_hub_download(repo_id, filename=ggml_model, local_dir=".")


#Load the model

# create a dict with the llama params
llama_context_params = {
    "n_ctx": 2000,
    # "n_parts": -1,
    "seed": 0,
    "embedding": 0,
}
# create a dict with the gpt params
gpt_params = {
    "n_threads": 4,
    "temp": 0.4,    
}

# create the model
model = Model(ggml_model=ggml_model, **llama_context_params)

#print the model params
print(model.llama_params)

#Generate
prompt="User: How are you doing?\nBot:"

model.generate(
    prompt, 
    n_predict=50, 
    new_text_callback=new_text_callback,
    verbose=False,
    **gpt_params,
    )
