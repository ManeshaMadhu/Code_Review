from transformers import pipeline
pipe = pipeline("text-generation", model="bigcode/starcoder")
from django.contrib.auth.decorators import login_required
import os

hf_token = os.environ.get("HF_TOKEN")

generator = None

def get_generator():
    global generator
    if generator is None:
        hf_token = os.environ.get("HF_TOKEN")
        if not hf_token:
            raise EnvironmentError("Hugging Face token (HF_TOKEN) is not set in environment variables.")

        generator = pipeline(
            "text-generation",
            model="bigcode/starcoderbase",
            token=hf_token
        )
    return generator

@login_required
def generate(code_text):
    gen = get_generator()  # Ensure the generator is initialized

    # Generate a descriptive code name using StarCoder
    name_prompt = f"Provide a concise, 3-4 word description for the following code:\n{code_text}"
    name_result = gen(name_prompt, max_length=20, do_sample=False)[0]['generated_text']
    code_name = name_result.strip().split('\n')[0]

    # Prompts for each type
    prompts = {
        "error": f"Find errors in the following code and explain:\n{code_text}",
        "enhance": f"Enhance the following code to make it more robust and readable:\n{code_text}",
        "optimize": f"Optimize the following code for performance and clarity:\n{code_text}"
    }

    # Generate all 3 responses
    error_response = gen(prompts["error"], max_length=1024, do_sample=True)[0]['generated_text']
    enhance_response = gen(prompts["enhance"], max_length=1024, do_sample=True)[0]['generated_text']
    optimize_response = gen(prompts["optimize"], max_length=1024, do_sample=True)[0]['generated_text']

    return (code_name,error_response,enhance_response,optimize_response)