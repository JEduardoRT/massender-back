-- Insertar datos en la tabla Acceso
INSERT INTO Acceso (ruta, descripcion, estado, fecha_insercion, usuario_insercion, parent_id)
VALUES 
('/dashboard', 'Inicio', 'A', NOW(), 0, NULL),
('/dashboard/reportes', 'Reportes', 'A', NOW(), 0, 1),
('/dashboard/empresas', 'Empresas', 'A', NOW(), 0, 1),
('/dashboard/pagos', 'Pagos', 'A', NOW(), 0, 1),
('/dashboard/destinatarios', 'Destinatarios', 'A', NOW(), 0, 1),
('/dashboard/destinatarios/filtros', 'Filtros', 'A', NOW(), 0, 5),
('/dashboard/destinatarios/:id/importar', 'Cargar Destinatarios', 'A', NOW(), 0, 5),
('/dashboard/campanias', 'Campañas', 'A', NOW(), 0, 1),
('/dashboard/campanias/creacion', 'Crear Campaña', 'A', NOW(), 0, 8);

-- Insertar datos en la tabla Rol
INSERT INTO Rol (descripcion, estado, fecha_insercion, usuario_insercion, scopes)
VALUES 
('SuperAdministrador', 'A', NOW(), 0, 'admin,user'),
('Administrador', 'A', NOW(), 0, 'user');
('Usuario', 'A', NOW(), 0, 'user');

-- Insertar datos en la tabla AccesoRol
INSERT INTO AccesoRol (acceso_id, rol_id, estado, fecha_insercion, usuario_insercion)
VALUES 
(1, 1, 'A', NOW(), 0),
(2, 1, 'A', NOW(), 0),
(3, 1, 'A', NOW(), 0),
(4, 1, 'A', NOW(), 0),
(5, 1, 'A', NOW(), 0),
(6, 1, 'A', NOW(), 0),
(7, 1, 'A', NOW(), 0),
(8, 1, 'A', NOW(), 0),
(9, 1, 'A', NOW(), 0),
(1, 2, 'A', NOW(), 0),
(2, 2, 'A', NOW(), 0),
(3, 2, 'A', NOW(), 0),
(4, 2, 'A', NOW(), 0),
(8, 2, 'A', NOW(), 0),
(1, 3, 'A', NOW(), 0),
(5, 3, 'A', NOW(), 0),
(6, 3, 'A', NOW(), 0),
(7, 3, 'A', NOW(), 0),
(8, 3, 'A', NOW(), 0),
(9, 3, 'A', NOW(), 0);

-- Insertar datos en la tabla Membresia
INSERT INTO Membresia (titulo, descripcion, dias_vigencia, estado, fecha_insercion, usuario_insercion)
VALUES 
('Plan Basic', 'Con el Plan Basic tendrás hasta 5K mensajes, ideal para probar nuestra plataforma y explorar las posibilidades del envío masivo de mensajes.', 30, 'A', NOW(), 0),
('Plan Premium', 'El siguiente nivel para expandir tus comunicaciones. El Plan Premium te permite enviar más de 100K mensajes. Ideal para una gran audiencia y campañas extensas.', 180, 'A', NOW(), 0),
('Plan VIP', 'Con el Plan VIP obtienes hasta 100K mensajes, perfecto para empresas que buscan una solución robusta y escalable para sus campañas.', 365, 'A', NOW(), 0);

-- Insertar datos en la tabla TablaPrecios
INSERT INTO TablaPrecios (descripcion, estado, fecha_insercion, usuario_insercion)
VALUES 
('Tabla de precios estándar', 'A', NOW(), 0);

-- Insertar datos en la tabla Precio
INSERT INTO Precio (membresia_id, tabla_precios_id, valor, estado, fecha_insercion, usuario_insercion)
VALUES 
(1, 1, 20.0, 'A', NOW(), 0),
(2, 1, 150.0, 'A', NOW(), 0),
(3, 1, 250.0, 'A', NOW(), 0);

-- Insertar datos en la tabla MedioPago
INSERT INTO MedioPago (descripcion, codigo, estado, fecha_insercion, usuario_insercion)
VALUES 
('Tarjeta de Crédito', 'TDC', 'A', NOW(), 0),
('Tarjeta de Débito', 'TDE', 'A', NOW(), 0),
('PayPal', 'PAY', 'A', NOW(), 0),
('Transferencia', 'TRA', 'A', NOW(), 0),
('Efectivo', 'EFE', 'A', NOW(), 0);

-- Insertar datos en la tabla Cliente
/*INSERT INTO Cliente (nombre, membresia_id, tabla_precios_id, medio_pago_id, fecha_ini_memb, fecha_fin_memb, estado, fecha_insercion, usuario_insercion)
VALUES 
('Cliente 1', 1, 1, 1, '2024-01-01', '2024-01-31', 'A', NOW(), 0),
('CONECEL CLARO', 3, 1, 4, '2024-01-01', '2024-12-31', 'A', NOW(), 0);*/

