from app import app, db
from flask import jsonify, request

# Importa los modelos y servicios necesarios
from models import Rep, Lug, Per, Emp  # Modelos para el join compuesto
from service.rep_service import crear_rep, leer_todos_rep, leer_rep, actualizar_rep, borrar_rep


# --- 1. RUTA POST: Crear Reporte (POST /rep) ---
@app.route('/rep', methods=['POST'])
def crear_reporte():
    """Llama a la función crear_rep del servicio."""
    data = request.get_json()
    if not data:
        return jsonify({"ok": False, "message": "No se recibió data"}), 400

    # El servicio maneja la lógica y la comunicación con la DB
    resultado = crear_rep(data)

    if resultado["ok"]:
        return jsonify(resultado), 201  # 201 Created
    else:
        return jsonify(resultado), 500  # 500 Internal Server Error (o 400 si es error de validación)


# --- 2. RUTA GET: Leer Todos (GET /rep) ---
@app.route('/rep', methods=['GET'])
def obtener_todos_reportes():
    """Llama a la función leer_todos_rep del servicio."""
    reportes_list = leer_todos_rep()
    return jsonify({"ok": True, "data": reportes_list}), 200


# --- 3. RUTAS GET, PUT, DELETE por ID (/rep/<id>) ---
# Se pueden consolidar las demás operaciones CRUD en una sola ruta con un parámetro
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
# --- Paso 1: Definición del Endpoint ---
@app.route('/reportes-completo/<int:user_id>', methods=['GET'])
def reportes_completo_por_usuario(user_id):
    """
    Obtiene un listado detallado de reportes para un usuario específico (o todos si se ajusta el filtro),
    uniendo información de Lugar y Empleado.
    """
    try:
        # --- Paso 2: Construcción de la Consulta con Joins ---
        # db.session.query(...) selecciona columnas específicas.
        # .join(Modelo, Condición) une las tablas.
        # .filter(...) aplica la restricción por usuario.

        query = db.session.query(
            Rep.IDEREP,
            Rep.FECEVE,
            Rep.FECREP,
            Rep.FREREP,
            Rep.OBSREP,
            Rep.CANREP,
            Lug.NOMLUG,  # Nombre del Lugar
            Emp.NOMEMP,  # Nombre del Empleado
            Emp.APPEMP,  # Apellido Paterno
            Emp.APMEMP  # Apellido Materno
        ).join(
            Lug, Rep.LUGREP == Lug.IDELUG  # Join Rep -> Lug
        ).join(
            Per, Rep.PERREP == Per.IDEPER  # Join Rep -> Per
        ).join(
            Emp, Per.EMPPER == Emp.IDEEMP  # Join Per -> Emp
        ).filter(
            Rep.PERREP == user_id  # Filtro: Solo reportes de este usuario
        ).order_by(
            Rep.FECREP.desc()  # Ordenar por fecha descendente (lo más nuevo primero)
        )

        # --- Paso 3: Mapeo de la Respuesta ---
        resultados = []

        # Iteramos sobre los resultados de la consulta (que vienen como tuplas/objetos Row)
        for fila in query.all():
            # Formatear el nombre completo para facilitar el trabajo al frontend
            nombre_completo = f"{fila.NOMEMP} {fila.APPEMP} {fila.APMEMP}".strip()

            # Construimos el diccionario
            reporte_dict = {
                "IDEREP": fila.IDEREP,
                "FECEVE": str(fila.FECEVE),  # Convertir fecha a string
                "FECREP": str(fila.FECREP),  # Convertir datetime a string
                "FREREP": fila.FREREP,
                "OBSREP": fila.OBSREP,
                "CANREP": fila.CANREP,
                "NOMLUG": fila.NOMLUG,  # Dato traído de tabla Lug
                "REPORTANTE": nombre_completo  # Dato calculado de tabla Emp
            }
            resultados.append(reporte_dict)

        # Devolvemos la lista en formato JSON
        return jsonify({"ok": True, "data": resultados}), 200

    except Exception as e:
        print(f"Error en servicio compuesto: {e}")
        return jsonify({"ok": False, "message": "Error interno al obtener reportes compuestos"}), 500