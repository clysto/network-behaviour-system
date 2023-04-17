from db import session_info
from fastapi import Request


def is_authenticated(request: Request) -> bool:
    return session_info.get(request.session.get("id"), {}).get("authenticated", False)
