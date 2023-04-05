from nicegui import ui
from analyse.main import used_by_hour, used_by_group
from data import load_dataset


class HoursPage:
    group = "所有"
    chart = None
    chart2 = None

    def get_chart(self, dataset):
        r = used_by_hour(dataset)
        chart = {
            "title": False,
            "chart": {"type": "column"},
            "xAxis": {"categories": []},
            "yAxis": {"title": {"text": "人数"}},
            "series": [{"name": self.group, "data": r}],
        }
        for h in range(24):
            chart["xAxis"]["categories"].append("{:02d}:00".format(h))
        return chart

    def build_chart(self):
        dataset = load_dataset(limit=-1)
        if self.group != "所有":
            dataset = dataset[dataset["group"] == self.group]
        if self.chart is None:
            self.chart = ui.chart(self.get_chart(dataset)).classes("w-full h-128 mt-16")
        else:
            self.chart._props["options"] = self.get_chart(dataset)
            self.chart.update()

    def build_chart2(self):
        if self.chart2 is None:
            dataset = load_dataset(limit=-1)
            r = used_by_group(dataset)
            r = list(
                map(
                    lambda x: {"name": x[1], "y": x[0]},
                    list(zip(r.to_list(), r.index)),
                )
            )
            chart = {
                "title": False,
                "chart": {"type": "pie"},
                "accessibility": {"point": {"valueSuffix": "%"}},
                "series": [{"name": "部门", "data": r}],
            }
            self.chart2 = ui.chart(chart).classes("w-full h-128 mt-16")

    def build(self):
        with ui.tabs().classes("bg-primary text-white") as tabs:
            ui.tab("每小时上网人数")
            ui.tab("各部门上网人数")
        with ui.element("div").classes("p-4 max-w-[800px] mx-auto"):
            with ui.tab_panels(tabs, value="每小时上网人数"):
                with ui.tab_panel("每小时上网人数"):
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
                    ).props("filled").bind_value(self, "group")
                    ui.button("分析上网时间分布", on_click=self.build_chart).props(
                        "push"
                    ).classes("full-width mt-4")
                with ui.tab_panel("各部门上网人数"):
                    ui.button("分析上网部门分布", on_click=self.build_chart2).props(
                        "push"
                    ).classes("full-width")
