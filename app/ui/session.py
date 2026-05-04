import uuid
from fastapi import Request, Response

# In-memory session store (simple for prototype/tests)
_sessions: dict[str, int] = {}


def _get_user_id(request: Request) -> int | None:
    token = request.cookies.get("tf_session")
    return _sessions.get(token) if token else None


def _create_session(response: Response, user_id: int) -> None:
    token = str(uuid.uuid4())
    _sessions[token] = user_id
    response.set_cookie("tf_session", token, httponly=True, samesite="lax", max_age=86400 * 7)


def _destroy_session(request: Request, response: Response) -> None:
    token = request.cookies.get("tf_session")
    if token:
        _sessions.pop(token, None)
    response.delete_cookie("tf_session")
