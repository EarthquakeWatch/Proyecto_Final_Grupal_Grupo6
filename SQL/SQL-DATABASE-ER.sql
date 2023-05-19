USE SISMOS;

DROP TABLE IF EXISTS SISMOS;
CREATE TABLE IF NOT EXISTS SISMOS(
ID              INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
Identificacion  VARCHAR(255),
Fecha 			DATETIME,
Magnitud 		FLOAT,
Longitud 		FLOAT,
Latitud 		FLOAT,
Profundidad		FLOAT,
ID_pais			INT NOT NULL,
ID_Location		INT NOT NULL,
ID_Parametros	INT NOT NULL
);


DROP TABLE IF EXISTS Parametros;
CREATE TABLE IF NOT EXISTS Parametros(
ID_Parametros 				INT NOT NULL PRIMARY KEY,
Felt 						FLOAT,
CDI 						FLOAT,
MMI 						FLOAT,
Dist_Horizontal_epicentro 	FLOAT,
Brecha_azimutal 			FLOAT,
Posibilidad_Tsunami 		INT,
Importancia_del_evento  	INT,
place 						VARCHAR(255),
Ids 						VARCHAR (255),
nst 						FLOAT,
RMS	 						FLOAT
);


DROP TABLE IF EXISTS Paises;
CREATE TABLE IF NOT EXISTS Paises(
ID_pais 	INT NOT NULL PRIMARY KEY,
Pais 		VARCHAR(255)
);


DROP TABLE IF EXISTS Locations;
CREATE TABLE IF NOT EXISTS Locations(
ID_Location 		INT NOT NULL PRIMARY KEY,
Prov_Est_Prefct 	VARCHAR(255)
);





