from fastapi import FastAPI, HTTPException, status

from database import Carrito, db_session, Producto, CarritoProducto, Venta

from schema import CarritoProductoCreate, ProductoCreate, ProductoResponse, VentaCreate, VentaResponse, CarritoCreate, CarritoResponse, VentaCarritoCreate


# =========================================================
# APLICACIÓN
# =========================================================

app = FastAPI(title="Laboratorio - Ventas")


# =========================================================
# INICIO
# =========================================================

@app.get("/")
async def root():
    return {"message": "Hello World"}


# =========================================================
# PRODUCTOS
# =========================================================

# GET /productos
# Obtener todos los productos
@app.get(
    "/productos",
    response_model=list[ProductoResponse],
    status_code=status.HTTP_200_OK
)
async def get_productos():

    try:
        productos = Producto.query.all()

        return productos

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {e}"
        )


# GET /productos/{id}
# Obtener un producto en particular
@app.get(
    "/productos/{producto_id}",
    response_model=ProductoResponse,
    status_code=status.HTTP_200_OK
)
async def get_producto(producto_id: int):

    try:
        producto = Producto.query.get(producto_id)

        if producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )

        return producto

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el producto: {e}"
        )


# POST /productos
# Crear un producto
@app.post(
    "/productos",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED
)
async def crear_producto(producto_data: ProductoCreate):

    try:

        # Buscamos si ya existe un producto con ese nombre
        producto_existente = Producto.query.filter_by(
            nombre=producto_data.nombre
        ).first()

        if producto_existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El producto ya existe"
            )

        producto = Producto(
            nombre=producto_data.nombre,
            precio=producto_data.precio
        )

        db_session.add(producto)
        db_session.commit()
        db_session.refresh(producto)

        return producto

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el producto: {e}"
        )


# PUT /productos/{id}
# Actualizar un producto
@app.put(
    "/productos/{producto_id}",
    response_model=ProductoResponse,
    status_code=status.HTTP_200_OK
)
async def actualizar_producto(
    producto_id: int,
    producto_data: ProductoCreate
):

    try:

        producto = Producto.query.get(producto_id)

        if producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )

        # Verificamos que no exista otro producto
        # con el mismo nombre
        producto_existente = Producto.query.filter_by(
            nombre=producto_data.nombre
        ).first()

        if (
            producto_existente is not None
            and producto_existente.id != producto_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El producto ya existe"
            )

        producto.nombre = producto_data.nombre
        producto.precio = producto_data.precio

        db_session.commit()
        db_session.refresh(producto)

        return producto

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el producto: {e}"
        )


# DELETE /productos/{id}
# Eliminar un producto
@app.delete(
    "/productos/{producto_id}",
    response_model=ProductoResponse,
    status_code=status.HTTP_200_OK
)
async def eliminar_producto(producto_id: int):

    try:

        producto = Producto.query.get(producto_id)

        if producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )

        # No se puede eliminar si el producto
        # está dentro de algún carrito
        producto_en_carrito = CarritoProducto.query.filter_by(
            id_producto=producto_id
        ).first()

        if producto_en_carrito is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar el producto porque está en un carrito"
            )

        db_session.delete(producto)
        db_session.commit()

        return producto

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el producto: {e}"
        )
        
from schema import (ProductoCreate,ProductoResponse,CarritoCreate,CarritoResponse
)

# =========================================================
# CARRITOS
# =========================================================

@app.post(
    "/carritos",
    response_model=CarritoResponse,
    status_code=status.HTTP_201_CREATED
)
async def crear_carrito(carrito_data: CarritoCreate):

    try:

        carrito = Carrito(
            fecha_creacion=carrito_data.fecha_creacion,
            estado=carrito_data.estado
        )

        db_session.add(carrito)
        db_session.commit()
        db_session.refresh(carrito)

        return carrito

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el carrito: {e}"
        )
        
# GET /carritos
# Obtener todos los carritos
@app.get(
    "/carritos",
    response_model=list[CarritoResponse],
    status_code=status.HTTP_200_OK
)
async def get_carritos():

    try:
        carritos = Carrito.query.all()

        return carritos

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener carritos: {e}"
        )
        
# GET /carritos/{id}
# Obtener un carrito en particular
@app.get(
    "/carritos/{carrito_id}",
    response_model=CarritoResponse,
    status_code=status.HTTP_200_OK
)
async def get_carrito(carrito_id: int):

    try:
        carrito = Carrito.query.get(carrito_id)

        if carrito is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrito no encontrado"
            )

        return carrito

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el carrito: {e}"
        )
    
