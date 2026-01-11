import os
import random
import logging
from dotenv import load_dotenv
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InferenceEngine:
    def __init__(self, mode="auto", model_path="lora_model", base_model="mistral"):
        """
        Initialize inference engine.
        mode: 'auto' (Priority: Local Adapter -> Groq -> Ollama -> Mock)
        """
        self.mode = mode
        self.model_path = model_path
        self.base_model = base_model
        self.model = None
        self.tokenizer = None
        
        # Detected active backend
        self.active_backend = None
        
        # Load environment variables
        load_dotenv()
        
        self._load_model()

    def _load_model(self):
        # 1. Try Local Adapter (Unsloth)
        if self.mode in ["auto", "local"]:
            if os.path.exists(self.model_path):
                try:
                    from unsloth import FastLanguageModel
                    logger.info(f"Loading local adapter from {self.model_path}...")
                    self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                        model_name=self.model_path,
                        max_seq_length=2048,
                        dtype=None,
                        load_in_4bit=True
                    )
                    FastLanguageModel.for_inference(self.model)
                    self.active_backend = "local_adapter"
                    logger.info("Local adapter loaded successfully.")
                    return
                except ImportError:
                    logger.warning("Unsloth not installed or import failed.")
                except Exception as e:
                    logger.error(f"Failed to load local adapter: {e}")
            else:
                logger.warning(f"Local model path {self.model_path} does not exist.")


        if self.mode in ["auto", "groq"] and self.active_backend is None:
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                try:
                    self.client = Groq(api_key=api_key)
                    # Verify connection with a dummy call (optional, but good practice)
                    self.client.models.list() 
                    self.active_backend = "groq"
                    logger.info("Using Groq backend.")
                    return
                except Exception as e:
                    logger.warning(f"Groq initialization failed: {e}")
            else:
                logger.warning("GROQ_API_KEY not found in environment.")

        # 3. Try Ollama (Base Model)
        if self.mode in ["auto", "ollama"] and self.active_backend is None:
            try:
                import ollama
                # Check connection
                ollama.list()
                self.active_backend = "ollama"
                logger.info(f"Using Ollama backend with model: {self.base_model}")
                return
            except Exception as e:
                logger.warning(f"Ollama backend not available: {e}")

        # 4. Fallback to Mock
        self.active_backend = "mock"
        logger.warning("Falling back to Mock mode.")

    def generate(self, prompt, temperature=0.7):
        if self.active_backend == "local_adapter":
            return self._generate_local(prompt, temperature)
        elif self.active_backend == "groq":
            return self._generate_groq(prompt, temperature)
        elif self.active_backend == "ollama":
            return self._generate_ollama(prompt, temperature)
        else:
            return self._generate_mock(prompt)

    def _generate_local(self, prompt, temperature):
        alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
"""
        inputs = self.tokenizer(
            [alpaca_prompt.format(prompt, "", "")], 
            return_tensors="pt"
        ).to("cuda")
        
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=128, 
            temperature=temperature
        )
        # Decode and strip prompt
        response = self.tokenizer.batch_decode(outputs)[0]
        # Basic cleanup - split by response tag
        if "### Response:" in response:
            return response.split("### Response:")[-1].strip().replace("<|end_of_text|>", "")
        return response

    def _generate_groq(self, prompt, temperature):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful expert assistant trained on Polars documentation."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=os.getenv("MODEL_NAME", "llama-3.1-8b-instant"),
                temperature=temperature,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            return f"Error generating response with Groq: {str(e)}"

    def _generate_ollama(self, prompt, temperature):
        import ollama
        system_prompt = "You are a helpful expert assistant trained on Polars documentation."
        response = ollama.chat(
            model=self.base_model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            options={'temperature': temperature}
        )
        return response['message']['content']

    def _generate_mock(self, prompt):
        import time
        time.sleep(1)
        responses = [
             "Based on the Polars documentation, you can use `pl.scan_csv()` for lazy loading.",
             "The `filter` context is highly optimized in Polars.",
             "To join two DataFrames, use the `join` method."
        ]
        return f"[MOCK] {random.choice(responses)}"

# Singleton instance (optional, but good for caching model load)
engine = InferenceEngine()
