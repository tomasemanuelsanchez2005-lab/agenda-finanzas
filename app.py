from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import time
from conexion import (
    ver_movimientos,
    obtener_meses_disponibles,
    agregar_movimiento,
    eliminar_movimiento,
    obtener_categorias,
    obtener_medios_pago,
    obtener_gastos_fijos,
    agregar_gasto_fijo,
    marcar_gasto_fijo_pagado,
    eliminar_gasto_fijo
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tipo = request.form.get("tipo", "Gasto")
        monto = float(request.form.get("monto", 0))
        fecha_str = request.form.get("fecha", "")
        
        if fecha_str:
            dt = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M")
            fecha_timestamp = int(dt.timestamp())
        else:
            fecha_timestamp = int(time.time())

        categoria_id = int(request.form.get("categoria") or 0)
        medio_pago_id = int(request.form.get("metodo_pago") or 0)
        descripcion = request.form.get("descripcion", "").strip()
        
        agregar_movimiento(tipo, monto, fecha_timestamp, categoria_id, medio_pago_id, descripcion)
        return redirect(url_for("index"))

    mes_seleccionado = request.args.get("mes", "")

    movimientos = ver_movimientos(mes_seleccionado if mes_seleccionado else None)
    
    todos_los_movimientos = ver_movimientos(None)

    categorias = obtener_categorias()
    medios_pago = obtener_medios_pago()
    meses_disponibles = obtener_meses_disponibles()

    total_ingresos = sum(float(m["monto"]) for m in movimientos if m["tipo"] == "Ingreso")
    total_gastos = sum(float(m["monto"]) for m in movimientos if m["tipo"] == "Gasto")
    total_inversiones = sum(float(m["monto"]) for m in movimientos if m["tipo"] == "Inversión")
    saldo_disponible = total_ingresos - total_gastos - total_inversiones

    saldos_por_medio = {mp["nombre"]: 0.0 for mp in medios_pago}
    for m in todos_los_movimientos:
        nombre_mp = m["metodo_pago"]
        monto = float(m["monto"])
        if nombre_mp not in saldos_por_medio:
            saldos_por_medio[nombre_mp] = 0.0
            
        if m["tipo"] == "Ingreso":
            saldos_por_medio[nombre_mp] += monto
        elif m["tipo"] in ["Gasto", "Inversión"]:
            saldos_por_medio[nombre_mp] -= monto

    gastos_fijos = obtener_gastos_fijos()
    mes_actual = datetime.now().strftime("%Y-%m")
    dia_actual = datetime.now().day

    return render_template("index.html", 
                           movimientos=movimientos,
                           ingresos=total_ingresos,
                           gastos=total_gastos,
                           inversiones=total_inversiones,
                           saldo=saldo_disponible,
                           saldos_por_medio=saldos_por_medio,
                           categorias=categorias,
                           medios_pago=medios_pago,
                           meses_disponibles=meses_disponibles,
                           mes_seleccionado=mes_seleccionado,
                           gastos_fijos=gastos_fijos,
                           mes_actual=mes_actual,
                           dia_hoy=dia_actual)

@app.route("/eliminar/<int:id_movimiento>")
def eliminar(id_movimiento):
    eliminar_movimiento(id_movimiento)
    return redirect(url_for("index"))

@app.route("/agregar_gasto_fijo", methods=["POST"])
def nuevo_gasto_fijo():
    nombre = request.form.get("nombre_fijo", "").strip()
    monto_estimado = float(request.form.get("monto_fijo") or 0)
    dia_vencimiento = int(request.form.get("dia_vencimiento") or 1)
    categoria_id = int(request.form.get("categoria_fijo") or 0)

    agregar_gasto_fijo(nombre, monto_estimado, dia_vencimiento, categoria_id)
    return redirect(url_for("index"))

@app.route("/pagar_gasto_fijo/<int:gasto_fijo_id>", methods=["POST"])
def pagar_gasto_fijo(gasto_fijo_id):
    nombre = request.form.get("nombre_fijo", "Gasto Fijo")
    monto = float(request.form.get("monto_real") or 0)
    categoria_id = int(request.form.get("categoria_id") or 0)
    medio_pago_id = int(request.form.get("medio_pago_id") or 0)

    ahora_timestamp = int(time.time())
    descripcion = f"Pago mensual: {nombre}"
    agregar_movimiento("Gasto", monto, ahora_timestamp, categoria_id, medio_pago_id, descripcion)

    mes_actual = datetime.now().strftime("%Y-%m")
    marcar_gasto_fijo_pagado(gasto_fijo_id, mes_actual)

    return redirect(url_for("index"))

@app.route("/eliminar_gasto_fijo/<int:gasto_fijo_id>")
def borrar_gasto_fijo(gasto_fijo_id):
    eliminar_gasto_fijo(gasto_fijo_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)