-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
--
-- Host: localhost    Database: calendario
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `etiquetas`
--

CREATE SCHEMA calendario;

USE calendario;

DROP TABLE IF EXISTS `etiquetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `etiquetas` (
  `id_etiqueta` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  PRIMARY KEY (`id_etiqueta`),
  UNIQUE KEY `id_etiqueta` (`id_etiqueta`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `etiquetas`
--

LOCK TABLES `etiquetas` WRITE;
/*!40000 ALTER TABLE `etiquetas` DISABLE KEYS */;
INSERT INTO `etiquetas` VALUES (1,'amigos'),(2,'reunion'),(3,'celebracion'),(4,'familia'),(5,'celebracion'),(6,'cumpleaños'),(7,'salud'),(8,'turno'),(9,'upateco'),(10,'universidad'),(11,'examen'),(12,'clase'),(13,'upateco'),(14,'universidad'),(15,'upateco'),(16,'clase'),(17,'universidad'),(18,'unsa'),(19,'universidad'),(20,'unsa'),(21,'examen'),(22,'tarjeta');
/*!40000 ALTER TABLE `etiquetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventos`
--

DROP TABLE IF EXISTS `eventos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos` (
  `id_evento` int unsigned NOT NULL AUTO_INCREMENT,
  `titulo` varchar(50) NOT NULL,
  `fecha_hora` datetime NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `duracion` smallint NOT NULL,
  `recordatorio` datetime DEFAULT NULL,
  `id_importancia` tinyint unsigned DEFAULT NULL,
  PRIMARY KEY (`id_evento`),
  UNIQUE KEY `id_evento` (`id_evento`),
  KEY `fk_importancia` (`id_importancia`),
  CONSTRAINT `fk_importancia` FOREIGN KEY (`id_importancia`) REFERENCES `importancias` (`id_importancia`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos`
--

LOCK TABLES `eventos` WRITE;
/*!40000 ALTER TABLE `eventos` DISABLE KEYS */;
INSERT INTO `eventos` VALUES (1,'Día del amigo','2023-07-20 20:00:00','Reunión con amigos para celebrar el día.',120,NULL,1),(2,'Cumpleaños de Rodo','2023-07-20 12:00:00','Se celebra el cumpleaños de Rodo en su casa.',120,'2023-07-19 22:01:00',1),(3,'Turno con dentista','2023-07-06 17:40:00','Turno reservado con la dentista para limpieza y chequeo general.',30,'2023-07-06 15:00:00',2),(4,'Desafío de Algorítmica','2023-07-14 09:00:00','Realizar el desafío de algorítmica disponible en la plataforma',60,'2023-07-13 20:15:00',2),(5,'Clase de Alogrítmica','2023-07-19 17:00:00','Conectarse a la sala de zoom de la clase de la materia algorítmica.',130,'2023-07-14 16:30:00',1),(6,'Clase de Programación 2','2023-07-14 08:30:00','Conectarse a la sala de zoom de la clase de la materia programación 2.',180,'2023-07-14 08:00:00',1),(7,'Final de POO','2023-07-27 08:00:00','Exámen final de programación orientada a objetos.',120,NULL,2),(8,'Final de SC','2023-07-28 10:00:00','Exámen final de sistemas de computación',120,NULL,2),(9,'Vencimiento de tarjeta','2023-08-10 00:00:00','Fecha límite para abonar el pago de la la tarjeta de cŕedito',0,NULL,1);
/*!40000 ALTER TABLE `eventos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eventos_etiquetas`
--

DROP TABLE IF EXISTS `eventos_etiquetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventos_etiquetas` (
  `id_evento_etiqueta` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `id_evento` int unsigned DEFAULT NULL,
  `id_etiqueta` tinyint unsigned DEFAULT NULL,
  PRIMARY KEY (`id_evento_etiqueta`),
  UNIQUE KEY `id_evento_etiqueta` (`id_evento_etiqueta`),
  KEY `fk_eventos` (`id_evento`),
  KEY `fk_etiquetas` (`id_etiqueta`),
  CONSTRAINT `fk_etiquetas` FOREIGN KEY (`id_etiqueta`) REFERENCES `etiquetas` (`id_etiqueta`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_eventos` FOREIGN KEY (`id_evento`) REFERENCES `eventos` (`id_evento`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventos_etiquetas`
--

LOCK TABLES `eventos_etiquetas` WRITE;
/*!40000 ALTER TABLE `eventos_etiquetas` DISABLE KEYS */;
INSERT INTO `eventos_etiquetas` VALUES (1,1,1),(2,1,2),(3,1,3),(4,2,4),(5,2,5),(6,2,6),(7,3,7),(8,3,8),(9,4,9),(10,4,10),(11,4,11),(12,5,12),(13,5,13),(14,5,14),(15,6,15),(16,6,16),(17,6,17),(18,7,18),(19,7,19),(20,8,20),(21,8,21),(22,9,22);
/*!40000 ALTER TABLE `eventos_etiquetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `importancias`
--

DROP TABLE IF EXISTS `importancias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `importancias` (
  `id_importancia` tinyint unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  PRIMARY KEY (`id_importancia`),
  UNIQUE KEY `id_importancia` (`id_importancia`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `importancias`
--

LOCK TABLES `importancias` WRITE;
/*!40000 ALTER TABLE `importancias` DISABLE KEYS */;
INSERT INTO `importancias` VALUES (1,'NORMAL'),(2,'IMPORTANTE'),(3,'URGENTE');
/*!40000 ALTER TABLE `importancias` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-19 22:35:13
