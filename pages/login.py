from config import router
from nicegui import ui


@router.add("/login")
def login_page():
    with ui.element("div").classes("max-w-[500px] mx-auto p-4"):
        ui.label("登录").classes("text-3xl font-bold text-center mb-4")
        ui.input("账号").props("outlined").classes("mb-4")
        ui.input("密码").props("type=password outlined")
        ui.button("登录").classes("full-width mt-16 mb-4").props("push")
        ui.button("取消").classes("full-width").props("push")
