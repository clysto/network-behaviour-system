from nicegui import ui
from db import db


class UsersPage:
    username = ""
    password = ""
    email = ""
    manage = "所有"

    def add_user(self):
        db.users.insert_one(
            {
                "username": self.username,
                "password": self.password,
                "email": self.email,
                "manage": self.manage,
            }
        )
        self.load_users()
        self.dialog.close()

    def load_users(self):
        users = list(db.users.find())
        self.table.rows.clear()
        self.table.rows.extend(users)
        self.table.update()

    def build(self):
        columns = [
            {"name": "username", "label": "用户名", "field": "username"},
            {"name": "email", "label": "邮箱", "field": "email"},
            {"name": "manage", "label": "管理权限", "field": "manage"},
        ]
        self.container = ui.element("div").classes("p-4")
        users = list(db.users.find())
        self.dialog = ui.dialog()
        with self.dialog, ui.card().classes("w-[400px]"):
            ui.input("用户名").bind_value(self, "username").classes("full-width").props(
                "outlined"
            )
            ui.input("邮箱").bind_value(self, "email").classes("full-width").props(
                "outlined"
            )
            ui.input("密码").bind_value(self, "password").classes("full-width").props(
                "outlined"
            )
            ui.select(
                [
                    "所有",
                    "大一",
                    "大二",
                    "大三",
                    "大四",
                    "后勤",
                    "办公室",
                    "学工处",
                ],
                label="部门",
            ).props("outlined").bind_value(self, "manage").classes("full-width")
            ui.button("取消", on_click=self.dialog.close).classes("full-width")
            ui.button("确定", on_click=self.add_user).classes("full-width")
        with self.container:
            ui.button("新建用户", on_click=self.dialog.open).props("push")
            self.table = ui.table(columns=columns, rows=users).props("grid")
