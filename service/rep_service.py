from app import db
from models import Rep
from dto.rep_dto import RepRequestDTO
from dto.RepResponseDTO import RepResponseDTO



def crear_rep(data: dict) -> dict:

    try:
        dto = RepRequestDTO(data)
        data_dict = dto.to_dict()

        # Opcional: Si el frontend envía las fechas como string, aquí iría la conversión
        # data_dict['FECEVE'] = convertirStringADate(data_dict['FECEVE'])
        # data_dict['FECREP'] = convertirStringADate(data_dict['FECREP'])
        registro = Rep(**data_dict)
        db.session.add(registro)
        db.session.commit()

        return {"ok": True, "message": "Reporte creado correctamente", "id": registro.IDEREP}

    except ValueError as ve:
        db.session.rollback()
        return {"ok": False, "message": f"Error de validación: {ve}"}

    except Exception as e:
        db.session.rollback()
        print(f"Error al crear reporte: {e}")
        return {"ok": False, "message": "Ocurrió un error interno al guardar el reporte."}


def leer_todos_rep() -> list:
    reportes = Rep.query.all()
    return [RepResponseDTO(r).to_dict() for r in reportes]


def leer_rep(id_rep: int) -> dict:
    reporte = Rep.query.get(id_rep)
    if reporte:
        return {"ok": True, "data": RepResponseDTO(reporte).to_dict()}
    else:
        return {"ok": False, "message": f"Reporte con ID {id_rep} no encontrado."}


def actualizar_rep(id_rep: int, data: dict) -> dict:
    try:
        reporte = Rep.query.get(id_rep)
        if not reporte:
            return {"ok": False, "message": f"Reporte con ID {id_rep} no encontrado."}
        dto = RepRequestDTO(data)
        data_dict = dto.to_dict()
        for key, value in data_dict.items():
            if value is not None:
                setattr(reporte, key, value)

        db.session.commit()
        return {"ok": True, "message": "Reporte actualizado correctamente"}

    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar reporte: {e}")
        return {"ok": False, "message": "Ocurrió un error interno al actualizar el reporte."}


def borrar_rep(id_rep: int) -> dict:
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