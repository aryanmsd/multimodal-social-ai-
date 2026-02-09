import requests
import os
from PIL import Image
import io
import time

HF_API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"

def generate_image(prompt: str):
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True
        }
    }

    response = requests.post(
        HF_API_URL,
        headers=headers,
        json=payload,
        timeout=90
    )

    # ---------- DEBUG HANDLING ----------
    if response.status_code == 503:
        raise Exception(
            "Model is loading on Hugging Face. Please wait 20–30 seconds and try again."
        )

    if response.headers.get("content-type", "").startswith("application/json"):
        raise Exception(response.json())

    if response.status_code != 200:
        raise Exception(f"HF Error {response.status_code}: {response.text}")

    return Image.open(io.BytesIO(response.content))
