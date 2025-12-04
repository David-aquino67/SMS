# services/rep_service.py

from app import db  # Importamos la instancia de SQLAlchemy
from models import Rep  # Importamos el Modelo de Reporte
from dto.rep_dto import RepRequestDTO
from dto.RepResponseDTO import RepResponseDTO


# from services.util_service import convertirStringADate # Importar si es necesario para formatear fechas

# --- Paso 1: Implementación de crear_rep(data) ---

def crear_rep(data: dict) -> dict:
    """
    Crea un nuevo registro de Reporte.
    """
    try:
        # 1. Usar el DTO para validar y estructurar la entrada
        dto = RepRequestDTO(data)
        data_dict = dto.to_dict()

        # Opcional: Si el frontend envía las fechas como string, aquí iría la conversión
        # data_dict['FECEVE'] = convertirStringADate(data_dict['FECEVE'])
        # data_dict['FECREP'] = convertirStringADate(data_dict['FECREP'])

        # 2. Crear una nueva instancia del modelo REP
        registro = Rep(**data_dict)

        # 3. Guardar en la base de datos
        db.session.add(registro)
        db.session.commit()

        return {"ok": True, "message": "Reporte creado correctamente", "id": registro.IDEREP}

    except ValueError as ve:
        # Errores del DTO (Ej: campos faltantes)
        db.session.rollback()
        return {"ok": False, "message": f"Error de validación: {ve}"}

    except Exception as e:
        # Errores de la base de datos o inesperados
        db.session.rollback()
        print(f"Error al crear reporte: {e}")
        return {"ok": False, "message": "Ocurrió un error interno al guardar el reporte."}


# --- Paso 2: Implementación de lectura ---

def leer_todos_rep() -> list:
    """
    Lee todos los registros de Reporte.
    """
    reportes = Rep.query.all()
    # Usamos el DTO de respuesta para formatear cada modelo antes de devolverlo
    return [RepResponseDTO(r).to_dict() for r in reportes]


def leer_rep(id_rep: int) -> dict:
    """
    Lee un registro de Reporte por su ID.
    """
    reporte = Rep.query.get(id_rep)
    if reporte:
        return {"ok": True, "data": RepResponseDTO(reporte).to_dict()}
    else:
        return {"ok": False, "message": f"Reporte con ID {id_rep} no encontrado."}


# --- Paso 3: Implementación de actualización y borrado ---

def actualizar_rep(id_rep: int, data: dict) -> dict:
    """
    Actualiza un registro de Reporte existente.
    """
    try:
        reporte = Rep.query.get(id_rep)
        if not reporte:
            return {"ok": False, "message": f"Reporte con ID {id_rep} no encontrado."}

        # 1. Usar el DTO para limpiar la entrada (opcional, podrías iterar sobre 'data' directamente)
        dto = RepRequestDTO(data)
        data_dict = dto.to_dict()

        # 2. Iterar sobre los datos recibidos y actualizar los atributos del modelo
        for key, value in data_dict.items():
            # Solo actualiza si el valor no es None o si la clave existe en el DTO/Modelo
            if value is not None:
                setattr(reporte, key, value)

        db.session.commit()
        return {"ok": True, "message": "Reporte actualizado correctamente"}

    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar reporte: {e}")
        return {"ok": False, "message": "Ocurrió un error interno al actualizar el reporte."}


def borrar_rep(id_rep: int) -> dict:
    """
    Borra un registro de Reporte por su ID.
    """
    try:
        reporte = Rep.query.get(id_rep)
        if not reporte:
            return {"ok": False, "message": f"Reporte con ID {id_rep} no encontrado."}

        db.session.delete(reporte)
        db.session.commit()
        return {"ok": True, "message": "Reporte eliminado correctamente"}

    except Exception as e:
        db.session.rollback()
        print(f"Error al borrar reporte: {e}")
        return {"ok": False, "message": "Ocurrió un error interno al eliminar el reporte."}