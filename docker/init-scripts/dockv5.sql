CREATE DATABASE  IF NOT EXISTS `dockv5` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `dockv5`;
-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: dockv5.cij1ovqtmj95.us-east-1.rds.amazonaws.com    Database: dockv5
-- ------------------------------------------------------
-- Server version	5.6.10

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('e79ea302e61f');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `config`
--

DROP TABLE IF EXISTS `config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dock_id` varchar(45) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `warehouse_id` int(11) DEFAULT NULL,
  `deployment_stage` varchar(45) DEFAULT 'staging',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dock_id_UNIQUE` (`dock_id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `config`
--

LOCK TABLES `config` WRITE;
/*!40000 ALTER TABLE `config` DISABLE KEYS */;
INSERT INTO `config` VALUES (1,'E423540B64BE',33,45,'prod'),(2,'E423540B65F3',33,45,'prod'),(3,'E423540B65F2',33,45,'prod'),(4,'E423540B687C',34,46,'prod'),(5,'E423540B687B',34,46,'prod'),(6,'E423540B65EE',33,45,'prod'),(9,'E423540B5DFC',34,46,'prod'),(12,'E423540B6879',34,46,'prod'),(19,'E423540B687D',32,43,'prod'),(21,'E423540B65EB',33,45,'dev'),(24,'E423540B5DFE',34,46,'prod'),(26,'E423540B5E00',33,45,'prod'),(27,'E423540B5DFF',34,46,'prod'),(30,'E423540B5DFD',33,45,'prod'),(33,'E423540B687A',33,45,'dev'),(35,'E423540B65F0',33,45,'dev'),(39,'E423540B5EFE',32,44,'prod'),(40,'E423540B5EF6',32,44,'prod'),(41,'E423540B5EF7',32,44,'prod'),(42,'E423540B5EFD',32,44,'prod'),(43,'E423540B5EFB',32,44,'prod'),(44,'E423540B5EFC',32,44,'prod'),(45,'E423540B5EFF',32,44,'prod'),(46,'E423540B5EF8',32,44,'prod'),(47,'E423540B5EF9',32,44,'prod'),(48,'E423540B5EFA',32,44,'prod'),(49,'E423540B6877',32,44,'prod'),(50,'E423540B6876',32,44,'prod'),(51,'E423540B6874',32,44,'prod'),(52,'E423540B6875',32,44,'prod'),(55,'E423540B5E03',32,43,'prod'),(56,'E423540B5E01',32,43,'prod'),(57,'E423540B5E02',32,43,'prod'),(58,'E423540B6623',32,43,'prod'),(59,'E423540B5E05',32,43,'prod'),(60,'E423540B6620',32,43,'prod'),(61,'E423540B6624',32,43,'prod'),(62,'E423540B6625',32,43,'prod'),(63,'E423540B6621',32,43,'prod'),(64,'E423540B661E',32,43,'prod'),(65,'E423540B661D',32,43,'prod'),(66,'E423540B661F',32,43,'prod'),(67,'E423540B6622',32,43,'prod'),(68,'E423540B661C',32,43,'prod'),(69,'E423540B5E04',33,45,'prod'),(70,'E423540B5EE0',33,45,'prod');
/*!40000 ALTER TABLE `config` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-07-20 13:35:05
