from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import get_db
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/vehicles")
def get_vehicles(request: Request):
    conn = get_db()
    vehicles = conn.execute("SELECT * FROM vehicles").fetchall()
    return templates.TemplateResponse("vehicles.html", {"request": request, "vehicles": vehicles})

@app.get("/drivers")
def get_drivers(request: Request):
    conn = get_db()
    drivers = conn.execute("SELECT * FROM drivers").fetchall()
    return templates.TemplateResponse("drivers.html", {"request": request, "drivers": drivers})

@app.get("/routes")
def get_routes(request: Request):
    conn = get_db()
    routes = conn.execute("SELECT * FROM routes").fetchall()
    return templates.TemplateResponse("routes.html", {"request": request, "routes": routes})

@app.get("/trips")
def get_trips(request: Request):
    conn = get_db()
    trips = conn.execute("SELECT * FROM trips").fetchall()
    return templates.TemplateResponse("trips.html", {"request": request, "trips": trips})

@app.get("/vehicles/add", response_class=HTMLResponse)
def add_vehicle_form(request: Request):
    return templates.TemplateResponse(
        "add_vehicles.html",
        {"request": request}
    )

@app.post("/vehicles/add")
def add_vehicle(
    type: str = Form(...),
    route_number: str = Form(...),
    model: str = Form(None),
    year: int = Form(...),
    capacity: int = Form(...)
):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO vehicles (type, route_number, model, year, capacity)
        VALUES (?, ?, ?, ?, ?)
    """, (
        type,
        route_number,
        model,
        year,
        capacity
    ))

    conn.commit()
    conn.close()
    return RedirectResponse(url="/vehicles", status_code=303)

@app.get("/export/vehicles")
def export_vehicles():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles")
    rows = cur.fetchall()
    conn.close()

    data = [dict(row) for row in rows]

    with open("vehicles.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return {"message": "Таблица vehicles экспортирована в vehicles.json"}

@app.post("/import/vehicles")
def import_vehicles():
    with open("vehicles.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = get_db()
    cur = conn.cursor()

    for v in data:
        cur.execute("""
            INSERT INTO vehicles (type, route_number, model, year, capacity, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            v["type"],
            v["route_number"],
            v.get("model"),
            v["year"],
            v["capacity"],
            v.get("status", "active")
        ))

    conn.commit()
    conn.close()
    return {"message": "Данные из JSON импортированы в таблицу vehicles"}