from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def main(request: Request):
    return templates.TemplateResponse(request=request, name="main.html")

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}
