from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Adding templates and static directories
templates = Jinja2Templates(directory="app/templates")
static = StaticFiles(directory="app/static")
