import os
import json
import grpc
import sys
import signal
from concurrent import futures
import pyllamacpp_pb2
import pyllamacpp_pb2_grpc
from pyllamacpp.model import Model
from huggingface_hub import hf_hub_download
from jinja2 import Environment, FileSystemLoader
from duckduckgo_search import ddg_translate

class LlamaModelService(pyllamacpp_pb2_grpc.LlamaModelServicer):
    llama_context_params = {
        "n_ctx": 10000,
    }
    gpt_params = {
        "n_predict": 100,
        "n_threads": 5,
        "temp": 0.6,
    }

    def __init__(self):
        self.__load_env_vars()

        #Download the model
        hf_hub_download(self.repo_id, filename=self.ggml_model, local_dir=".")

        #Load custom model params from env
        try:
            custom_llama_context_parameters = json.loads(os.environ.get('LLAMA_CONTEXT_PARAMETERS', "{}"))
        except json.JSONDecodeError:
            print("Warning: LLAMA_CONTEXT_PARAMETERS contains invalid JSON. Using default parameters.")
            custom_llama_context_parameters = {}

        self.llama_context_params.update(custom_llama_context_parameters)

        # create the model
        self.model = Model(ggml_model=self.ggml_model, **self.llama_context_params)

    def __load_env_vars(self):
        #load env vars
        self.default_prompt_template = os.environ.get('DEFAULT_PROMPT_TEMPLATE', "funfact-generator-w-description")
        self.ggml_model = os.environ.get('GGML_MODEL', "ggjt-model.bin")
        self.repo_id = os.environ.get('REPO_ID', "LLukas22/gpt4all-lora-quantized-ggjt")

    def GenerateText(self, request, context):
        # update the gpt params with the new ones from the request
        reqParams = {}
        if request.gptParameters.nThreads != "":
            reqParams["n_threads"] = float(request.gptParameters.nThreads)
        if request.gptParameters.temp != "":
            reqParams["temp"] = float(request.gptParameters.temp)
        if request.gptParameters.topK != "":
            reqParams["top_k"] = float(request.gptParameters.topK)
        if request.gptParameters.topP != "":
            reqParams["top_p"] = float(request.gptParameters.topP)
        if request.gptParameters.repeatLastN != "":
            reqParams["repeat_last_n"] = float(request.gptParameters.repeatLastN)
        if request.gptParameters.repeatPenalty != "":
            reqParams["repeat_penalty"] = float(request.gptParameters.repeatPenalty)
        if request.gptParameters.nBatch != "":
            reqParams["n_batch"] = float(request.gptParameters.nBatch)
        if request.gptParameters.nPredict != "":
            reqParams["n_predict"] = float(request.gptParameters.nPredict)
        self.gpt_params.update(reqParams)

        # get the template and compile the prompt
        templateName = request.template if request.template != "" else self.default_prompt_template
        env = Environment(loader=FileSystemLoader('prompt_templates'))
        template = env.get_template(f"{templateName}.j2")
        template_terminator = "Bot:"

        # Translate the product description to english to facilitate the model generating the fun fact
        if request.productDescription != "":
            request.productDescription = translateTo(request.productDescription, lang="en")
        conversation_start = template.render(
            product_name=request.productName,
            product_description=request.productDescription,
            terminator=template_terminator,
        )

        generated_text = self.model.generate(
            conversation_start,
            new_text_callback=None,
            verbose=False,
            **self.gpt_params,
        )

        # Extract the response text after the "Bot:" delimiter
        try:
            response = generated_text.split(template_terminator)[1].strip()
        except IndexError:
            try:
                response = generated_text.split("Text:")[1].strip()
            except IndexError:
                response = generated_text

        # Translate the response to the requested language
        if request.language != "":
            response = translateTo(response, lang=request.language)
        return pyllamacpp_pb2.GenerateTextResponse(text=response)

    def UpdateParameters(self, request, context):
        # update the llama params with the new ones from the request
        self.llama_context_params.update(request.llama_context_parameters)

        # create the model
        self.model = Model(ggml_model=self.ggml_model, **self.llama_context_params)
        return pyllamacpp_pb2.UpdateParametersResponse(success=True)

def translateTo(text, lang="en"):
    translation = ddg_translate(text, to=lang)
    if len(translation) > 0:
        # only use the first translation
        translation = translation[0]
        if translation["detected_language"] != lang:
            text = translation["translated"]
    return text

def exit_gracefully(signum, frame):
    print("Caught signal, stopping server...")
    server.stop(0)
    print("Server stopped. Exiting...")
    sys.exit(0)

def serve():
    global server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pyllamacpp_pb2_grpc.add_LlamaModelServicer_to_server(LlamaModelService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server started on port 50051')

    # Register the signal handler for graceful exit
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        exit_gracefully(None, None)

if __name__ == '__main__':
    serve()
