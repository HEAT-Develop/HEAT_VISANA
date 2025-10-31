-- MySQL dump 10.13  Distrib 8.0.38, for macos14 (x86_64)
--
-- Host: localhost    Database: hyb2_tir_lv3
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `meshes`
--

DROP TABLE IF EXISTS `meshes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meshes` (
  `mesh_id` char(36) NOT NULL DEFAULT (uuid()),
  `asteroid_id` char(36) NOT NULL,
  `mesh_name` varchar(255) NOT NULL,
  `mesh_uri` varchar(2048) NOT NULL,
  `polygon_count` int unsigned NOT NULL,
  `vertex_count` int unsigned DEFAULT NULL,
  `format` varchar(32) DEFAULT NULL,
  `checksum_sha256` char(64) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`mesh_id`),
  UNIQUE KEY `uq_mesh_per_asteroid` (`asteroid_id`,`mesh_name`),
  KEY `idx_mesh_asteroid` (`asteroid_id`),
  CONSTRAINT `fk_mesh_asteroid` FOREIGN KEY (`asteroid_id`) REFERENCES `asteroids` (`asteroid_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meshes`
--

LOCK TABLES `meshes` WRITE;
/*!40000 ALTER TABLE `meshes` DISABLE KEYS */;
INSERT INTO `meshes` VALUES ('4885359d-5fd4-4631-a3a5-7e1dd93d4099','7b5c3101-f9da-4ebe-b4c0-56e354c1f5cf','hyb2_tir_20181231_155248_l3.vtk\',)','(\'/Volumes/HEAT_VISANA/HEAT_VISANA/HEAT_VISANA/src/pages/files/spc/800k/hyb2_tir_20181231_155248_l3.vtk\',)',786432,396294,'vtk\',)','None','2018-12-30 21:52:48'),('56392b5c-c528-4cb8-99fe-691d75de1811','83cb30ab-68af-46dc-8942-bdd8917dcc06','patched.vtk','/Volumes/HEAT_VISANA/HEAT_VISANA/patched.vtk',786432,396294,'vtk','None','2019-01-21 06:00:00');
/*!40000 ALTER TABLE `meshes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-31 17:29:50
