import logging
import uuid
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Set up logging
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # Log the request
        body = await request.body()
        logging.info(f"[{request_id}] --> {request.method} {request.url} | Body: {body.decode('utf-8', errors='ignore')}")

        response: Response = await call_next(request)
        process_time = (time.time() - start_time) * 1000

        # Log the response
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        response.body_iterator = iter([response_body])

        logging.info(f"[{request_id}] <-- {response.status_code} | {len(response_body)} bytes | {process_time:.2f} ms")
        return response
