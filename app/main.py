from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Optional
import os
import secrets
from app.services.compose import generate_precliniverse_compose

app = FastAPI(title="Precliniverse Wizard")

# Ensure static/templates exist
os.makedirs("app/static", exist_ok=True)
os.makedirs("app/templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse("wizard/welcome.html", {"request": request})

@app.get("/install/step1", response_class=HTMLResponse)
async def step1(request: Request):
    return templates.TemplateResponse("wizard/step1_modules.html", {"request": request})

@app.post("/install/step2", response_class=HTMLResponse)
async def step2(request: Request, module: List[str] = Form(...)):
    return templates.TemplateResponse("wizard/step2_config.html", {
        "request": request, 
        "selected_modules": module
    })

@app.post("/install/generate", response_class=HTMLResponse)
async def generate(
    request: Request, 
    facility_name: str = Form(...),
    db_pass: str = Form(None),
    sso_pass: str = Form(None),
    modules: str = Form(...),
    # Admin
    admin_email: str = Form(None),
    admin_pass: str = Form(None),
    # SMTP
    smtp_host: str = Form(None),
    smtp_port: int = Form(587),
    smtp_user: str = Form(None),
    smtp_pass: str = Form(None),
    smtp_tls: str = Form(None), # Checkbox sends 'on' or None
    smtp_from: str = Form(None)
):
    module_list = modules.split(",")
    # If passwords are not provided, generate them
    db_p = db_pass if db_pass else secrets.token_urlsafe(16)
    sso_p = sso_pass if sso_pass else secrets.token_urlsafe(16)
    
    config = {
        "facility_name": facility_name,
        "db_pass": db_p,
        "sso_pass": sso_p,
        "modules": module_list,
        "db_external": False,
        "admin_config": {
            "email": admin_email,
            "password": admin_pass if admin_pass else secrets.token_urlsafe(12)
        },
        "smtp_config": {
            "host": smtp_host,
            "port": smtp_port,
            "user": smtp_user,
            "password": smtp_pass,
            "tls": True if smtp_tls == "on" else False,
            "from_email": smtp_from
        }
    }
    
    compose_content = generate_precliniverse_compose(config)
    
    return templates.TemplateResponse("wizard/review.html", {
        "request": request,
        "compose": compose_content,
        "config": config
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