-- Insertar datos en la tabla ListaDestinatarios
/*INSERT INTO ListaDestinatarios (nombre, cliente_id, estado, fecha_insercion, usuario_insercion)
VALUES 
('Lista General', 1, 'A', NOW(), 0),
('Lista General', 2, 'A', NOW(), 0),
('Lista Back', 2, 'A', NOW(), 0);*/

-- Insertar datos en la tabla Destinatario
/*INSERT INTO Destinatario (nombre_completo, correo, telefono, metadatos, lista_id, estado, fecha_insercion, usuario_insercion)
VALUES 
('Jandry Rodriguez', 'jandry_eduardo@hotmail.com', '593993879910', NULL, 1, 'A', NOW(), 0),
('Gabriel Castro', 'gabriel@example.com', '59234567890', '{"Edad":23}', 1, 'A', NOW(), 0),
('Alexis Loor', 'alexis@example.com', '51234567890', '{"Edad":22}', 1, 'A', NOW(), 0),
('Keneth Pacheco', 'keneth@example.com', '11234567890', '{"Ciudad":"Guayaquil"}', 1, 'A', NOW(), 0),
('Jandry Rodriguez', 'jandry_eduardo@hotmail.com', '593993879910', '{"Ciudad":"Guayaquil"}', 2, 'A', NOW(), 0),
('Gabriel Castro', 'gabriel@example.com', '593934567890', '{"Ciudad":"Guayaquil", "Edad": 22}', 2, 'A', NOW(), 0),
('Alexis Loor', 'alexis@example.com', '593934567890', NULL, 2, 'A', NOW(), 0),
('Keneth Pacheco', 'keneth@example.com', '593934567890', '{"Edad":24}', 2, 'A', NOW(), 0),
('Keneth Pacheco', 'keneth@example.com', '593934567890', '{"Ciudad":"Guayaquil"}', 3, 'A', NOW(), 0),
('Jandry Rodriguez', 'jandry_eduardo@hotmail.com', '593993879910', NULL, 3, 'A', NOW(), 0);*/

-- Insertar datos en la tabla Usuario
INSERT INTO Usuario (username, nombre_completo, password, correo, rol_id, cliente_id, telefono, estado, fecha_insercion, usuario_insercion)
VALUES 
('hang.admin', 'SuperAdmin Hangaroa', '$2a$15$ush5/cXx0mjrp5Ujmm3aHuey/dGsiL/1FRvZhLJb3/XmFhgMiTIy2', 'admin@hangaroa.com.ec', 1, NULL, '593993879910', 'A', NOW(), 0);

-- Insertar datos en la tabla Campania
/*INSERT INTO Campania (mensaje_id, nombre, fecha_ini, fecha_fin, activo, cliente_id, estado, fecha_insercion, usuario_insercion)
VALUES 
(NULL, 'Campania 1 Cliente 1', '2024-01-01', '2024-01-08', TRUE, 1, 'A', NOW(), 0),
(NULL, 'Campania 1 CLARO', '2024-02-01', '2024-02-28', TRUE, 2, 'A', NOW(), 0);*/

-- Insertar datos en la tabla Mensaje
/*INSERT INTO Mensaje (campania_id, texto, multimedia, estado, fecha_insercion, usuario_insercion)
VALUES 
(1, 'Texto del mensaje 1', '{"images":[{"alt": "Imagen1", "url": "url a imagen1"}]}', 'A', NOW(), 0),
(2, 'Texto del mensaje 2', '{"images":[{"alt": "Imagen1", "url": "url a imagen1"}], "videos":[{"alt": "Video1", "url": "url a video1"}]}', 'A', NOW(), 0);*/

-- Insertar datos en la tabla ListaDestinatariosCampania
/*INSERT INTO ListaDestinatariosCampania (campania_id, lista_destinatarios_id, estado, fecha_insercion, usuario_insercion)
VALUES 
(1, 1, 'A', NOW(), 0),
(2, 2, 'A', NOW(), 0);*/

-- Insertar datos en la tabla UsuarioCampania
/*INSERT INTO UsuarioCampania (usuario_id, campania_id, estado, fecha_insercion, usuario_insercion)
VALUES 
(2, 1, 'A', NOW(), 0),
(3, 2, 'A', NOW(), 0);*/

-- Insertar datos en la tabla Pago
/*INSERT INTO Pago (cliente_id, membresia_id, fecha_pago, pagado, cod_medio_pago, estado, fecha_insercion, usuario_insercion)
VALUES 
(1, 1, '2024-06-15', TRUE, 'TDC', 'A', NOW(), 0),
(2, 2, '2024-06-15', FALSE, 'TRA', 'A', NOW(), 0);*/
