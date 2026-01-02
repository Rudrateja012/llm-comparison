from concurrent.futures import ThreadPoolExecutor
from models.chatgpt_model import chatgpt_response
from models.geminiai_model import gemini_response
from models.llama_model import llama_response

def run_parallel_responses(prompt: str) -> dict:
    results = {}

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            'chatgpt': executor.submit(chatgpt_response, prompt),
            'gemini': executor.submit(gemini_response, prompt),
            'llama': executor.submit(llama_response, prompt),
        }
        for model, future in futures.items():
            try:
                results[model] = future.result()
            except Exception as e:
                results[model] = f"Error: {str(e)}" 
    return results
            