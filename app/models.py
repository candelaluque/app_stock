from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    costo = Column(Float, nullable=False, default=0.0)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    producto_nombre = Column(String) 
    cantidad = Column(Integer, nullable=False)
    precio_venta = Column(Float, nullable=False) 
    costo = Column(Float, nullable=False)
    ganancia = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.now)