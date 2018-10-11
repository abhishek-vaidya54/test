CREATE DATABASE  IF NOT EXISTS `pipelineStaging` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `pipelineStaging`;
-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: production-pipeline-aurora-us-east-1d.cij1ovqtmj95.us-east-1.rds.amazonaws.com    Database: pipelineStaging
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
-- Table structure for table `activity`
--

DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entity_type` varchar(255) NOT NULL,
  `entity_id` int(11) NOT NULL,
  `action` varchar(255) NOT NULL,
  `before_state` text,
  `after_state` text,
  `user_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `db_created_at` datetime NOT NULL,
  `db_modified_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `activity_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `activity_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `athlete_group`
--

DROP TABLE IF EXISTS `athlete_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `athlete_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `client_id` int(11) NOT NULL,
  `warehouse_id` int(11) DEFAULT NULL,
  `db_created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `db_modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `description` text,
  `group_administrator` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`warehouse_id`),
  KEY `client_id` (`client_id`),
  KEY `warehouse_id` (`warehouse_id`),
  CONSTRAINT `athlete_group_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  CONSTRAINT `athlete_group_ibfk_2` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `binary_bucket_monitor`
--

DROP TABLE IF EXISTS `binary_bucket_monitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `binary_bucket_monitor` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `sensor_id` varchar(50) DEFAULT NULL,
  `athlete_id` varchar(50) DEFAULT NULL,
  `dock_id` varchar(50) DEFAULT NULL,
  `client_id` varchar(50) DEFAULT NULL,
  `warehouse_id` varchar(50) DEFAULT NULL,
  `firmware_version` varchar(50) DEFAULT NULL,
  `assignment_time` varchar(50) DEFAULT NULL,
  `session_id` varchar(50) NOT NULL,
  `db_created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `db_modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `file_size` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=71746 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `db_created_at` datetime NOT NULL,
  `db_modified_at` datetime NOT NULL,
  `prefix` varchar(255) NOT NULL,
  `guid` varchar(32) NOT NULL,
  `domain` varchar(255) DEFAULT NULL,
  `enable_processing` tinyint(1) NOT NULL DEFAULT '1',
  `account_lock_timeout` int(11) DEFAULT NULL,
  `dynamic_shift` tinyint(1) NOT NULL,
  `client_regex_code` varchar(255) DEFAULT NULL,
  `algo_version` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `domain` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `compliance_tracker`
--

DROP TABLE IF EXISTS `compliance_tracker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `compliance_tracker` (
  `Athlete_ID` varchar(8) NOT NULL,
  `Fuse_ID` varchar(255) DEFAULT NULL,
  `Client_ID` varchar(255) NOT NULL,
  `Date` varchar(50) NOT NULL,
  PRIMARY KEY (`Athlete_ID`,`Date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `db_created_at` datetime NOT NULL,
  `db_modified_at` datetime NOT NULL,
  `client_id` int(11) NOT NULL,
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `edison_id` int(11) NOT NULL,
  `device_label` int(11) NOT NULL,
  `hotspot_template` varchar(255) NOT NULL,
  `hotspot` int(11) DEFAULT NULL,
  `warehouse_id` int(11) DEFAULT NULL,
  `device_identifier` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `client_id` (`client_id`),
  KEY `warehouse_id` (`warehouse_id`),
  CONSTRAINT `device_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  CONSTRAINT `device_ibfk_2` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `email_domain`
--

DROP TABLE IF EXISTS `email_domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `email_domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `client_id` int(11) NOT NULL,
  `db_created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `email_domain_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `email_schedule`
--

DROP TABLE IF EXISTS `email_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `email_schedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `to_emails` text NOT NULL,
  `client_id` int(11) NOT NULL,
  `pattern` varchar(255) NOT NULL,
  `pilot_length` int(11) NOT NULL,
  `warehouse_id` int(11) DEFAULT NULL,
  `db_created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `db_modified_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `group_id` int(11) DEFAULT NULL,
  `job_function_id` int(11) DEFAULT NULL,
  `shift_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `client_id` (`client_id`),
  KEY `warehouse_id` (`warehouse_id`),
  KEY `email_schedule_ibfk_es` (`job_function_id`),
  KEY `email_schedule_ibfk_sh` (`shift_id`),
  KEY `email_schedule_ibfk_gp` (`group_id`),
  CONSTRAINT `email_schedule_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  CONSTRAINT `email_schedule_ibfk_2` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`),
  CONSTRAINT `email_schedule_ibfk_es` FOREIGN KEY (`job_function_id`) REFERENCES `job_function` (`id`),
  CONSTRAINT `email_schedule_ibfk_gp` FOREIGN KEY (`group_id`) REFERENCES `athlete_group` (`id`),
  CONSTRAINT `email_schedule_ibfk_sh` FOREIGN KEY (`shift_id`) REFERENCES `shifts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `db_created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `haptic_events`
--

DROP TABLE IF EXISTS `haptic_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `haptic_events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp_ms` bigint(20) DEFAULT NULL,
  `feedback_occured` tinyint(4) DEFAULT NULL,
  `event_type` varchar(45) DEFAULT NULL,
  `event_quantifier` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `setting_id` int(11) DEFAULT NULL,
  `session_id` varchar(45) DEFAULT NULL,
  `athlete_id` int(11) DEFAULT NULL,
  `sensor_id` varchar(45) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `warehouse_id` int(11) DEFAULT NULL,
  `dock_id` varchar(45) DEFAULT NULL,
  `assignment_time` varchar(45) DEFAULT NULL,
  `db_created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=544688 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `industrial_athlete`
--

DROP TABLE IF EXISTS `industrial_athlete`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `industrial_athlete` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `external_id` varchar(255) NOT NULL,
  `client_id` int(11) NOT NULL,
  `warehouse_id` int(11) DEFAULT NULL,
  `shift_id` int(11) DEFAULT NULL,
  `job_function_id` int(11) DEFAULT NULL,
  `schedule` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `height` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `hire_date` datetime DEFAULT NULL,
  `termination_date` datetime DEFAULT NULL,
  `prior_back_injuries` varchar(255) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `setting_id` int(11) DEFAULT NULL,
  `db_created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `db_modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `industrial_athlete_ibfk_2` (`job_function_id`),
  KEY `industrial_athlete_ibfk_3` (`warehouse_id`),
  KEY `industrial_athlete_ibfk_4` (`shift_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20169 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `job_function`
--

DROP TABLE IF EXISTS `job_function`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_function` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `warehouse_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `db_created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `db_modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `max_package_mass` float DEFAULT NULL,
  `color` varchar(255) DEFAULT NULL,
  `avg_package_weight` int(11) DEFAULT NULL,
  `description` text,
  `group_administrator` varchar(255) NOT NULL,
  `lbd_indicence` tinyint(1) DEFAULT NULL,
  `lbd_indicence_rate` int(11) DEFAULT NULL,
  `max_package_weight` int(11) DEFAULT NULL,
  `min_package_weight` int(11) DEFAULT NULL,
  `standard_score` float DEFAULT '70',
  PRIMARY KEY (`id`),
  KEY `warehouse_id` (`warehouse_id`),
  CONSTRAINT `job_function_ibfk_1` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=277 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `messages_surveys`
--

DROP TABLE IF EXISTS `messages_surveys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages_surveys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `engagement` varchar(30) NOT NULL,
  `days_worn` int(11) NOT NULL,
  `modal_type` varchar(50) NOT NULL,
  `content` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_eng_days_worn` (`engagement`,`days_worn`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `parser_monitor`
--

DROP TABLE IF EXISTS `parser_monitor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parser_monitor` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `sensor_id` varchar(50) DEFAULT NULL,
  `athlete_id` varchar(50) DEFAULT NULL,
  `dock_id` varchar(50) DEFAULT NULL,
  `client_id` varchar(50) DEFAULT NULL,
  `warehouse_id` varchar(50) DEFAULT NULL,
  `firmware_version` varchar(50) DEFAULT NULL,
  `assignment_time` varchar(50) DEFAULT NULL,
  `session_id` varchar(50) NOT NULL,
  `db_created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `db_modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `file_status` varchar(50) NOT NULL DEFAULT 'parsing',
  `message` varchar(50) DEFAULT NULL,
  `file_size` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `parser_monitor_uq_evt` (`file_status`,`session_id`)
) ENGINE=InnoDB AUTO_INCREMENT=59886 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `processed_file`
--

DROP TABLE IF EXISTS `processed_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `processed_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `status` enum('COMPLETE','PROCESSING','FAILED','TOO SMALL','UNKNOWN ATHLETE','REPROCESS') NOT NULL,
  `version` int(11) NOT NULL,
  `db_created_at` datetime NOT NULL,
  `db_modified_at` datetime NOT NULL,
  `last_error` text,
  `backtrace` text,
  `last_error_time` datetime DEFAULT NULL,
  `lateral_angle_exceeded_limit` int(11) NOT NULL,
  `lateral_vel_exceeded_limit` int(11) NOT NULL,
  `twist_vel_exceeded_limit` int(11) NOT NULL,
  `cropping_time` int(11) NOT NULL,
  `cropping_percentage` float NOT NULL,
  `work_time` int(11) NOT NULL,
  `sg_position_limit` int(11) NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `athlete_id` int(11) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `warehouse_id` int(11) DEFAULT NULL,
  `job_function_id` int(11) DEFAULT NULL,
  `sensor_id` varchar(45) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `setting_id` int(11) DEFAULT NULL,
  `session_id` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`version`),
  KEY `processed_files_start_end_index` (`start_time`,`end_time`,`version`,`status`)
) ENGINE=InnoDB AUTO_INCREMENT=145183 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `processed_haptic_file`
--

