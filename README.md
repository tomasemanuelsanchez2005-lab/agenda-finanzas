# 💰 Mi Agenda y Finanzas Personales (Versión 1.0 - MVP)

Aplicación web para administrar ingresos, gastos, inversiones y recordar el pago de gastos fijos mensuales. Desarrollada con Python (Flask) y MySQL aplicando las correcciones de arquitectura recomendadas por mi sensei

## 🛠️ Qué incluye esta Primera Versión (V1.0)

1. **Base de datos relacional (4 tablas):**
   - Separación en `movimientos`, `categorias`, `medios_pago` y `gastos_fijos` para trabajar con identificadores numéricos (IDs) en lugar de repetir textos.
   - **Valores `DEFAULT` declarados:** Todos los campos `NOT NULL` tienen su valor por defecto (`DEFAULT 0` para números/IDs y `DEFAULT ''` para textos) para que el motor de MySQL no falle según la versión instalada ni obligue a tener categorías previas para guardar un movimiento.
   - **Campo `ENUM` en el tipo de movimiento:** La columna `tipo` solo permite `'Ingreso'`, `'Gasto'` o `'Inversión'`, evitando que entren palabras distintas por error.
   - **Fechas con Timestamp numérico (`BIGINT`):** Las fechas se guardan como segundos Unix (un número entero) para evitar problemas de formato o zonas horarias al pasarlas por el código. Al leerlas en SQL se formatean con `FROM_UNIXTIME()`.

2. **Balances separados (Mes filtrado vs. Saldo real en Billeteras):**
   - **Tarjetas principales e Historial:** Permiten filtrar por mes (`YYYY-MM`) para analizar cuánto ingresó, cuánto se gastó y cuánto se invirtió en ese período puntual.
   - **Saldo en Cuentas / Billeteras:** Calcula el dinero real acumulado histórico en cada medio de pago (Efectivo, Mercado Pago, Banco, etc.), descontando tanto los gastos como el dinero que salió hacia inversiones.

3. **Agenda de Gastos Fijos con Pago en 1 Clic:**
   - Permite registrar gastos recurrentes indicando qué día del mes vencen (del 1 al 31).
   - Muestra alertas por color según el día actual (pagado en el mes, pendiente o vencido).
   - Al tocar **"Pagar"**, registra automáticamente el gasto en la tabla `movimientos`, descuenta el saldo de la billetera elegida y marca el servicio como pagado en el mes actual (`ultimo_mes_pagado`).

## 📂 Archivos del proyecto
- `app.py`: Rutas de Flask, conversión de fechas a Timestamp y cálculo de saldos.
- `conexion.py`: Consultas SQL a MySQL (`SELECT` con `LEFT JOIN`, `INSERT`, `UPDATE` y `DELETE`).
- `database.sql`: Script para crear la base de datos `agenda_finanzas` y las tablas desde cero.
- `templates/index.html`: Pantalla principal con plantillas Jinja2.
- `static/css/style.css`: Diseño visual de tarjetas, formularios y tablas.

## 🚀 Cómo probar el proyecto

1. Ejecutar el archivo `database.sql` en MySQL Workbench.
2. Configurar el usuario y contraseña de MySQL en `conexion.py`.
3. Crear el entorno virtual e instalar las librerías:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install flask mysql-connector-python
