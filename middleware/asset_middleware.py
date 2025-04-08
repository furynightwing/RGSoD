import re
import base64
from pathlib import Path
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad
import logging

logger = logging.getLogger(__name__)

class AssetMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, config):
        super().__init__(app)
        self.config = config["AssetServer"]
        self.encrypt_key = bytes.fromhex(self.config["AutoEncryptKey"].replace("-", ""))
        self.encrypt_regex = re.compile(self.config["AutoEncryptRegexp"])
        self.assets_root = Path("assets")  # Adjust this if your asset folder is elsewhere

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Check if the requested path matches encryption regex
        if self.encrypt_regex.search(path):
            file_path = self.assets_root / path.lstrip("/")
            if file_path.exists():
                try:
                    with open(file_path, "rb") as f:
                        plain_data = f.read()

                    cipher = DES3.new(self.encrypt_key, DES3.MODE_ECB)
                    encrypted = cipher.encrypt(pad(plain_data, DES3.block_size))
                    encoded = base64.b64encode(encrypted)

                    logger.info(f"Encrypted asset served: {file_path}")
                    return Response(content=encoded, media_type="text/plain")
                except Exception as e:
                    logger.error(f"Encryption failed for {path}: {e}")
                    return Response(status_code=500, content="Encryption failed")
            else:
                logger.warning(f"Asset not found: {file_path}")
                return Response(status_code=404, content="File not found")

        # Proceed normally if no encryption is needed
        return await call_next(request)
