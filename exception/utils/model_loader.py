
import os
import sys
from dotenv import load_dotenv
from utils.config_loader import load_config
from .config_loader import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
#from langchain_openai import ChatOpenAI
from logger.custom_logger import CustomLogger
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import DocumentPortalException
log = CustomLogger().get_logger(__name__)

class ModelLoader:

@@ -59,8 +58,8 @@
llm_block = self.config["llm"]

log.info("Loading LLM...")
        
        provider_key = os.getenv("LLM_PROVIDER", "groq")  # Default groq

        provider_key = os.getenv("LLM_PROVIDER", "google")  # Default google
if provider_key not in llm_block:
log.error("LLM provider not found in config", provider_key=provider_key)
raise ValueError(f"Provider '{provider_key}' not found in config")