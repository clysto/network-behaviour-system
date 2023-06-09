from typing import Awaitable, Callable

from nicegui import background_tasks, ui
from nicegui.dependencies import register_component
from utils import is_authenticated, get_item, set_item

register_component("router_frame", __file__, "router_frame.js")

NEED_LOGIN = ["/dataset", "/hours", "/users", "/cluster"]


class Router:
    def __init__(self) -> None:
        self.routes = {}
        self.content: ui.element = None

    def add(self, path: str):
        def decorator(func: Callable):
            self.routes[path] = ("func", func)
            return func

        return decorator

    def add_page_class(self, path, page):
        self.routes[path] = ("class", page)

    def open(self, target: str):
        async def build():
            with self.content:
                path = target
                builder = self.routes[target]
                session_id = await get_item("id")
                if not is_authenticated(session_id) and path in NEED_LOGIN:
                    path = "/login"
                    builder = self.routes[path]
                await ui.run_javascript(
                    f'history.pushState({{page: "{path}"}}, "", "{path}")',
                    respond=False,
                )
                if builder[0] == "func":
                    result = builder[1]()
                else:
                    result = builder[1]().build()

                if isinstance(result, Awaitable):
                    await result

        self.content.clear()
        background_tasks.create(build())

    def frame(self) -> ui.element:
        self.content = ui.element("router_frame").on(
            "open", lambda msg: self.open(msg["args"])
        )
        return self.content
