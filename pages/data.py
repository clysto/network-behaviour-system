from data import load_dataset
from nicegui import ui


class DatasetPage:
    current_page = 1

    def change_page(self, page):
        if page < 1:
            return
        self.current_page = page
        data = load_dataset((self.current_page - 1) * 100, limit=100).to_dict("records")
        self.table.rows.clear()
        self.table.rows.extend(data)
        self.table.update()

    def build(self):
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
        ]
        data = load_dataset((self.current_page - 1) * 100, limit=100).to_dict("records")
        with ui.element("div").classes("p-4"):
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
                ui.button("导入数据").props("push")
            self.table = ui.table(columns=columns, rows=data, title="数据集")