DROP TABLE IF EXISTS `processed_haptic_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `processed_haptic_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `status` enum('COMPLETE','PROCESSING','FAILED','UNKNOWN ATHLETE','REPROCESS') NOT NULL,
  `version` int(11) NOT NULL,
  `db_created_at` datetime NOT NULL,
  `db_modified_at` datetime NOT NULL,
  `modified_at` datetime DEFAULT NULL,
  `last_error` text,
  `backtrace` text,
  `bad_bends` int(11) DEFAULT NULL,
  `feedback_events` int(11) DEFAULT NULL,
  `last_error_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`version`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `risk`
--

DROP TABLE IF EXISTS `risk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `risk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `processed_file_id` int(11) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `avg_twist_velocity` int(11) DEFAULT NULL,
  `lift_rate` int(11) DEFAULT NULL,
  `max_flexion` int(11) DEFAULT NULL,
  `average_flexion` int(11) DEFAULT NULL,
  `max_lateral` int(11) DEFAULT NULL,
  `average_lateral` int(11) DEFAULT NULL,
  `max_lateral_velocity` float DEFAULT NULL,
  `max_moment` float DEFAULT NULL,
  `risk_score` float DEFAULT NULL,
  `db_created_at` datetime NOT NULL,
  `db_modified_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `processed_file_id` (`processed_file_id`),
  KEY `start_end_time_idx` (`start_time`,`end_time`),
  KEY `risk_start_end_index` (`start_time`,`end_time`),
  CONSTRAINT `risk_ibfk_1` FOREIGN KEY (`processed_file_id`) REFERENCES `processed_file` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28328 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `target_type` varchar(45) NOT NULL,
  `target_id` int(11) NOT NULL,
  `value` json DEFAULT NULL,
  `db_created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`pipeline`@`%`*/ /*!50003 TRIGGER `pipelineStaging`.`settings_AFTER_INSERT` AFTER INSERT ON `settings` FOR EACH ROW
BEGIN
	IF (new.target_type = 'industrial_athlete') THEN
		UPDATE industrial_athlete SET setting_id=(SELECT MAX(id) FROM `settings`) WHERE id=new.target_id;
	END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`pipeline`@`%`*/ /*!50003 TRIGGER `pipelineStaging`.`settings_BEFORE_UPDATE` BEFORE UPDATE ON `settings` FOR EACH ROW
BEGIN
  SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Update not allowed!';
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`pipeline`@`%`*/ /*!50003 TRIGGER `pipelineStaging`.`settings_BEFORE_DELETE` BEFORE DELETE ON `settings` FOR EACH ROW
BEGIN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Delete not allowed!';
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `shifts`
--

DROP TABLE IF EXISTS `shifts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shifts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `warehouse_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `shift_start` time NOT NULL,
  `shift_end` time NOT NULL,
  `db_created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `db_modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `color` varchar(255) DEFAULT NULL,
  `description` text,
  `group_administrator` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `warehouse_id` (`warehouse_id`),
  CONSTRAINT `shifts_ibfk_1` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=108 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `survey_question`
--

DROP TABLE IF EXISTS `survey_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `survey_question` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `question` varchar(400) NOT NULL,
  `option1` varchar(255) DEFAULT NULL,
  `option2` varchar(255) DEFAULT NULL,
  `option3` varchar(255) DEFAULT NULL,
  `option4` varchar(255) DEFAULT NULL,
  `db_inserted_at` timestamp NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tags` (
  `tag_id` int(11) DEFAULT NULL,
  `industrial_athlete_id` int(11) DEFAULT NULL,
  UNIQUE KEY `tag_id` (`tag_id`,`industrial_athlete_id`),
  KEY `industrial_athlete_id` (`industrial_athlete_id`),
  CONSTRAINT `tags_ibfk_1` FOREIGN KEY (`industrial_athlete_id`) REFERENCES `industrial_athlete` (`id`),
  CONSTRAINT `tags_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `client_id` int(11) NOT NULL,
  `db_created_at` datetime NOT NULL,
  `db_modified_at` datetime NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `warehouse_id` int(11) DEFAULT NULL,
  `is_locked` tinyint(1) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `brute_force_locked` tinyint(1) NOT NULL,
  `new_password_on_login` tinyint(1) DEFAULT NULL,
  `brute_force_locked_at` datetime DEFAULT NULL,
  `is_suspended` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `client_id` (`client_id`),
  KEY `user_warehouse_ibfk_1` (`warehouse_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  CONSTRAINT `user_warehouse_ibfk_1` FOREIGN KEY (`warehouse_id`) REFERENCES `warehouse` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `warehouse`
--

DROP TABLE IF EXISTS `warehouse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `warehouse` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `location` varchar(500) DEFAULT NULL,
  `db_created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `db_modified_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `prefered_timezone` varchar(100) NOT NULL DEFAULT '+00:00',
  `algo_version` int(11) DEFAULT NULL,
  `display_names` tinyint(1) NOT NULL DEFAULT '1',
  `utc_op_day_start` varchar(45) DEFAULT '00:00:00',
  `week_start` varchar(45) DEFAULT 'Sunday',
  `show_engagement` tinyint(1) NOT NULL DEFAULT '0',
  `update_engagement` tinyint(1) NOT NULL DEFAULT '1',
  `hide_judgement` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `client_id` (`client_id`),
  CONSTRAINT `warehouse_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'pipelineStaging'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-11 12:29:22
