-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 2017-04-01 17:21:01
-- 服务器版本： 10.1.21-MariaDB
-- PHP Version: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `googlescholardb`
--

-- --------------------------------------------------------

--
-- 表的结构 `connections`
--

CREATE TABLE `connections` (
  `sourceScholarURL` varchar(256) COLLATE utf8_bin NOT NULL,
  `targetScholarURL` varchar(256) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- 表的结构 `fields`
--

CREATE TABLE `fields` (
  `scholarURL` varchar(255) NOT NULL,
  `field` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `institutions`
--

CREATE TABLE `institutions` (
  `scholarURL` varchar(255) NOT NULL,
  `institution` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `nodes`
--

CREATE TABLE `nodes` (
  `scholarURL` varchar(256) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- 表的结构 `papercoauthors`
--

CREATE TABLE `papercoauthors` (
  `paperTitle` varchar(255) NOT NULL,
  `paperAuthors` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `papers`
--

CREATE TABLE `papers` (
  `paperName` varchar(512) COLLATE utf8_bin NOT NULL,
  `author` varchar(256) COLLATE utf8_bin NOT NULL,
  `yearPublished` int(11) DEFAULT NULL,
  `numberOfCitations` int(11) DEFAULT '0',
  `authorURL` varchar(255) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- 表的结构 `profile`
--

CREATE TABLE `profile` (
  `aName` varchar(255) COLLATE utf8_bin NOT NULL,
  `NumPaper` int(11) NOT NULL,
  `hIndex` int(11) NOT NULL,
  `authorURL` varchar(255) CHARACTER SET utf8 COLLATE utf8_german2_ci NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `profile`
--
ALTER TABLE `profile`
  ADD PRIMARY KEY (`authorURL`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
