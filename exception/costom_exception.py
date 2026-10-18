
import sys
import traceback
from typing import Optional, cast
@@ -53,15 +52,15 @@ def __repr__(self):
return f"DocumentPortalException(file={self.file_name!r}, line={self.lineno}, message={self.error_message!r})"


if __name__ == "__main__":
    # Demo-1: generic exception -> wrap
    try:
        a = 1 / 0
    except Exception as e:
        raise DocumentPortalException("Division failed", e) from e
if __name__ == "__main__":
          Demo-1: generic exception -> wrap
#     try:
#         a = 1 / 0
#     except Exception as e:
#         raise DocumentPortalException("Division failed", e) from e

    # Demo-2: still supports sys (old pattern)
    # try:
    #     a = int("abc")
    # except Exception as e:
    #     raise DocumentPortalException(e, sys)
#     # Demo-2: still supports sys (old pattern)
#     # try:
#     #     a = int("abc")
#     # except Exception as e:
#     #     raise DocumentPortalException(e, sys)