# PUT /carritos/{id}
# Actualizar un carrito
@app.put(
    "/carritos/{carrito_id}",
    response_model=CarritoResponse,
    status_code=status.HTTP_200_OK
)
async def actualizar_carrito(
    carrito_id: int,
    carrito_data: CarritoCreate
):

    try:
        carrito = Carrito.query.get(carrito_id)

        if carrito is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrito no encontrado"
            )

        # Verificamos si el carrito ya está asociado
        # a una venta
        venta = Venta.query.filter_by(
            id_carrito=carrito_id
        ).first()

        if venta is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede modificar un carrito asociado a una venta"
            )

        carrito.fecha_creacion = carrito_data.fecha_creacion
        carrito.estado = carrito_data.estado

        db_session.commit()
        db_session.refresh(carrito)

        return carrito

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el carrito: {e}"
        )
        
# =========================================================
# AGREGAR PRODUCTO A UN CARRITO
# =========================================================

@app.post(
    "/carritos/{carrito_id}/productos",
    response_model=CarritoResponse,
    status_code=status.HTTP_200_OK
)
async def agregar_producto_carrito(
    carrito_id: int,
    producto_data: CarritoProductoCreate
):

    try:

        # Buscamos el carrito
        carrito = Carrito.query.get(carrito_id)

        if carrito is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrito no encontrado"
            )

        # El carrito debe estar abierto
        if carrito.estado != "abierto":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Solo se pueden agregar productos a un carrito abierto"
            )

        # La cantidad debe ser mayor a 0
        if producto_data.cantidad <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cantidad debe ser mayor a 0"
            )

        # Buscamos el producto
        producto = Producto.query.get(
            producto_data.id_producto
        )

        if producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )

        # Buscamos si el producto ya está dentro
        # del carrito
        carrito_producto = CarritoProducto.query.filter_by(
            id_carrito=carrito_id,
            id_producto=producto_data.id_producto
        ).first()

        if carrito_producto is not None:

            # Si ya existe, sumamos la cantidad
            carrito_producto.cantidad += producto_data.cantidad

        else:

            # Si no existe, creamos un nuevo registro
            carrito_producto = CarritoProducto(
                id_carrito=carrito_id,
                id_producto=producto_data.id_producto,
                cantidad=producto_data.cantidad
            )

            db_session.add(carrito_producto)

        db_session.commit()
        db_session.refresh(carrito)

        return carrito

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al agregar el producto al carrito: {e}"
        )
        
@app.delete(
    "/carritos/{carrito_id}/productos/{producto_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def eliminar_producto_carrito(
    carrito_id: int,
    producto_id: int
):

    try:

        # Buscamos el carrito
        carrito = Carrito.query.get(carrito_id)

        if carrito is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrito no encontrado"
            )

        # El carrito debe estar abierto
        if carrito.estado != "abierto":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Solo se pueden quitar productos de un carrito abierto"
            )

        # Buscamos el producto
        producto = Producto.query.get(producto_id)

        if producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )

        # Buscamos el producto dentro del carrito
        carrito_producto = CarritoProducto.query.filter_by(
            id_carrito=carrito_id,
            id_producto=producto_id
        ).first()

        if carrito_producto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El producto no se encuentra en el carrito"
            )

        db_session.delete(carrito_producto)
        db_session.commit()

        return None

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el producto del carrito: {e}"
        )
    
# DELETE /carritos/{id}
# Eliminar un carrito
@app.delete(
    "/carritos/{carrito_id}",
    response_model=CarritoResponse,
    status_code=status.HTTP_200_OK
)
async def eliminar_carrito(carrito_id: int):

    try:

        # Buscamos el carrito
        carrito = Carrito.query.get(carrito_id)

        if carrito is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrito no encontrado"
            )

        # Verificamos si está asociado a una venta
        venta = Venta.query.filter_by(
            id_carrito=carrito_id
        ).first()

        if venta is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar un carrito asociado a una venta"
            )

        db_session.delete(carrito)
        db_session.commit()

        return carrito

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el carrito: {e}"
        )
        
def calcular_precio_total(carrito):
    total = 0

    for item in carrito.productos:
        total += item.producto.precio * item.cantidad

    return total

# =========================================================
# VENTAS
# =========================================================


# POST /ventas
# Crear una venta
# =========================================================
# VENTAS
# =========================================================

@app.post(
    "/ventas",
    response_model=VentaResponse,
    status_code=status.HTTP_201_CREATED
)
async def crear_venta(venta_data: VentaCreate):

    try:

        # Buscamos el carrito
        carrito = Carrito.query.get(venta_data.id_carrito)

        if carrito is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrito no encontrado"
            )

        # El carrito debe estar cerrado
        if carrito.estado != "cerrado":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Solo se puede registrar una venta con un carrito cerrado"
            )

        # Comprobamos que el carrito no esté asociado
        # a otra venta
        venta_existente = Venta.query.filter_by(
            id_carrito=venta_data.id_carrito
        ).first()

        if venta_existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El carrito ya está asociado a una venta"
            )

        # Creamos la venta
        venta = Venta(
            fecha=venta_data.fecha,
            hora=venta_data.hora,
            id_carrito=venta_data.id_carrito
        )

        db_session.add(venta)
        db_session.commit()
        db_session.refresh(venta)

        # Calculamos el total solamente para la respuesta
        precio_total = calcular_precio_total(carrito)

        return {
            "id": venta.id,
            "fecha": venta.fecha,
            "hora": venta.hora,
            "precio_total": precio_total,
            "carrito": carrito
        }

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la venta: {e}"
        )
        
