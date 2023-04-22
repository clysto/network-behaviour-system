from nicegui import ui
from db import db


class UsersPage:
    username = ""
    password = ""
    email = ""
    manage = "所有"
    delete_user = None

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
        self.select1.options.clear()
        self.select1.options.extend(list(map(lambda x: x["username"], users)))
        self.select1.update()
        self.table.update()

    def remove_user(self):
        db.users.delete_one({"username": self.delete_user})
        self.load_users()
        self.dialog1.close()

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
        self.dialog1 = ui.dialog()
        with self.dialog1, ui.card().classes("w-[400px]"):
            self.select1 = (
                ui.select(
                    list(map(lambda x: x["username"], users)),
                    label="用户名",
                )
                .props("outlined")
                .bind_value(self, "delete_user")
                .classes("full-width")
            )
            ui.button("取消", on_click=self.dialog1.close).classes("full-width")
            ui.button("确定", on_click=self.remove_user).classes("full-width")
        with self.container:
            ui.button("新建用户", on_click=self.dialog.open).props("push")
            ui.button("删除用户", on_click=self.dialog1.open).props("push").classes("ml-2")
            self.table = ui.table(columns=columns, rows=users).props("grid")
