from nicegui import ui
from config import router
from db import db
from fastapi import Request
import uuid


class LoginPage:
    username = ""
    password = ""

    def login(self):
        user = db["users"].find_one({"username": self.username})
        if user is None:
            ui.notify("不存在该用户！", type="warning", position="top")
            return
        if user["password"] == self.password:
            ui.notify("登录成功！", position="top")
            router.open("/dataset")
        else:
            ui.notify("密码不正确！", type="warning", position="top")

    def build(self):
        with ui.element("div").classes(
            "max-w-[500px] mx-auto p-4 mt-4 shadow-xl rounded-xl"
        ):
            ui.label("登录").classes("text-3xl font-bold text-center mb-4")
            ui.input("账号").props("outlined").classes("mb-4").bind_value(
                self, "username"
            )
            ui.input("密码").props("type=password outlined").bind_value(self, "password")
            ui.button("登录", on_click=self.login).classes("full-width mt-16 mb-4").props(
                "push"
            )
            ui.button("取消").classes("full-width").props("push")
