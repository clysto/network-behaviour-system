from router.router import Router
from task import TaskManager

CONNECTION_STRING = "mongodb://127.0.0.1:27017/"

router = Router()
task_manager = TaskManager()
