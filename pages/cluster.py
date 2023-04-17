from nicegui import ui
from config import task_manager
from analyse.main import k_means
from data import load_dataset
from matplotlib.figure import Figure
import io
import base64


class ClusterPage:
    type = "K Means ++"
    plot = None
    k = "2"
    cols = "hour"


    def cluster(self):
        if self.k.isdigit():
            dataset = load_dataset(limit=-1)
            return k_means(dataset, self.cols, k=int(self.k))
        else:
            with self.container:
                ui.notify("K值必须为整数", type="warning", position="top")

    def button_click(self):
        self.button.props("loading")
        task_manager.add_task(self.cluster, self.render_chart)

    def render_chart(self, data):
        if data is None:
            self.button.props("loading=false")
            return
        fig = Figure(dpi=300, figsize=(10, 4))
        ax = fig.subplots()
        ax.scatter(data[self.cols], data["id"], c=data["cluster"], cmap="viridis")
        ax.set_xlabel(self.cols)
        ax.set_ylabel("ID")
        buf = io.BytesIO()
        fig.savefig(buf, format="jpg")
        img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        url = f"data:image/jpeg;base64,{img_base64}"

        with self.div:
            if self.plot is not None:
                self.plot.set_source(url)
            else:
                self.plot = ui.image(url).classes("w-full mt-8")

        self.button.props("loading=false")

    def build(self):
        self.container = ui.element("div").classes("p-4 max-w-[800px] mx-auto")
        with self.container:
            ui.select(
                [
                    "K Means ++",
                ],
                label="聚类方法",
            ).props(
                "filled"
            ).bind_value(self, "type")
            ui.input(label="K 值").classes("mt-4").props("filled").bind_value(self, "k")
            ui.select(
                [
                    "hour",
                    "weekday",
                    "ret",
                ],
                label="聚类属性",
            ).props(
                "filled"
            ).classes("mt-4").bind_value(self, "cols")
            self.button = (
                ui.button("开始聚类", on_click=self.button_click)
                .props("push")
                .classes("full-width mt-4")
            )
            self.div = ui.element("div")
