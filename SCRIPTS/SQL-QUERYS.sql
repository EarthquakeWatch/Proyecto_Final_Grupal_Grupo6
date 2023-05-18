DROP DATABASE IF EXISTS sismos;
CREATE DATABASE IF NOT EXISTS sismos;
USE sismos;

DROP TABLE IF EXISTS  USA;
CREATE TABLE IF NOT EXISTS USA (
  id VARCHAR(200) NOT NULL,
  Magnitud FLOAT NOT NULL,
  properties_place VARCHAR(200),
  Primer_reg VARCHAR(200) NOT NULL,
  Ultimo_registro VARCHAR(200) NOT NULL,
  properties_felt FLOAT,
  cdi FLOAT,
  mmi FLOAT,
  alert VARCHAR(200),
  Posibilidad_tsunami INT NOT NULL,
  Importancia_evento INT NOT NULL,
  ids VARCHAR(200),
  nst FLOAT,
  Dist_Horizontal_epicentro FLOAT,
  properties_rms FLOAT,
  Brecha_azimutal FLOAT,
  properties_type VARCHAR(200),
  geometry_type VARCHAR(200),
  Longitud FLOAT NOT NULL,
  Latitud FLOAT NOT NULL,
  Profundidad FLOAT NOT NULL,
  estado VARCHAR(200)
);




DROP TABLE IF EXISTS  JAPON;
CREATE TABLE IF NOT EXISTS JAPON (
  id VARCHAR(200),
  Magnitud FLOAT,
  Ubicación VARCHAR(200),
  `Primer Registro` VARCHAR(200),
  `Último Registro` VARCHAR(200),
  `properties.felt` FLOAT,
  `properties.cdi` FLOAT,
  `properties.mmi` FLOAT,
  `properties.tsunami` INT,
  `properties.sig` INT,
  `properties.net` VARCHAR(200),
  `properties.ids` VARCHAR(200),
  `properties.nst` FLOAT,
  `properties.dmin` FLOAT,
  `properties.rms` FLOAT,
  `properties.gap` FLOAT,
  `geometry.coordinates` VARCHAR(200),
  `Longitud (grados)` FLOAT,
  `Latitud (grados)` FLOAT,
  `Profundidad (km)` FLOAT
);


DROP TABLE IF EXISTS  PERU;
CREATE TABLE IF NOT EXISTS Peru (
  id VARCHAR(200),
  Magnitud FLOAT,
  `properties.place` VARCHAR(200),
  `Primer reg` VARCHAR(200),
  `Ultimo registro` VARCHAR(200),
  felt FLOAT,
  cdi FLOAT,
  mmi FLOAT,
  `Posibilidad tsunami` INT,
  `Importancia del evento` INT,
  nst FLOAT,
  `Dist Horizontal epicentro` FLOAT,
  RMS FLOAT,
  `Brecha azimutal` FLOAT,
  Longitud FLOAT,
  Latitud FLOAT,
  Profundidad FLOAT,
  Pais VARCHAR(200)
);


