CREATE DATABASE `generator`;

USE `generator`;

DROP TABLE IF EXISTS `mytable`;

CREATE TABLE `mytable` (
  `id` bigint(20) DEFAULT NULL,
  `cur_pair` varchar(10) DEFAULT NULL,
  `direction` varchar(5) DEFAULT NULL,
  `status` varchar(15) DEFAULT NULL,
  `date` bigint(20) DEFAULT NULL,
  `init_px` double DEFAULT NULL,
  `init_volume` double DEFAULT NULL,
  `fill_px` double DEFAULT NULL,
  `fill_volume` double DEFAULT NULL,
  `desc` varchar(4) DEFAULT NULL,
  `tags` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;