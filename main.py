from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from utils import clonarPaginaWeb, traducirTags
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")



@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/traducir-pagina/")
async def clonar_traducir_pagina(request: Request, url: str = Form(...)):
    clonarPaginaWeb(url)
    traducirTags()
    return templates.TemplateResponse("status.html", {"request": request, "url": url})


@app.get("/pagina-original", response_class=HTMLResponse)
async def ver_pagina_original(request: Request):
    try:
        with open(f"website_original.html", "r", encoding="utf-8") as HTMLFile:
            html_content = HTMLFile.read()
    except Exception as e:
        return RedirectResponse(request.url_for("root"))
    return html_content


@app.get("/pagina-traducida", response_class=HTMLResponse)
async def ver_pagina_traducida(request: Request):
    try:
        with open(f"website_translated.html", "r", encoding="utf-8") as HTMLFile:
            html_content = HTMLFile.read()
    except Exception as e:
        return RedirectResponse(request.url_for("root"))
    return html_content


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000)