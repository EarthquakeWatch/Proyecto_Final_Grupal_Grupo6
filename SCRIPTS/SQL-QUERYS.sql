USE sismos;

DROP TABLE IF EXISTS  USA;
CREATE TABLE IF NOT EXISTS USA(
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
Codigo VARCHAR(250) NOT NULL,
Magnitud FLOAT,
place VARCHAR(250),
Fecha_Hora DATE NOT NULL,
updated DATE NOT NULL,
cdi FLOAT,
status VARCHAR(250),
tsunami INT,
sig INT,
ids VARCHAR(250),
nst FLOAT,
dmin FLOAT,
rms FLOAT,
gap FLOAT,
Longitud DOUBLE,
Latitud DOUBLE,
Profundidad FLOAT
);


DROP TABLE IF EXISTS  JAPON;
CREATE TABLE IF NOT EXISTS JAPON(
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
Fecha_Hora DATE NOT NULL,
Latitud DOUBLE,
Longitud DOUBLE,
profundidad FLOAT,
Magnitud FLOAT,
Ubicacion VARCHAR(250)
);


DROP TABLE IF EXISTS  PERU;
CREATE TABLE IF NOT EXISTS PERU(
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
Fecha_Hora DATE NOT NULL,
Latitud DOUBLE,
Longitud DOUBLE,
profundidad FLOAT,
Magnitud FLOAT
);
