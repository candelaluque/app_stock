import secrets
from fastapi import FastAPI, Depends, Form, Request, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import engine, Base, get_db
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="App Inventario")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

import os
import secrets
from fastapi import FastAPI, Depends, Form, Request, HTTPException, status

security = HTTPBasic()

def verificar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    usuario_real = os.getenv("APP_USUARIO", "micaelaencina")
    clave_real = os.getenv("APP_CLAVE", "aedecohome2026")
    
    usuario_correcto = secrets.compare_digest(credentials.username, usuario_real)
    clave_correcta = secrets.compare_digest(credentials.password, clave_real)
    
    if not (usuario_correcto and clave_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/", response_class=HTMLResponse)
def leer_inicio(request: Request, db: Session = Depends(get_db), usuario: str = Depends(verificar_usuario)):
    productos = db.query(models.Producto).all()
    ventas = db.query(models.Venta).all()

    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio_semana = inicio_semana.replace(hour=0, minute=0, second=0)
    inicio_mes = hoy.replace(day=1, hour=0, minute=0, second=0)

    ventas_semana = sum((v.precio_venta * v.cantidad) for v in ventas if v.fecha >= inicio_semana)
    ganancia_semana = sum(v.ganancia for v in ventas if v.fecha >= inicio_semana)
    ventas_mes = sum((v.precio_venta * v.cantidad) for v in ventas if v.fecha >= inicio_mes)
    ganancia_mes = sum(v.ganancia for v in ventas if v.fecha >= inicio_mes)

    context = {
        "productos": productos,
        "ventas_semana": round(ventas_semana, 2),
        "ganancia_semana": round(ganancia_semana, 2),
        "ventas_mes": round(ventas_mes, 2),
        "ganancia_mes": round(ganancia_mes, 2)
    }
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@app.post("/productos")
def crear_producto(
    nombre: str = Form(...), 
    costo: float = Form(...), 
    precio: float = Form(...), 
    stock: int = Form(...), 
    db: Session = Depends(get_db),
    usuario: str = Depends(verificar_usuario)
):
    nuevo = models.Producto(nombre=nombre, costo=costo, precio=precio, stock=stock)
    db.add(nuevo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/vender")
def vender_producto(
    producto_id: int = Form(...), 
    cantidad: int = Form(...), 
    db: Session = Depends(get_db),
    usuario: str = Depends(verificar_usuario)
):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    
    if producto and producto.stock >= cantidad:
        producto.stock -= cantidad
        ganancia_total = (producto.precio - producto.costo) * cantidad
        nueva_venta = models.Venta(
            producto_id=producto.id,
            producto_nombre=producto.nombre,
            cantidad=cantidad,
            precio_venta=producto.precio,
            costo=producto.costo,
            ganancia=ganancia_total
        )
        db.add(nueva_venta)
        db.commit()
        
    return RedirectResponse(url="/", status_code=303)