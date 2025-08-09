# api/config_log.py
import logging, time, uuid
from pythonjsonlogger import jsonlogger
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

def configure_logging():
    """
    Configura logs JSON para stdout (Render captura automaticamente).
    """
    
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    for h in list(root.handlers):
        root.removeHandler(h)
    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    root.addHandler(handler)
    for name in ["uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"]:
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

logger = logging.getLogger("api")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Loga uma linha em JSON por requisição
    """
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        path_template = request.scope.get("route").path if request.scope.get("route") else request.url.path

        try:
            response: Response = await call_next(request)
            return response
        finally:
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.info(
                "http_request",
                extra={
                    "event": "http_request",
                    "request_id": req_id,
                    "method": request.method,
                    "path": path_template,
                    "status_code": getattr(locals().get("response", None), "status_code", None),
                    "latency_ms": latency_ms,
                    "client_ip": request.client.host if request.client else None,
                    "user_agent": request.headers.get("user-agent"),
                },
            )
