import threading


class Task:
    def __init__(self, func, callback, *args, **kwargs):
        self.func = func
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.thread = None

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            raise e

        if self.callback:
            self.callback(result)


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, func, callback, *args, **kwargs):
        task = Task(func, callback, *args, **kwargs)
        self.tasks.append(task)
        self.start_task(task)

    def start_task(self, task):
        thread = threading.Thread(target=task.run)
        task.thread = thread
        thread.start()

    def wait_all(self):
        for task in self.tasks:
            task.thread.join()
