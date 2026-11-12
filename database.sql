CREATE DATABASE IF NOT EXISTS agenda_finanzas;
USE agenda_finanzas;

DROP TABLE IF EXISTS movimientos;
DROP TABLE IF EXISTS gastos_fijos;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS medios_pago;

CREATE TABLE categorias (
    categoria_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL DEFAULT '' UNIQUE
);

CREATE TABLE medios_pago (
    medio_pago_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30) NOT NULL DEFAULT '' UNIQUE
);

CREATE TABLE movimientos (
    movimiento_id INT PRIMARY KEY AUTO_INCREMENT,
    tipo ENUM('Ingreso', 'Gasto', 'Inversión') NOT NULL DEFAULT 'Gasto',
    monto DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    fecha BIGINT NOT NULL DEFAULT 0,
    categoria_id INT NOT NULL DEFAULT 0,
    medio_pago_id INT NOT NULL DEFAULT 0,
    descripcion VARCHAR(60) NOT NULL DEFAULT ''
);

CREATE TABLE gastos_fijos (
    gasto_fijo_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(60) NOT NULL DEFAULT '',
    monto_estimado DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    dia_vencimiento INT NOT NULL DEFAULT 1,
    categoria_id INT NOT NULL DEFAULT 0,
    ultimo_mes_pagado VARCHAR(7) NOT NULL DEFAULT ''
);

INSERT INTO categorias (nombre) VALUES 
('Sueldo'), ('Kiosco'), ('Ocio'), ('Comida / Supermercado'), 
('Servicios / Alquiler'), ('Vehículos'), ('Salud / Gimnasio'), ('Ahorro / Inversión');

INSERT INTO medios_pago (nombre) VALUES 
('Efectivo'), ('Mercado Pago'), ('Banco / Transferencia'), ('Tarjeta de Crédito'), ('Tarjeta de Débito');

INSERT INTO movimientos (tipo, monto, fecha, categoria_id, medio_pago_id, descripcion) VALUES 
('Ingreso', 500000.00, 1790846400, 1, 3, 'Cobro del mes'),
('Gasto', 2500.00, 1793644200, 2, 1, 'Alfajor y Coca'),
('Inversión', 1500.00, 1794164280, 8, 2, 'Invertí en la app InvertirOnline');

INSERT INTO gastos_fijos (nombre, monto_estimado, dia_vencimiento, categoria_id, ultimo_mes_pagado) VALUES 
('Suscripción Claude', 20000.00, 5, 5, ''),
('Internet Fibra', 25000.00, 10, 5, '');