from huggingface_hub import HfApi
from huggingface_hub import login, logout, get_token, snapshot_download
from flask import Flask
from typing import Union, List, Dict
from transformers import AutoModelForCausalLM

app = Flask(__name__)

base_path = "/model"

@app.route(f"{base_path}/login/<token>", methods=["GET"])
def login_to_hf(token):
    return login(token=token)


@app.route(f"{base_path}/download/<model_provider>/<model_name>")
def download_model(model_provider : str, model_name : str) -> Dict:
    model_id = model_provider + "/" + model_name
    
    if get_token() is None:
        assert("Please Login first")
        return {
            "message" : "Please Login First",
            "success" : False
        }

    snapshot_download(repo_id=model_id)

    return {
        "message" : "Model downloaded successfully",
        "success" : True
    }
    

@app.route(f"{base_path}/search")
def get_models() -> Dict:
    api = HfApi()
    models = api.list_models(
        task="text-generation",
        library="pytorch",
    )

    model_list = iter(models)
    model = next(model_list)

    return model.id

@app.route(f"{base_path}/hf-status")
def is_logged_in() -> Dict:
    
    try:
        token = get_token()
    except:
        return {
            "success" : False,
            "message" : "Unable to verify hf logged in status",
            "status" : 500
        }

    if token is None:
        return {
            "success" : True,
            "message" : "You are not logged into your hugging face account",
            "status" : 200
        }

    return {
        "success" : True,
        "message" : "You are logged into your hugging face account",
        "status" : 200
    }

# logout()
# print(get_token())

# print(login_to_hf("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"))