from nicegui import ui


class ClusterPage:
    def build(self):
        with ui.element("div").classes("p-4 max-w-[800px] mx-auto"):
            ui.select(
                [
                    "所有",
                    "人事行政中心",
                    "业务创新中心",
                    "市场战略发展中心",
                    "政企事业部",
                    "研发中心",
                    "渠道生态合作事业部",
                    "通用市场部",
                ],
                label="部门",
                value="所有",
            ).props("filled")
            ui.button("开始 KNN 聚类").props("push").classes("full-width mt-4")
            chart = ui.chart(
                {
                    "title": False,
                    "chart": {"type": "column"},
                    "xAxis": {"categories": ["A", "B"]},
                    "series": [
                        {"name": "Alpha", "data": [0.1, 0.2]},
                        {"name": "Beta", "data": [0.3, 0.4]},
                    ],
                }
            ).classes("w-full h-64 mt-4")
