import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
@@ -14,7 +14,6 @@ class DocumentAnalyzer:
   Automatically logs all actions and supports session-based organization.
   """
def __init__(self):
        self.log = CustomLogger().get_logger(__name__)
try:
self.loader=ModelLoader()
self.llm=self.loader.load_llm()
@@ -25,11 +24,11 @@ def __init__(self):

self.prompt = PROMPT_REGISTRY["document_analysis"]

            self.log.info("DocumentAnalyzer initialized successfully")
            log.info("DocumentAnalyzer initialized successfully")


except Exception as e:
            self.log.error(f"Error initializing DocumentAnalyzer: {e}")
            log.error(f"Error initializing DocumentAnalyzer: {e}")
raise DocumentPortalException("Error in DocumentAnalyzer initialization", sys)


@@ -41,19 +40,19 @@ def analyze_document(self, document_text:str)-> dict:
try:
chain = self.prompt | self.llm | self.fixing_parser

            self.log.info("Meta-data analysis chain initialized")
            log.info("Meta-data analysis chain initialized")

response = chain.invoke({
"format_instructions": self.parser.get_format_instructions(),
"document_text": document_text
})

            self.log.info("Metadata extraction successful", keys=list(response.keys()))
            log.info("Metadata extraction successful", keys=list(response.keys()))

return response

except Exception as e:
            self.log.error("Metadata analysis failed", error=str(e))
            log.error("Metadata analysis failed", error=str(e))
raise DocumentPortalException("Metadata extraction failed",sys)

