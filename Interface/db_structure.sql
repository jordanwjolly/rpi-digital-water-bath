-- phpMyAdmin SQL Dump
-- version 4.0.10.5
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 25, 2014 at 12:29 AM
-- Server version: 5.5.40-cll
-- PHP Version: 5.4.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `willseph_thermostat`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth`
--

CREATE TABLE IF NOT EXISTS `auth` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `salt` char(32) NOT NULL,
  `ip` varchar(128) NOT NULL,
  `valid` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=36 ;

-- --------------------------------------------------------

--
-- Table structure for table `controllers`
--

CREATE TABLE IF NOT EXISTS `controllers` (
  `id` varchar(8) NOT NULL,
  `name` varchar(128) NOT NULL,
  `hash` char(128) NOT NULL,
  `salt` char(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sensors`
--

CREATE TABLE IF NOT EXISTS `sensors` (
  `id` varchar(8) NOT NULL,
  `name` varchar(128) NOT NULL,
  `hash` char(128) NOT NULL,
  `salt` char(32) NOT NULL,
  `last_update` int(11) NOT NULL,
  `temperature` float NOT NULL,
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

CREATE TABLE IF NOT EXISTS `settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `compressor_mode` enum('off','cool','heat','auto') NOT NULL DEFAULT 'off',
  `temperature_max` float NOT NULL DEFAULT '75',
  `temperature_min` float NOT NULL,
  `fan_mode` enum('on','auto') NOT NULL DEFAULT 'auto',
  `observed_sensor` varchar(8) DEFAULT NULL,
  `temperature_threshold` float NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `observed_sensor` (`observed_sensor`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

-- --------------------------------------------------------

--
-- Table structure for table `status`
--

CREATE TABLE IF NOT EXISTS `status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `controller` varchar(8) NOT NULL,
  `last_update` int(11) NOT NULL,
  `last_fan_disable_time` int(11) NOT NULL,
  `last_compressor_enable_time` int(11) NOT NULL,
  `last_compressor_disable_time` int(11) NOT NULL,
  `last_settings_update_time` int(11) NOT NULL,
  `fan` tinyint(1) NOT NULL,
  `cooling` tinyint(1) NOT NULL,
  `heating` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `controller` (`controller`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `settings`
--
ALTER TABLE `settings`
  ADD CONSTRAINT `settings_ibfk_1` FOREIGN KEY (`observed_sensor`) REFERENCES `sensors` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `status`
--
ALTER TABLE `status`
  ADD CONSTRAINT `status_ibfk_1` FOREIGN KEY (`controller`) REFERENCES `controllers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
