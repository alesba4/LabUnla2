from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


# =========================================================
# CONEXIÓN A LA BASE DE DATOS
# =========================================================

engine = create_engine("sqlite:///database.db")

db_session = scoped_session(
    sessionmaker(bind=engine)
)

Base = declarative_base()

Base.query = db_session.query_property()


# =========================================================
# PRODUCTO
# =========================================================

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)

    productos_carrito = relationship(
        "CarritoProducto",
        back_populates="producto"
    )


# =========================================================
# CARRITO
# =========================================================

class Carrito(Base):
    __tablename__ = "carritos"

    id = Column(Integer, primary_key=True)
    fecha_creacion = Column(Date, nullable=False)
    estado = Column(String, nullable=False)

    productos = relationship(
        "CarritoProducto",
        back_populates="carrito",
        cascade="all, delete-orphan"
    )

    venta = relationship(
        "Venta",
        back_populates="carrito",
        uselist=False
    )


# =========================================================
# CARRITO_PRODUCTO
# =========================================================

class CarritoProducto(Base):
    __tablename__ = "carrito_producto"

    id = Column(Integer, primary_key=True)

    id_carrito = Column(
        Integer,
        ForeignKey("carritos.id"),
        nullable=False
    )

    id_producto = Column(
        Integer,
        ForeignKey("productos.id"),
        nullable=False
    )

    cantidad = Column(
        Integer,
        nullable=False
    )

    carrito = relationship(
        "Carrito",
        back_populates="productos"
    )

    producto = relationship(
        "Producto",
        back_populates="productos_carrito"
    )


# =========================================================
# VENTA
# =========================================================

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True)

    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)

    id_carrito = Column(
        Integer,
        ForeignKey("carritos.id"),
        unique=True,
        nullable=False
    )

    carrito = relationship(
        "Carrito",
        back_populates="venta"
    )


# =========================================================
# CREAR TABLAS
# =========================================================

Base.metadata.create_all(
    engine,
    Base.metadata.tables.values(),
    checkfirst=True
)
