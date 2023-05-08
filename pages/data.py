from data import load_dataset
from nicegui import ui
from utils import get_item
from db import session_info, db
import numpy as np


class DatasetPage:
    current_page = 1
    url_type = "娱乐"
    hour = 0

    def change_page(self, page):
        if page < 1:
            return
        self.current_page = page
        if self.user["manage"] != "所有":
            data = load_dataset(
                (self.current_page - 1) * 100, limit=100, group=self.user["manage"]
            )
        else:
            data = load_dataset((self.current_page - 1) * 100, limit=100)
        data["time"] = data["time"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
        self.table.rows.clear()
        self.table.rows.extend(data.to_dict("records"))
        self.table.update()

    async def build(self):
        self.session_id = await get_item("id")
        self.user = session_info[self.session_id]["user"]
        columns = [
            {"name": "id", "label": "Id", "field": "id"},
            {"name": "account", "label": "Account", "field": "account"},
            {"name": "group", "label": "Group", "field": "group"},
            {"name": "ip", "label": "IP", "field": "IP"},
            {"name": "url", "label": "URL", "field": "url"},
            {"name": "port", "label": "Port", "field": "port"},
            {"name": "vlan", "label": "VLAN", "field": "vlan"},
            {"name": "switchIP", "label": "Switch IP", "field": "switchIP"},
            {"name": "time", "label": "Time", "field": "time"},
            {"name": "ret", "label": "Ret", "field": "ret"},
            {"name": "duration", "label": "Duration", "field": "duration"},
        ]
        # if self.user["manage"] != "所有":
        #     data = load_dataset(
        #         (self.current_page - 1) * 100, limit=100, group=self.user["manage"]
        #     ).to_dict("records")
        # else:
        #     data = load_dataset((self.current_page - 1) * 100, limit=100).to_dict(
        #         "records"
        #     )
        with ui.tabs().classes("bg-primary text-white") as tabs:
            ui.tab("全部数据")
            ui.tab("上网预警")
        with ui.tab_panels(tabs, value="上网预警"):
            with ui.tab_panel("全部数据"):
                with ui.row():
                    with ui.element("q-btn-group").classes("mb-4"):
                        ui.button(
                            "上一页",
                            on_click=lambda _: self.change_page(self.current_page - 1),
                        ).props("push")
                        ui.button(
                            "下一页",
                            on_click=lambda _: self.change_page(self.current_page + 1),
                        ).props("push")
                    ui.element("div").classes("flex-1")
                self.table = ui.table(columns=columns, rows=[], title="数据集").props(
                    "dense"
                )
                self.change_page(1)
            with ui.tab_panel("上网预警"):
                with ui.element("div").classes(
                    "mx-auto w-[500px] rounded-2xl shadow p-4 bg-[#f5f5f5]"
                ):
                    url_types = ["娱乐", "视频", "学习", "社交", "网课", "购物", "游戏"]
                    ui.select(options=url_types, label="上网类型").bind_value(
                        self, "url_type"
                    ).props("outlined")
                    ui.select(options=list(np.arange(0, 24)), label="上网时段").props(
                        "outlined"
                    ).classes("mt-4").bind_value(self, "hour")
                    ui.button("查看预警名单", on_click=self.show_alert).props(
                        "push color=amber-10"
                    ).classes("full-width mt-8")
                ui.button("一键发送预警通知邮件", on_click=self.send_email).classes("mt-4").props(
                    "push"
                )
                self.table2 = (
                    ui.table(columns=columns, rows=[], title="预警名单")
                    .props("dense")
                    .classes("mt-4")
                )

    def send_email(self):
        ui.notify("邮件已发送!")

    def show_alert(self):
        # rows = db.dataset.find(
        #     {"url": self.url_type}
        # ).limit(100)
        mm = {"url": self.url_type, "hour": int(self.hour)}
        if self.user["manage"] != "所有":
            mm["group"] = self.user["manage"]
        rows = db.dataset.aggregate(
            [
                {
                    "$project": {
                        "id": 1,
                        "account": 1,
                        "group": 1,
                        "ip": 1,
                        "url": 1,
                        "port": 1,
                        "vlan": 1,
                        "switchIP": 1,
                        "time": 1,
                        "ret": 1,
                        "duration": 1,
                        "hour": {"$hour": "$time"},
                    }
                },
                {"$match": mm},
                {"$limit": 100},
            ]
        )
        self.table2.rows.clear()
        self.table2.rows.extend(rows)
        self.table2.update()
