from app import app, db
from flask import jsonify, request

from models import Rep, Lug, Per, Emp
from service.rep_service import crear_rep, leer_todos_rep, leer_rep, actualizar_rep, borrar_rep

@app.route('/rep', methods=['POST'])
def crear_reporte():
    data = request.get_json()
    if not data:
        return jsonify({"ok": False, "message": "No se recibió data"}), 400
    resultado = crear_rep(data)

    if resultado["ok"]:
        return jsonify(resultado), 201
    else:
        return jsonify(resultado), 500

@app.route('/rep', methods=['GET'])
def obtener_todos_reportes():
    reportes_list = leer_todos_rep()
    return jsonify({"ok": True, "data": reportes_list}), 200

@app.route('/rep/<int:id_rep>', methods=['GET', 'PUT', 'DELETE'])
def manejar_reporte_por_id(id_rep):
    if request.method == 'GET':
        resultado = leer_rep(id_rep)
        if resultado["ok"]:
            return jsonify(resultado), 200
        return jsonify(resultado), 404

    elif request.method == 'PUT':
        data = request.get_json()
        resultado = actualizar_rep(id_rep, data)
        if resultado["ok"]:
            return jsonify(resultado), 200
        return jsonify(resultado), 500

    elif request.method == 'DELETE':
        resultado = borrar_rep(id_rep)
        if resultado["ok"]:
            return jsonify(resultado), 200
        return jsonify(resultado), 500
@app.route('/reportes-completo/<int:user_id>', methods=['GET'])
def reportes_completo_por_usuario(user_id):
    try:

        query = db.session.query(
            Rep.IDEREP,
            Rep.FECEVE,
            Rep.FECREP,
            Rep.FREREP,
            Rep.OBSREP,
            Rep.CANREP,
            Lug.NOMLUG,
            Emp.NOMEMP,
            Emp.APPEMP,
            Emp.APMEMP
        ).join(
            Lug, Rep.LUGREP == Lug.IDELUG
        ).join(
            Per, Rep.PERREP == Per.IDEPER
        ).join(
            Emp, Per.EMPPER == Emp.IDEEMP
        ).filter(
            Rep.PERREP == user_id
        ).order_by(
            Rep.FECREP.desc()
        )
        resultados = []

        for fila in query.all():
            nombre_completo = f"{fila.NOMEMP} {fila.APPEMP} {fila.APMEMP}".strip()
            reporte_dict = {
                "IDEREP": fila.IDEREP,
                "FECEVE": str(fila.FECEVE),  #
                "FECREP": str(fila.FECREP),
                "FREREP": fila.FREREP,
                "OBSREP": fila.OBSREP,
                "CANREP": fila.CANREP,
                "NOMLUG": fila.NOMLUG,
                "REPORTANTE": nombre_completo
            }
            resultados.append(reporte_dict)

        return jsonify({"ok": True, "data": resultados}), 200

    except Exception as e:
        print(f"Error en servicio compuesto: {e}")
        return jsonify({"ok": False, "message": "Error interno al obtener reportes compuestos"}), 500