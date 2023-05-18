DROP DATABASE IF EXISTS sismos;
CREATE DATABASE IF NOT EXISTS sismos;
USE sismos;

DROP TABLE IF EXISTS  USA;
CREATE TABLE IF NOT EXISTS USA (
  id VARCHAR(255),
  Magnitud VARCHAR(255),
  Place VARCHAR(255),
  `Primer Registro` VARCHAR(255),
  `Ultimo registro` VARCHAR(255),
  Felt VARCHAR(255),
  cdi VARCHAR(255),
  mmi VARCHAR(255),
  `Posibilidad tsunami` VARCHAR(255),
  `Importancia del evento` VARCHAR(255),
  ids VARCHAR(255),
  nst VARCHAR(255),
  `Dist Horizontal epicentro` VARCHAR(255),
  RMS VARCHAR(255),
  `Brecha azimutal` VARCHAR(255),
  Longitud VARCHAR(255),
  Latitud VARCHAR(255),
  Profundidad VARCHAR(255),
  estado VARCHAR(255)
);




DROP TABLE IF EXISTS  JAPON;
CREATE TABLE IF NOT EXISTS JAPON (
  id VARCHAR(255),
  Magnitud VARCHAR(255),
  Place VARCHAR(255),
  `Primer Registro` VARCHAR(255),
  `Ultimo registro` VARCHAR(255),
  Felt VARCHAR(255),
  cdi VARCHAR(255),
  mmi VARCHAR(255),
  `Posibilidad tsunami` VARCHAR(255),
  `Importancia del evento` VARCHAR(255),
  ids VARCHAR(255),
  nst VARCHAR(255),
  `Dist Horizontal epicentro` VARCHAR(255),
  RMS VARCHAR(255),
  `Brecha azimutal` VARCHAR(255),
  Longitud VARCHAR(255),
  Latitud VARCHAR(255),
  Profundidad VARCHAR(255),
  Pais VARCHAR(255)
);



DROP TABLE IF EXISTS  PERU;
CREATE TABLE IF NOT EXISTS PERU (
  id VARCHAR(255),
  Magnitud VARCHAR(255),
  Place VARCHAR(255),
  `Primer Registro` VARCHAR(255),
  `Ultimo registro` VARCHAR(255),
  Felt VARCHAR(255),
  cdi VARCHAR(255),
  mmi VARCHAR(255),
  `Posibilidad tsunami` VARCHAR(255),
  `Importancia del evento` VARCHAR(255),
  ids VARCHAR(255),
  nst VARCHAR(255),
  `Dist Horizontal epicentro` VARCHAR(255),
  RMS VARCHAR(255),
  `Brecha azimutal` VARCHAR(255),
  Longitud VARCHAR(255),
  Latitud VARCHAR(255),
  Profundidad VARCHAR(255),
  Pais VARCHAR(255)
);



