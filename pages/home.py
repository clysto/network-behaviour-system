from config import router
from nicegui import ui


@router.add("/")
async def home_page():
    with ui.column().style("height: calc(100vh - 68px - 53px)").classes(
        "bg-[#3874c8] justify-center items-center"
    ):

        def on_click():
            router.open("/login")

        ui.image("/public/logo.svg").classes("max-w-[400px]")
        ui.label("欢迎来到高校学生上网行为分析系统！").classes("text-3xl font-bold text-white")
        with ui.row():
            ui.button("现在登录", on_click=on_click).props(
                "push size=large color=white"
            ).classes("text-black")
