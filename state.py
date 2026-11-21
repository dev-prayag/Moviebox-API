import asyncio
import httpx
from fastapi import HTTPException
from config import REQUEST_TIMEOUT

client: httpx.AsyncClient | None = None
bearer_tokens: dict[str, tuple[str, float]] = {}
bearer_lock = asyncio.Lock()
domain_cache: dict = {"value": None, "expires": 0.0}
home_cache: dict = {}
stream_cache: dict = {}
probe_task: asyncio.Task | None = None


def require_client() -> httpx.AsyncClient:
    global client
    if client is None or client.is_closed:
        client = httpx.AsyncClient(
            timeout=httpx.Timeout(REQUEST_TIMEOUT, connect=10.0),
            limits=httpx.Limits(
                max_connections=50,
                max_keepalive_connections=20,
                keepalive_expiry=30.0,
            ),
            follow_redirects=True,
        )
    return client
