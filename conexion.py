import mysql.connector

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="",          
            database="agenda_finanzas"
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None

def ver_movimientos(mes_filtro=None):
    conexion = None
    cursor = None
    movimientos = []
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            sql = """
                SELECT 
                    m.movimiento_id, 
                    m.tipo, 
                    m.monto, 
                    m.fecha AS timestamp_fecha,
                    FROM_UNIXTIME(m.fecha, '%d/%m/%Y %H:%i') AS fecha_formateada,
                    FROM_UNIXTIME(m.fecha, '%Y-%m') AS mes_anio,
                    COALESCE(c.nombre, 'Sin categoría') AS categoria, 
                    COALESCE(mp.nombre, 'Sin medio de pago') AS metodo_pago, 
                    m.descripcion
                FROM movimientos m
                LEFT JOIN categorias c ON m.categoria_id = c.categoria_id
                LEFT JOIN medios_pago mp ON m.medio_pago_id = mp.medio_pago_id
            """
            parametros = []
            if mes_filtro:
                sql += " WHERE FROM_UNIXTIME(m.fecha, '%Y-%m') = %s"
                parametros.append(mes_filtro)
                
            sql += " ORDER BY m.fecha DESC;"
            cursor.execute(sql, tuple(parametros))
            movimientos = cursor.fetchall()
    except Exception as e:
        print(f"Error al leer movimientos: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    return movimientos

def obtener_meses_disponibles():
    conexion = None
    cursor = None
    meses = []
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            sql = """
                SELECT DISTINCT FROM_UNIXTIME(fecha, '%Y-%m') AS mes_anio 
                FROM movimientos 
                WHERE fecha > 0 
                ORDER BY mes_anio DESC;
            """
            cursor.execute(sql)
            meses = [fila["mes_anio"] for fila in cursor.fetchall()]
    except Exception as e:
        print(f"Error al obtener meses: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    return meses

def agregar_movimiento(tipo, monto, fecha_timestamp, categoria_id, medio_pago_id, descripcion):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO movimientos 
                (tipo, monto, fecha, categoria_id, medio_pago_id, descripcion) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (tipo, monto, fecha_timestamp, categoria_id, medio_pago_id, descripcion))
            conexion.commit()
    except Exception as e:
        if conexion: conexion.rollback()
        print(f"Error al agregar movimiento: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def eliminar_movimiento(movimiento_id):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM movimientos WHERE movimiento_id = %s", (movimiento_id,))
            conexion.commit()
    except Exception as e:
        if conexion: conexion.rollback()
        print(f"Error al eliminar movimiento: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def obtener_categorias():
    conexion = None
    cursor = None
    categorias = []
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM categorias ORDER BY nombre ASC")
            categorias = cursor.fetchall()
    except Exception as e:
        print(f"Error al leer categorías: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    return categorias

def obtener_medios_pago():
    conexion = None
    cursor = None
    medios = []
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM medios_pago ORDER BY nombre ASC")
            medios = cursor.fetchall()
    except Exception as e:
        print(f"Error al leer medios de pago: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    return medios

def obtener_gastos_fijos():
    conexion = None
    cursor = None
    gastos = []
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor(dictionary=True)
            sql = """
                SELECT 
                    gf.gasto_fijo_id,
                    gf.nombre,
                    gf.monto_estimado,
                    gf.dia_vencimiento,
                    gf.categoria_id,
                    gf.ultimo_mes_pagado,
                    COALESCE(c.nombre, 'Sin categoría') AS categoria
                FROM gastos_fijos gf
                LEFT JOIN categorias c ON gf.categoria_id = c.categoria_id
                ORDER BY gf.dia_vencimiento ASC
            """
            cursor.execute(sql)
            gastos = cursor.fetchall()
    except Exception as e:
        print(f"Error al leer gastos fijos: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()
    return gastos

def agregar_gasto_fijo(nombre, monto_estimado, dia_vencimiento, categoria_id):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO gastos_fijos (nombre, monto_estimado, dia_vencimiento, categoria_id, ultimo_mes_pagado)
                VALUES (%s, %s, %s, %s, '')
            """
            cursor.execute(sql, (nombre, monto_estimado, dia_vencimiento, categoria_id))
            conexion.commit()
    except Exception as e:
        if conexion: conexion.rollback()
        print(f"Error al agregar gasto fijo: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def marcar_gasto_fijo_pagado(gasto_fijo_id, mes_actual):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            sql = "UPDATE gastos_fijos SET ultimo_mes_pagado = %s WHERE gasto_fijo_id = %s"
            cursor.execute(sql, (mes_actual, gasto_fijo_id))
            conexion.commit()
    except Exception as e:
        if conexion: conexion.rollback()
        print(f"Error al actualizar gasto fijo: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

def eliminar_gasto_fijo(gasto_fijo_id):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM gastos_fijos WHERE gasto_fijo_id = %s", (gasto_fijo_id,))
            conexion.commit()
    except Exception as e:
        if conexion: conexion.rollback()
        print(f"Error al eliminar gasto fijo: {e}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()