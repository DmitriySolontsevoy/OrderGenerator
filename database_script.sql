CREATE DATABASE `generator`;

USE `generator`;

DROP TABLE IF EXISTS `mytable`;

CREATE TABLE `mytable` (
  `id` varchar(20) NOT NULL,
  `currency_pair` tinyint(4) DEFAULT NULL,
  `direction` tinyint(4) DEFAULT NULL,
  `status` tinyint(4) NOT NULL,
  `date` bigint(20) DEFAULT NULL,
  `init_px` double DEFAULT NULL,
  `init_volume` double DEFAULT NULL,
  `fill_px` double DEFAULT NULL,
  `fill_volume` double DEFAULT NULL,
  `desc` varchar(4) DEFAULT NULL,
  `tags` varchar(45) DEFAULT NULL,
  `zone` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`,`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;