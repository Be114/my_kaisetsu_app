# config.py

# Configuration for script_generator.py

# Model name for OpenRouter API
# Example: "google/gemini-1.5-flash-latest", "google/gemini-pro", "mistralai/mistral-7b-instruct"
# The user previously had "google/gemini-2.5-pro-preview"
MODEL_NAME = "google/gemini-2.5-pro-preview"

# Input and Output file paths
# These are assumed to be in the same directory as the script.
INPUT_FILE_PATH = "input.txt"
OUTPUT_SCRIPT_FILE = "generated_script_openrouter.md"

# Default title if not provided for the script generation
DEFAULT_TITLE_PREFIX = "私の最初の解説"
