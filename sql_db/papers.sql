-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 23, 2017 at 01:47 PM
-- Server version: 10.1.21-MariaDB
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
-- Table structure for table `papers`
--

CREATE TABLE `papers` (
  `paperName` varchar(512) NOT NULL,
  `author` varchar(256) NOT NULL,
  `yearPublished` int(11) NOT NULL,
  `numberOfCitations` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `papers`
--

INSERT INTO `papers` (`paperName`, `author`, `yearPublished`, `numberOfCitations`) VALUES
('Finiteness in rigid supersymmetric theories', 'Andrew J Parkes', 1984, 257),
('Setting the research agenda in automated timetabling: The second international timetabling competition', 'Andrew J Parkes', 2010, 184),
('Three-loop results in two-loop finite supersymmetric gauge theories', 'Andrew J Parkes', 1985, 119),
('A Survey of NP-Complete Puzzles.', 'Andrew J Parkes', 2008, 109),
('Supermodels and robustness', 'Andrew J Parkes', 1998, 99),
('HyFlex: A Benchmark Framework for Cross-domain Heuristic Search', 'Andrew J Parkes', 2012, 98),
('Clustering at the phase transition', 'Andrew J Parkes', 1997, 93),
('Search for a three-loop-finite chiral theory', 'Andrew J Parkes', 1985, 78),
('Three-loop finiteness conditions in N = 1 super-Yang-Mills', 'Andrew J Parkes', 1985, 76),
('Tuning local search for satisfiability testing', 'Andrew J Parkes', 1996, 72),
('Decomposition, reformulation, and diving in university course timetabling', 'Andrew J Parkes', 2010, 70),
('A cubic action for self-dual Yang-Mills', 'Andrew J Parkes', 1992, 69),
('An investigation of fuzzy multiple heuristic orderings in the construction of university examination timetables', 'Andrew J Parkes', 2009, 62),
('Explicit supersymmetry breaking can preserve finiteness in rigid N = 2 supersymmetric theories', 'Andrew J Parkes', 1983, 62),
('A new model for automated examination timetabling', 'Andrew J Parkes', 2008, 52),
('Generalizing Boolean satisfiability I: Background and survey of existing work', 'Andrew J Parkes', 2004, 52),
('A supernodal formulation of vertex colouring with applications in course timetabling', 'Andrew J Parkes', 2010, 51),
('An extended great deluge approach to the examination timetabling problem', 'Andrew J Parkes', 2009, 50),
('A branch-and-cut procedure for the Udine course timetabling problem', 'Andrew J Parkes', 2012, 49),
('Finiteness and explicit supersymmetry breaking of the N= 4 supersymmetric Yang-Mills theory', 'Andrew J Parkes', 1983, 49),
('N= 1 supersymmetric mass terms in the N = 4 supersymmetric Yang-Mills theory', 'Andrew J Parkes', 1983, 49),
('On covariant multi-loop superstring amplitudes', 'Andrew J Parkes', 1990, 45),
('On the vanishing of the genus two superstring vacuum amplitude', 'Andrew J Parkes', 1988, 41),
('Towards improving the utilization of university teaching space', 'Andrew J Parkes', 2009, 34),
('The second international timetabling competition: Examination timetabling track', 'Andrew J Parkes', 2007, 32),
('The cross-domain heuristic search challengean international research competition', 'Andrew J Parkes', 2011, 30),
('Two-loop modular invariance and spin-statistics', 'Andrew J Parkes', 1987, 28),
('Satisfiability algorithms and finite quantification', 'Andrew J Parkes', 2003, 25),
('Generalizing boolean satisfiability II: Theory', 'Andrew J Parkes', 2004, 24),
('Lifted search engines for satisfiability', 'Andrew J Parkes', 1999, 24),
('Satisfiability algorithms and finite quantification', 'Andrew J Parkes', 2000, 23),
('The teaching space allocation problem with splitting', 'Andrew J Parkes', 2006, 22),
('Mapping the performance of heuristics for constraint satisfaction', 'Andrew J Parkes', 2010, 21),
('The interleaved constructive memetic algorithm and its application to timetabling', 'Andrew J Parkes', 2012, 20),
('HySST: hyper-heuristic search strategies and timetabling', 'Andrew J Parkes', 2012, 20),
('Twisting the N= 2 string', 'Andrew J Parkes', 1995, 19),
('The two loop superstring vacuum amplitude and canonical divisors', 'Andrew J Parkes', 1989, 19),
('Penalising patterns in timetables: Novel integer programming formulations', 'Andrew J Parkes', 2008, 17),
('Scaling properties of pure random walk on random 3-SAT', 'Andrew J Parkes', 2002, 17),
('Policy matrix evolution for generation of heuristics', 'Andrew J Parkes', 2011, 16),
('A stochastic local search algorithm with adaptive acceptance for high-school timetabling', 'Andrew J Parkes', 2014, 13),
('Understanding the role of UFOs within space exploitation', 'Andrew J Parkes', 2006, 13),
('Dimensional regularization and supersymmetry', 'Andrew J Parkes', 1984, 13),
('Generalizing boolean satisfiability III: Implementation', 'Andrew J Parkes', 2005, 12),
('Exploiting solution clusters for coarse-grained distributed search', 'Andrew J Parkes', 2001, 12),
('Generalizing hyper-heuristics via apprenticeship learning', 'Andrew J Parkes', 2013, 11),
('Combining Monte-Carlo and Hyper-heuristic methods for the Multi-mode Resource-constrained Multi-project Scheduling Problem', 'Andrew J Parkes', 2013, 10),
('Multi-objective aspects of the examination timetabling competition track', 'Andrew J Parkes', 2008, 10),
('Search, subsearch and QPROP', 'Andrew J Parkes', 2000, 9),
('Batched Mode Hyper-heuristics', 'Andrew J Parkes', 2013, 8),
('Matrix analysis of genetic programming mutation', 'Andrew J Parkes', 2012, 8),
('Properties of yeditepe examination timetabling benchmark instances', 'Andrew J Parkes', 2010, 8),
('On N= 2 strings and classical scattering solutions of self-dual Yang-Mills in (2, 2) spacetime', 'Andrew J Parkes', 1991, 8),
('Hyperion2: a toolkit for {meta-, hyper-} heuristic research', 'Andrew J Parkes', 2014, 7),
('Evolutionary Squeaky Wheel Optimization: A New Analysis Framework', 'Andrew J Parkes', 2011, 7),
('University space planning and space-type profiles', 'Andrew J Parkes', 2010, 7),
('Dimension reduction in the search for online bin packing policies', 'Andrew J Parkes', 2013, 6),
('Implementing a generalized version of resolution', 'Andrew J Parkes', 2004, 6),
('Distributed local search, phase transitions, and polylog time', 'Andrew J Parkes', 2001, 6),
('System and process for job scheduling to minimize construction costs', 'Andrew J Parkes', 2011, 5),
('On the idea of evolving decision matrix hyper-heuristics for solving constraint satisfaction problems', 'Andrew J Parkes', 2011, 5),
('Combined blackbox and algebraic architecture (CBRA)', 'Andrew J Parkes', 2010, 5),
('Improving the room-size profiles of university teaching space', 'Andrew J Parkes', 2007, 5),
('Easy predictions for the easy-hard-easy transition', 'Andrew J Parkes', 2002, 5),
('Likely Near-term Advances in SAT Solvers', 'Andrew J Parkes', 2002, 5),
('On supersymmetry anomalies', 'Andrew J Parkes', 1985, 5),
('Heuristic generation via parameter tuning for online bin packing', 'Andrew J Parkes', 2014, 4),
('Initial results on fairness in examination timetabling', 'Andrew J Parkes', 2013, 4),
('Enrollment generators, clustering and chromatic numbers', 'Andrew J Parkes', 2008, 4),
('Exploring Heuristic Interactions in Constraint Satisfaction Problems: A Closer Look at the Hyper-Heuristic Space', 'Andrew J Parkes', 2013, 3),
('Improving the performance of vector hyper-heuristics through local search', 'Andrew J Parkes', 2012, 3),
('Conflict inheritance in sectioning and space planning', 'Andrew J Parkes', 2008, 3),
('Worldwide aeronautical route planner', 'Andrew J Parkes', 1999, 3),
('A Software Interface for Supporting the Application of Data Science to Optimisation', 'Andrew J Parkes', 2015, 2),
('Fairness in Examination Timetabling: Student Preferences and Extended Formulations', 'Andrew J Parkes', 2014, 2),
('An ensemble based genetic programming system to predict english football premier league games', 'Andrew J Parkes', 2013, 2),
('Variable and value ordering decision matrix hyper-heuristics: a local improvement approach', 'Andrew J Parkes', 2011, 2),
('Recent Work on Planning and Management of University Teaching Space', 'Andrew J Parkes', 2009, 2),
('An investigation into the use of Haskell for dynamic programming', 'Andrew J Parkes', 2014, 1),
('A genetic programming hyper-heuristic: turning features into heuristics for constraint satisfaction', 'Andrew J Parkes', 2013, 1),
('Next Steps for the Examination Timetabling Format and Competition', 'Andrew J Parkes', 2012, 1),
('Dynamic Data Structures for Taskgraph Scheduling Policies with Applications in OpenCL Accelerators', 'Andrew J Parkes', 2011, 1),
('Semidefinite Programming Relaxations in Timetabling', 'Andrew J Parkes', 2010, 1),
('Evaluating the space planning benefits of partitionable rooms', 'Andrew J Parkes', 2008, 1),
('Clustering within timetabling conflict graphs', 'Andrew J Parkes', 2007, 1),
('Improving coalition performance by exploiting phase transition behavior', 'Andrew J Parkes', 2004, 1),
('Exploiting Solution-Space Structure', 'Andrew J Parkes', 2003, 1),
('CHAMP: Creating heuristics via many parameters for online bin packing', 'Andrew J Parkes', 2016, 0),
('International Portfolio Optimisation with Integrated Currency Overlay Costs and Constraints', 'Andrew J Parkes', 2016, 0),
('Systematic search for local-search SAT heuristics', 'Andrew J Parkes', 2016, 0),
('Multi-component approach to the bipartite Boolean quadratic programming problem', 'Andrew J Parkes', 2016, 0),
('Pattern-Based Approach to the Workflow Satisfiability Problem with User-Independent Constraints', 'Andrew J Parkes', 2016, 0),
('A Hybrid Genetic Algorithm for a Two-Stage Stochastic Portfolio Optimization With Uncertain Asset Prices', 'Andrew J Parkes', 2015, 0),
('Lessons from Building an Automated Pre-Departure Sequencer for Airports', 'Andrew J Parkes', 2014, 0),
('CHaMP: Creating Heuristics via Many Parameters', 'Andrew J Parkes', 2014, 0),
('Task Force on Hyper-heuristics', 'Andrew J Parkes', 2014, 0),
('Physics Department University of California Davis, CA 95616.', 'Andrew J Parkes', 2013, 0),
('Semidefinite Programming in Timetabling II: Algorithms', 'Andrew J Parkes', 2012, 0),
('Generalizing Boolean Satisfiability III: Implementation', 'Andrew J Parkes', 2011, 0),
('Generalizing Boolean Satisfiability II: Theory', 'Andrew J Parkes', 2011, 0);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
