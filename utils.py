from db import session_info
import json
from nicegui import ui


def is_authenticated(session_id) -> bool:
    return session_info.get(session_id, {}).get("authenticated", False)


async def set_item(key, data):
    if not isinstance(data, str):
        data = json.dumps(data)
    await ui.run_javascript(
        f"""
    window.localStorage.setItem('{key}', `{data}`)
    """,
        respond=False,
    )


async def get_item(key):
    result = await ui.run_javascript(
        f"""
    window.localStorage.getItem('{key}')
    """
    )
    try:
        return json.loads(result)
    except:
        return result
