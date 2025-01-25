import json
from register import register_ngo
from generate import write_letter
from regenerate import regenerate_letter
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

config_file_path = r"configs/register_configs.json"


# Load the configuration file
try:
    with open(config_file_path, 'r') as file:
        config_data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file at {config_file_path} was not found.")
except json.JSONDecodeError:
    print("Error: The file contains invalid JSON.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Store NGO details
ngo_data = register_ngo(config_data)
print(ngo_data)


# Generate proposal letters
# letter = write_letter(config_data)
# print(letter)