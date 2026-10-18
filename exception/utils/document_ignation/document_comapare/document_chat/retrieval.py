import sys
import os
from operator import itemgetter
from typing import List, Optional, Dict, Any

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS

from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger
from logger import GLOBAL_LOGGER as log
from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType

@@ -27,7 +27,6 @@

def __init__(self, session_id: Optional[str], retriever=None):
try:
            self.log = CustomLogger().get_logger(__name__)
self.session_id = session_id

# Load LLM and prompts once
@@ -45,9 +44,9 @@
if self.retriever is not None:
self._build_lcel_chain()

            self.log.info("ConversationalRAG initialized", session_id=self.session_id)
            log.info("ConversationalRAG initialized", session_id=self.session_id)
except Exception as e:
            self.log.error("Failed to initialize ConversationalRAG", error=str(e))
            log.error("Failed to initialize ConversationalRAG", error=str(e))
raise DocumentPortalException("Initialization error in ConversationalRAG", sys)

# ---------- Public API ----------
@@ -83,7 +82,7 @@
)
self._build_lcel_chain()

            self.log.info(
            log.info(
"FAISS retriever loaded successfully",
index_path=index_path,
index_name=index_name,
@@ -93,7 +92,7 @@
return self.retriever

except Exception as e:
            self.log.error("Failed to load retriever from FAISS", error=str(e))
            log.error("Failed to load retriever from FAISS", error=str(e))
raise DocumentPortalException("Loading error in ConversationalRAG", sys)

def invoke(self, user_input: str, chat_history: Optional[List[BaseMessage]] = None) -> str:
@@ -107,19 +106,19 @@
payload = {"input": user_input, "chat_history": chat_history}
answer = self.chain.invoke(payload)
if not answer:
                self.log.warning(
                log.warning(
"No answer generated", user_input=user_input, session_id=self.session_id
)
return "no answer generated."
            self.log.info(
            log.info(
"Chain invoked successfully",
session_id=self.session_id,
user_input=user_input,
answer_preview=str(answer)[:150],
)
return answer
except Exception as e:
            self.log.error("Failed to invoke ConversationalRAG", error=str(e))
            log.error("Failed to invoke ConversationalRAG", error=str(e))
raise DocumentPortalException("Invocation error in ConversationalRAG", sys)

# ---------- Internals ----------
@@ -129,10 +128,10 @@
llm = ModelLoader().load_llm()
if not llm:
raise ValueError("LLM could not be loaded")
            self.log.info("LLM loaded successfully", session_id=self.session_id)
            log.info("LLM loaded successfully", session_id=self.session_id)
return llm
except Exception as e:
            self.log.error("Failed to load LLM", error=str(e))
            log.error("Failed to load LLM", error=str(e))
raise DocumentPortalException("LLM loading error in ConversationalRAG", sys)

@staticmethod
@@ -167,7 +166,7 @@
| StrOutputParser()
)

            self.log.info("LCEL graph built successfully", session_id=self.session_id)
            log.info("LCEL graph built successfully", session_id=self.session_id)
except Exception as e:
            self.log.error("Failed to build LCEL chain", error=str(e), session_id=self.session_id)
            log.error("Failed to build LCEL chain", error=str(e), session_id=self.session_id)
raise DocumentPortalException("Failed to build LCEL chain", sys)