-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Aug 27, 2016 at 05:58 PM
-- Server version: 5.5.44-0+deb8u1
-- PHP Version: 5.6.22-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `SAfer`
--

-- --------------------------------------------------------

--
-- Table structure for table `security_user`
--

CREATE TABLE IF NOT EXISTS `security_user` (
`id` int(11) NOT NULL,
  `name` varchar(25) NOT NULL,
  `surname` varchar(25) NOT NULL,
  `company` varchar(50) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `security_user`
--

INSERT INTO `security_user` (`id`, `name`, `surname`, `company`) VALUES
(1, 'Haemish', 'Kyd', 'SecurityForReal'),
(2, 'Bob', 'Newheart', 'TheSecGuys');

-- --------------------------------------------------------

--
-- Table structure for table `security_user_calls`
--

CREATE TABLE IF NOT EXISTS `security_user_calls` (
`call_idx` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `lat_data` double NOT NULL,
  `long_data` double NOT NULL,
  `call_flag` int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `security_user_calls`
--

INSERT INTO `security_user_calls` (`call_idx`, `id`, `lat_data`, `long_data`, `call_flag`) VALUES
(9, 1, -26.11851537122595, 28.00108596652537, 0),
(10, 1, -26.118594473986732, 28.00105880767712, 0),
(11, 1, -26.118513785701712, 28.001073272097976, 0),
(12, 1, -26.11842298269484, 28.001131349468135, 0),
(13, 1, -26.118545152237804, 28.001052389456284, 0),
(14, 1, -26.118564952856268, 28.00099201097147, 0),
(15, 1, -26.118501177318326, 28.000974578485433, 0),
(16, 1, -25.97760698837536, 28.117864921105998, 0);

-- --------------------------------------------------------

--
-- Table structure for table `security_user_current`
--

CREATE TABLE IF NOT EXISTS `security_user_current` (
`id` int(11) NOT NULL,
  `sec_user_id` int(11) NOT NULL,
  `lat_data` double NOT NULL,
  `long_data` double NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `security_user_current`
--

INSERT INTO `security_user_current` (`id`, `sec_user_id`, `lat_data`, `long_data`) VALUES
(1, 1, -25.977526452281374, 28.118120975620467),
(2, 2, -25.977494485987467, 28.1188159887255);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `security_user`
--
ALTER TABLE `security_user`
 ADD PRIMARY KEY (`id`);

--
-- Indexes for table `security_user_calls`
--
ALTER TABLE `security_user_calls`
 ADD PRIMARY KEY (`call_idx`), ADD UNIQUE KEY `call_idx` (`call_idx`);

--
-- Indexes for table `security_user_current`
--
ALTER TABLE `security_user_current`
 ADD UNIQUE KEY `id_2` (`id`), ADD KEY `id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `security_user`
--
ALTER TABLE `security_user`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `security_user_calls`
--
ALTER TABLE `security_user_calls`
MODIFY `call_idx` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=17;
--
-- AUTO_INCREMENT for table `security_user_current`
--
ALTER TABLE `security_user_current`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
