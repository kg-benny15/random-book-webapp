from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.extensions import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(request=request, name="main/home_page.html")
