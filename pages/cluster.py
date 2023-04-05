from nicegui import ui


class ClusterPage:
    type = "K Means"

    def build(self):
        with ui.element("div").classes("p-4 max-w-[800px] mx-auto"):
            ui.select(
                [
                    "K Means",
                ],
                label="聚类方法",
            ).props(
                "filled"
            ).bind_value(self, "type")
            ui.input(label="K 值").classes("mt-4").props("filled")
            ui.select(
                [
                    "时间",
                    "异常程度",
                ],
                label="聚类属性",
            ).props(
                "filled"
            ).classes("mt-4")
