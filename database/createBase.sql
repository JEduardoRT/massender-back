CREATE TABLE Acceso (
    acceso_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ruta CHAR(100) NOT NULL,
    descripcion CHAR(50) NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL
);

CREATE TABLE Rol (
    rol_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    descripcion CHAR(30) NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL
);

CREATE TABLE AccesoRol (
    acc_rol_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    acceso_id INT NOT NULL,
    rol_id INT NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL,
    FOREIGN KEY (acceso_id) REFERENCES Acceso(acceso_id),
    FOREIGN KEY (rol_id) REFERENCES Rol(rol_id)
);

CREATE TABLE Membresia (
    membresia_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(20) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    dias_vigencia INT NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL
);

CREATE TABLE TablaPrecios (
    tabla_precios_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    descripcion CHAR(50) NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL
);

CREATE TABLE MedioPago (
    medio_pago_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    descripcion CHAR(50) NOT NULL,
    codigo CHAR(3) NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL
);

CREATE TABLE Cliente (
    cliente_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre CHAR(20) NOT NULL,
    membresia_id INT NOT NULL,
    tabla_precios_id INT NOT NULL,
    medio_pago_id INT NOT NULL,
    fecha_ini_memb DATE,
    fecha_fin_memb DATE,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL,
    FOREIGN KEY (membresia_id) REFERENCES Membresia(membresia_id),
    FOREIGN KEY (tabla_precios_id) REFERENCES TablaPrecios(tabla_precios_id),
    FOREIGN KEY (medio_pago_id) REFERENCES MedioPago(medio_pago_id)
);

CREATE TABLE Usuario (
    usuario_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username CHAR(10) NOT NULL,
    nombre_completo CHAR(50) NOT NULL,
    password CHAR(50) NOT NULL,
    correo CHAR(30) NOT NULL,
    rol_id INT NOT NULL,
    cliente_id INT,
    telefono VARCHAR(15) NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL,
    FOREIGN KEY (rol_id) REFERENCES Rol(rol_id),
    FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id)
);

CREATE TABLE UsuarioCampania (
    usuario_camp_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    campania_id INT NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(usuario_id),
    FOREIGN KEY (campania_id) REFERENCES Campania(campania_id)
);

CREATE TABLE Precio (
    precio_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    membresia_id INT NOT NULL,
    tabla_precios_id INT NOT NULL,
    valor DOUBLE NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL,
    FOREIGN KEY (membresia_id) REFERENCES Membresia(membresia_id),
    FOREIGN KEY (tabla_precios_id) REFERENCES TablaPrecios(tabla_precios_id)
);

CREATE TABLE Pago (
    pago_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    membresia_id INT NOT NULL,
    fecha_pago DATE NOT NULL,
    pagado BOOLEAN NOT NULL,
    cod_medio_pago VARCHAR(3) NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL,
    FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id),
    FOREIGN KEY (membresia_id) REFERENCES Membresia(membresia_id)
);

CREATE TABLE Campania (
    campania_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre CHAR(50) NOT NULL,
    fecha_ini DATE,
    fecha_fin DATE,
    activo BOOLEAN NOT NULL,
    cliente_id INT NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL,
    FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id)
);

CREATE TABLE ListaDestinatarios (
    lista_destinatarios_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre CHAR(50) NOT NULL,
    cliente_id INT NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL,
    FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id)
);

CREATE TABLE Destinatario (
    destinatario_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_completo CHAR(20) NOT NULL,
    correo VARCHAR(50) NOT NULL,
    telefono VARCHAR(15) NULL,
    metadatos VARCHAR(500) NULL,
    lista_id INT NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL,
    FOREIGN KEY (lista_id) REFERENCES ListaDestinatarios(lista_destinatarios_id)
);

CREATE TABLE Mensaje (
    mensaje_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    campania_id INT NOT NULL,
    texto VARCHAR(60000) NOT NULL,
    multimedia VARCHAR(2000) NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL,
    FOREIGN KEY (campania_id) REFERENCES Campania(campania_id)
);

CREATE TABLE ListaDestinatariosCampania (
    lista_dest_camp_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    campania_id INT NOT NULL,
    lista_destinatarios_id INT NOT NULL,
    estado CHAR(1) NOT NULL,
    fecha_insercion DATETIME NOT NULL,
    fecha_modificacion DATETIME NULL,
    usuario_insercion INT NOT NULL,
    usuario_modificacion INT NULL,
    FOREIGN KEY (campania_id) REFERENCES Campania(campania_id),
    FOREIGN KEY (lista_destinatarios_id) REFERENCES ListaDestinatarios(lista_destinatarios_id)
);
