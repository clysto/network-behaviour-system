from nicegui import ui
from analyse.main import used_by_hour
from data import load_dataset


class ClusterPage:
    group = "所有"
    chart = None

    def get_chart(self, dataset):
        r = used_by_hour(dataset)
        chart = {
            "title": False,
            "chart": {"type": "column"},
            "xAxis": {"categories": []},
            "yAxis": {"title": {"text": "人数"}},
            "series": [{"name": self.group, "data": r.to_list()}],
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
            ).props("filled").bind_value(self, "group")
            ui.button("分析上网时间分布", on_click=self.build_chart).props("push").classes(
                "full-width mt-4"
            )