# GET /ventas
# Obtener todas las ventas
@app.get(
    "/ventas",
    response_model=list[VentaResponse],
    status_code=status.HTTP_200_OK
)
async def get_ventas():

    try:

        ventas = Venta.query.all()

        respuestas = []

        for venta in ventas:

            precio_total = calcular_precio_total(venta.carrito)

            respuestas.append({
                "id": venta.id,
                "fecha": venta.fecha,
                "hora": venta.hora,
                "precio_total": precio_total,
                "carrito": venta.carrito
            })

        return respuestas

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las ventas: {e}"
        )
        
# GET /ventas/{id}
# Obtener una venta en particular
@app.get(
    "/ventas/{venta_id}",
    response_model=VentaResponse,
    status_code=status.HTTP_200_OK
)
async def get_venta(venta_id: int):

    try:

        venta = Venta.query.get(venta_id)

        if venta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venta no encontrada"
            )

        precio_total = calcular_precio_total(venta.carrito)

        return {
            "id": venta.id,
            "fecha": venta.fecha,
            "hora": venta.hora,
            "precio_total": precio_total,
            "carrito": venta.carrito
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la venta: {e}"
        )
        
# PUT /ventas/{id}
# Actualizar una venta
@app.put(
    "/ventas/{venta_id}",
    response_model=VentaResponse,
    status_code=status.HTTP_200_OK
)
async def actualizar_venta(
    venta_id: int,
    venta_data: VentaCreate
):

    try:

        # Buscamos la venta
        venta = Venta.query.get(venta_id)

        if venta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venta no encontrada"
            )

        # Buscamos el carrito nuevo
        carrito = Carrito.query.get(
            venta_data.id_carrito
        )

        if carrito is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrito no encontrado"
            )

        # El carrito debe estar cerrado
        if carrito.estado != "cerrado":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Solo se puede asociar una venta a un carrito cerrado"
            )

        # Verificamos si el carrito ya pertenece
        # a otra venta
        venta_existente = Venta.query.filter(
            Venta.id_carrito == venta_data.id_carrito,
            Venta.id != venta_id
        ).first()

        if venta_existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El carrito ya está asociado a otra venta"
            )

        # Actualizamos la venta
        venta.fecha = venta_data.fecha
        venta.hora = venta_data.hora
        venta.id_carrito = venta_data.id_carrito

        db_session.commit()
        db_session.refresh(venta)

        # Calculamos el total para la respuesta
        precio_total = calcular_precio_total(venta.carrito)

        return {
            "id": venta.id,
            "fecha": venta.fecha,
            "hora": venta.hora,
            "precio_total": precio_total,
            "carrito": venta.carrito
        }

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la venta: {e}"
        )
        
# DELETE /ventas/{id}
# Eliminar una venta
@app.delete(
    "/ventas/{venta_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def eliminar_venta(venta_id: int):

    try:

        venta = Venta.query.get(venta_id)

        if venta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venta no encontrada"
            )

        db_session.delete(venta)
        db_session.commit()

        return None

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la venta: {e}"
        )
        
# =========================================================
# ASIGNAR / REEMPLAZAR CARRITO DE UNA VENTA
# =========================================================

@app.post(
    "/ventas/{venta_id}/carrito",
    response_model=VentaResponse,
    status_code=status.HTTP_200_OK
)
async def asignar_carrito_venta(
    venta_id: int,
    carrito_data: VentaCarritoCreate
):

    try:

        # Buscamos la venta
        venta = Venta.query.get(venta_id)

        if venta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venta no encontrada"
            )

        # Buscamos el carrito
        carrito = Carrito.query.get(
            carrito_data.id_carrito
        )

        if carrito is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrito no encontrado"
            )

        # El carrito debe estar cerrado
        if carrito.estado != "cerrado":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Solo se puede asociar un carrito cerrado a una venta"
            )

        # Verificamos si el carrito ya está asociado
        # a otra venta
        venta_existente = Venta.query.filter(
            Venta.id_carrito == carrito_data.id_carrito,
            Venta.id != venta_id
        ).first()

        if venta_existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El carrito ya está asociado a otra venta"
            )

        # Asignamos o reemplazamos el carrito
        venta.id_carrito = carrito_data.id_carrito

        db_session.commit()
        db_session.refresh(venta)

        # Calculamos el total usando el nuevo carrito
        precio_total = calcular_precio_total(venta.carrito)

        return {
            "id": venta.id,
            "fecha": venta.fecha,
            "hora": venta.hora,
            "precio_total": precio_total,
            "carrito": venta.carrito
        }

    except HTTPException:
        raise

    except Exception as e:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al asignar el carrito a la venta: {e}"
        )