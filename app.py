from nicegui import ui, app, Client
from fastapi import Request
import uuid
from utils import set_item
from db import session_info

from pages import *
from config import router
from starlette.middleware.sessions import SessionMiddleware

router.add_page_class("/dataset", DatasetPage)
router.add_page_class("/hours", HoursPage)
router.add_page_class("/cluster", ClusterPage)
router.add_page_class("/login", LoginPage)
router.add_page_class("/users", UsersPage)

app.add_static_files("/public", "public")
app.add_middleware(SessionMiddleware, secret_key="9a218947-b6cd-4010-a4b4-2fd4b4eac889")


@ui.page("/")
@ui.page("/{_:path}")
async def main(client: Client, request: Request):
    if "id" not in request.session:
        request.session["id"] = str(uuid.uuid4())
    await client.connected()
    await set_item("id", request.session["id"])
    try:
        user = session_info[request.session["id"]]["user"]
    except Exception:
        user = None
    client.content.classes("p-0")
    ui.colors(primary="#3874c8")
    with ui.header(elevated=True).style("background-color: #3874c8").classes(
        "items-center justify-between"
    ):
        with ui.row().classes("display-flex items-center"):
            ui.icon("school").classes("text-2xl")
            ui.label("高校学生上网行为分析系统").classes("font-bold text-xl")
        with ui.row():
            ui.button("首页", on_click=lambda: router.open("/")).classes(
                "font-bold"
            ).props("flat color=white")
            ui.button("数据集", on_click=lambda: router.open("/dataset")).classes(
                "font-bold"
            ).props("flat color=white")
            ui.button("上网时间分析", on_click=lambda: router.open("/hours")).classes(
                "font-bold"
            ).props("flat color=white")
            ui.button("聚类分析", on_click=lambda: router.open("/cluster")).classes(
                "font-bold"
            ).props("flat color=white")
            if user is not None and user["manage"] == "所有":
                ui.button("用户管理", on_click=lambda: router.open("/users")).classes(
                    "font-bold"
                ).props("flat color=white")
            ui.button("登录", on_click=lambda: router.open("/login")).classes(
                "font-bold"
            ).props("flat color=white")
    with ui.footer().style("background-color: #3874c8"):
        ui.label("v1.0").classes("text-white-100")
    router.frame().classes("w-full")


ui.run(title="高校学生上网行为分析系统")
