import json
import os
try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

class LLMEngine:
    def __init__(self, config):
        self.config = config
        self.model_path = config.get("model_path", "")
        self.context_size = config.get("context_size", 2048)
        self.llm = None
        self._load_model()

    def _load_model(self):
        if Llama and os.path.exists(self.model_path):
            print(f"Loading LLM from {self.model_path}...")
            try:
                self.llm = Llama(
                    model_path=self.model_path,
                    n_ctx=self.context_size,
                    verbose=False
                )
                print("LLM loaded.")
            except Exception as e:
                print(f"Failed to load LLM: {e}")
        else:
            print(f"LLM model not found at {self.model_path} or llama-cpp-python not installed.")

    def process_command(self, text):
        """
        Process user text and return a structured JSON command.
        """
        if not self.llm:
            # Mock response for testing without model
            print("LLM not loaded. returning mock response.")
            if "chrome" in text.lower():
                return {"intent": "open_application", "application": "Google Chrome"}
            return {"intent": "unknown", "text": text}

        prompt = self._construct_prompt(text)

        output = self.llm(
            prompt,
            max_tokens=128,
            stop=["User:", "\n"],
            echo=False
        )

        response_text = output['choices'][0]['text'].strip()
        return self._parse_json(response_text)

    def _construct_prompt(self, text):
        return f"""You are a helpful assistant named Jarvis. Output valid JSON only.
User: {text}
Jarvis:"""

    def _parse_json(self, text):
        try:
            # simple cleanup if needed
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            return json.loads(text)
        except json.JSONDecodeError:
            return {"intent": "chat", "response": text}
