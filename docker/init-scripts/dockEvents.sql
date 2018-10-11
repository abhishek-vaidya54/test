CREATE DATABASE  IF NOT EXISTS `dockEventsStaging` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `dockEventsStaging`;
-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: production-pipeline-aurora-us-east-1d.cij1ovqtmj95.us-east-1.rds.amazonaws.com    Database: dockEventsStaging
-- ------------------------------------------------------
-- Server version	5.7.12-log

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `appcrash_log`
--

DROP TABLE IF EXISTS `appcrash_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `appcrash_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `log` varchar(5000) NOT NULL,
  `dockID` char(12) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=329 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `data_events`
--

DROP TABLE IF EXISTS `data_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `sensorID` varchar(45) DEFAULT NULL,
  `firmware_version` varchar(45) DEFAULT NULL,
  `datarecord_count` int(20) DEFAULT NULL,
  `db_inserted_at` datetime DEFAULT NULL,
  `assignment_time` int(20) DEFAULT NULL,
  `filename` varchar(200) DEFAULT NULL,
  `dockID` varchar(45) DEFAULT NULL,
  `warehouseID` varchar(45) DEFAULT NULL,
  `athleteID` varchar(45) DEFAULT NULL,
  `clientID` varchar(45) DEFAULT NULL,
  `port` int(10) DEFAULT NULL,
  `sessionID` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29083 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `engagement_stats`
--

DROP TABLE IF EXISTS `engagement_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engagement_stats` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `athlete_id` int(11) NOT NULL,
  `total_days_worn` int(11) DEFAULT '0',
  `total_hours_worn` int(11) DEFAULT '0',
  `last_checkin` datetime DEFAULT NULL,
  `last_checkout` datetime DEFAULT NULL,
  `db_created_at` datetime DEFAULT NULL,
  `db_modified_at` datetime DEFAULT NULL,
  `days_worn_haptic_enabled` int(11) NOT NULL DEFAULT '0',
  `days_worn_haptic_disabled` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `athlete_id_UNIQUE` (`athlete_id`)
) ENGINE=InnoDB AUTO_INCREMENT=933 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `keepalive_events`
--

DROP TABLE IF EXISTS `keepalive_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `keepalive_events` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `dockID` varchar(45) DEFAULT NULL,
  `db_inserted_at` datetime DEFAULT NULL,
  `batt_percent` varchar(45) DEFAULT NULL,
  `charge_status` varchar(45) DEFAULT NULL,
  `clientID` varchar(50) DEFAULT NULL,
  `warehouseID` varchar(50) DEFAULT NULL,
  `dockIMEI` varchar(45) DEFAULT NULL,
  `enum_ports` varchar(100) DEFAULT NULL,
  `occupied_ports` varchar(100) DEFAULT NULL,
  `local_sensor_fw` int(11) DEFAULT NULL,
  `app_version` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=569713 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `monthly_safety`
--

DROP TABLE IF EXISTS `monthly_safety`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `monthly_safety` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `athlete_id` int(11) NOT NULL,
  `latest_safety_score` float NOT NULL DEFAULT '0',
  `monthly_score` float DEFAULT NULL,
  `db_modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `athlete_id_UNIQUE` (`athlete_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10938 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `raw_event_log`
--

DROP TABLE IF EXISTS `raw_event_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `raw_event_log` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) DEFAULT NULL,
  `dockID` varchar(45) DEFAULT NULL,
  `db_inserted_at` datetime NOT NULL,
  `event_blob` json DEFAULT NULL,
  `event_hash` varchar(40) NOT NULL DEFAULT '',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=743497 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sensor_events`
--

DROP TABLE IF EXISTS `sensor_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sensor_events` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `dockID` varchar(45) DEFAULT NULL,
  `clientID` varchar(45) DEFAULT NULL,
  `warehouseID` varchar(45) DEFAULT NULL,
  `assignment_time` int(20) DEFAULT NULL,
  `sensorID` varchar(45) DEFAULT NULL,
  `athleteID` varchar(45) DEFAULT NULL,
  `datarecord_count` int(20) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `db_inserted_at` datetime NOT NULL,
  `firmware_version` varchar(45) DEFAULT NULL,
  `sessionID` varchar(45) DEFAULT NULL,
  `datapage_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=215228 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `survey_events`
--

DROP TABLE IF EXISTS `survey_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `survey_events` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  `athleteID` varchar(45) DEFAULT NULL,
  `dockID` varchar(45) DEFAULT NULL,
  `survey_type` varchar(45) DEFAULT NULL,
  `response` varchar(45) DEFAULT NULL,
  `db_inserted_at` datetime DEFAULT NULL,
  `firmware_version` varchar(45) DEFAULT NULL,
  `clientID` varchar(50) DEFAULT NULL,
  `warehouseID` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2585 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'dockEventsStaging'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-11 12:29:37
