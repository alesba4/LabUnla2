from datetime import date, time

from pydantic import BaseModel, ConfigDict, Field


# =========================================================
# PRODUCTO
# =========================================================

class ProductoCreate(BaseModel):
    nombre: str
    precio: float


class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# CARRITO - PRODUCTOS
# =========================================================

class CarritoProductoCreate(BaseModel):
    id_producto: int
    cantidad: int


class CarritoProductoResponse(BaseModel):
    id: int
    producto: ProductoResponse
    cantidad: int

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# CARRITO
# =========================================================

class CarritoCreate(BaseModel):
    fecha_creacion: date
    estado: str


class CarritoResponse(BaseModel):
    id: int
    fecha_creacion: date
    estado: str
    productos: list[CarritoProductoResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# VENTA
# =========================================================

class VentaCreate(BaseModel):
    fecha: date
    hora: time
    id_carrito: int

    model_config = ConfigDict(extra="forbid")


class VentaResponse(BaseModel):
    id: int
    fecha: date
    hora: time
    precio_total: float
    carrito: CarritoResponse

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# ASIGNAR / REEMPLAZAR CARRITO DE UNA VENTA
# =========================================================

class VentaCarritoCreate(BaseModel):
    id_carrito: int