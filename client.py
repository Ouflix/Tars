import requests
import json

SERVER_URL = "http://192.168.0.117:5000/ai_response"

def get_ai_response(prompt):
    payload = {"prompt": prompt}
    try:
        response = requests.post(SERVER_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("[CLIENT] Error calling AI function:", e)
        return {}

def process_server_response(data):
    """
    Processes the server's response.
    If a function call is included, it prints the function name and arguments
    instead of executing it.
    """
    if not data:
        print("[CLIENT] No response data received.")
        return

    # Check if the response includes a function call
    if "function_call" in data:
        func_call = data["function_call"]
        func_name = func_call.get("name")
        arguments_str = func_call.get("arguments", "{}")
        try:
            # Parse the arguments (assuming it's a JSON string)
            args = json.loads(arguments_str) if isinstance(arguments_str, str) else arguments_str
        except Exception as e:
            print("[CLIENT] Error parsing arguments:", e)
            args = {}
        # Instead of calling the function, simply print what would be called.
        print(f"[CLIENT] Would call function '{func_name}' with arguments: {args}")
    elif "response" in data:
        # If there's a plain text response, just print it.
        print("[CLIENT] AI response:", data["response"])
    else:
        print("[CLIENT] Unexpected response:", data)

if __name__ == "__main__":
    while True:
        prompt = input("Enter prompt (or 'close' to exit): ")
        if prompt.lower() == "close":
            break
        response_data = get_ai_response(prompt)
        process_server_response(response_data)
