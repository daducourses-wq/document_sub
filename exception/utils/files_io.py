from __future__ import annotations
import re
import uuid
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import uuid
from typing import Iterable, List
from logger.custom_logger import CustomLogger
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import DocumentPortalException
log = CustomLogger().get_logger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

# ----------------------------- #