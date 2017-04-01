-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 11, 2017 at 01:20 PM
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
-- Table structure for table `institutions`
--

CREATE TABLE `institutions` (
  `scholarName` varchar(255) NOT NULL,
  `institution` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `institutions`
--

INSERT INTO `institutions` (`scholarName`, `institution`) VALUES
('Andrew J Parkes', 'School of Computer Science, University of Nottingham'),
('Edmund Kieran Burke', 'Queen Mary University of London'),
('Greet Vanden Berghe', 'Computer Science, KU Leuven'),
('Patrick De Causmaecker', 'gewoon hoogleraar computerwetenschappen, KU Leuven'),
('Andrew J Parkes', 'School of Computer Science, University of Nottingham'),
('Steven Gustafson', 'Kansas State University, University of Nottingham, GE Global Research'),
('Peter Cowling', 'Professor of Computer Science and Management, University of York'),
('Jingpeng Li', 'Reader of Computer Science, University of Stirling, UK'),
('Salwani Abdullah', 'Universiti Kebangsaan Malaysia'),
('David Elliman', 'Senior Engineer, Montvieux Ltd'),
('Jonathan M. Garibaldi', 'University of Nottingham'),
('Yuri Bykov', 'Research Fellow, The University of Nottingham'),
('John R. Woodward', 'Lecturer in Big Data, Department of Mathematics and Computing Science Stirling University, FK9 4LA'),
('Natalio Krasnogor', 'Professor of Computing Science and Synthetic Biology, Newcastle University'),
('Peter Ross', 'Napier University'),
('Barry McCollum', 'Senior Lecturer, Computer Science, Queen:s University'),
('Peter Middleton', 'Senior Lecturer, Computer Science, Queen:s University Belfast'),
('Ender zcan', 'Lecturer of Computer Science and Operational Research'),
('John H. Drake', 'Queen Mary University of London'),
('Chilukuri Mohan', 'Professor, Electrical Eng. & Computer Science, Syracuse Univ.'),
('A. Sima Etaner - Uyar', 'Associate Professor at Computer Engineering Department, Istanbul Technical University'),
('Mustafa Msr', 'Assoc. Prof., Nanjing University of Aeronautics and Astronautics'),
('Jerry Swan', 'Senior Research Fellow, University of York'),
('Djamila Ouelhadj', 'Associate Professor in Operational Research'),
('Berna Kiraz', 'Research Assistant, Computer Engineering, Marmara niversitesi'),
('Simon Martin', 'Research Assistant. Computing and Mathematics, University of Stirling'),
('Syariza Abdul Rahman', 'Senior Lecturer, Decision Science Department, School of Quantitative Sciences, Universiti Utara'),
('Jakub Mareek', 'IBM Research'),
('Martin Tak', 'Lehigh University'),
('Vana Kalogeraki', 'Associate Professor, Athens University of Economics and Business, AUEB'),
('Dimitrios Gunopulos', 'University of Athens'),
('Franois Schnitzler', 'Senior Researcher, Technicolor'),
('Katharina Morik', 'Professor of Computer Science, TU Dortmund University'),
('Shie Mannor', 'Professor of Electrical Engineering, Technion'),
('Matthias Weidlich', 'Humboldt-Universitt zu Berlin'),
('Alexander Artikis', 'University of Piraeus, NCSR Demokritos'),
('Christian Bockermann', 'Researcher, TU Dortmund University'),
('Robert Shorten', 'Chair of Control Engineering and Decision Science, UCD'),
('Peter Richtarik', 'University of Edinburgh'),
('bissan ghaddar', 'Unknown affiliation'),
('Fabian Wirth', 'Professor for Dynamical Systems, University of Passau'),
('Jie Liu', 'Lehigh University'),
('guanglei wang', 'Telecom SudParis'),
('Jonathan Epperlein', 'IBM Research'),
('Rong Qu', 'Associate Professor, University of Nottingham, UK'),
('Professor Graham Kendall', 'Provost, CEO and Pro-Vice Chancellor, University of Nottingham'),
('Nasser R. Sabar', 'Researcher at STRC, Queensland University of Technology'),
('Jiawei Li', 'School of Computer Science, University of Stirling'),
('Naimah Mohd Hussin', 'Associate Professor of Computer Science'),
('Philip Hingston', 'A/Professor of Computer Science, Edith Cowan University'),
('Simon Lucas', 'Professor of Computer Science, University of Essex'),
('Simon J T Pollard', 'Pro-Vice-Chancellor, School of Water, Energy and Environment'),
('Emma Soane', 'London School of Economics and Political Science'),
('Shahriar Asta', 'PhD - Data & Computer Scientist'),
('Engin Erzin', 'Associate Professor of Computer Engineering, Koc University'),
('YUCEL YEMEZ', 'Koc University'),
('Elif Bozkurt', 'Koc University'),
('Sanem Sariel', 'Associate Professor of Computer Engineering, Istanbul Technical University'),
('Julian Miller', 'Reader, University of York'),
('Patricia Ryser-Welch', 'Unknown affiliation'),
('Mustafa Ersen', 'Research Assistant, Computer Engineering, Istanbul Technical University'),
('Raras Tyasnurita', 'Information Systems Dept., ITS Indonesia/PhD Student ASAP, CS, Univ. of Nottingham'),
('Robert John', 'Professor of Operational Research and Computer Science, University of Nottingham'),
('Abdulkerim apar', 'stanbul Teknik niversitesi, Biliim Enstits'),
('Peer-Olaf Siebers', 'Assistant Professor, School of Computer Science, The University of Nottingham'),
('Hana Rudov', 'Masaryk University, Czech Republic'),
('Dalibor Klusek', 'Masaryk University / CESNET'),
('Tom Mller', 'Purdue University'),
('Ludek Matyska', 'Professor of Informatics, Masaryk University'),
('Roman Bartak', 'Univerzita Karlova v Praze'),
('Pavel Troubil', 'Research Fellow, Masaryk University'),
('Ranieri Baraglia', 'ISTI - CNR'),
('Gabriele Capannini', 'Mlardalens University'),
('Pavel Fibich', 'Department of Botany, University of South Bohemia'),
('Jerome Lauret', 'Brookhaven National Laboratory'),
('Mgr. imon Tth', 'Faculty of Informatics, Masaryk University'),
('Dario Landa-Silva', 'University of Nottingham'),
('Matthew R. Hyde', 'Senior Research Fellow, University of Nottingham'),
('Gabriela Ochoa', 'Senior Lecturer (Associate Professor) , Computing Science and Mathematics, University of Stirling'),
('Marco Tomassini', 'Professor of Computer Science, Faculty of Business and Economics (HEC), University of Lausanne'),
('Sbastien Verel', 'Universit du Littoral Cte d:Opale'),
('Michel Gendreau', 'Professor of Operations Research, cole Polytechnique'),
('Fabio Daolio', 'Postdoctoral Research Assistant, University of Stirling'),
('Nadarajen Veerapen', 'Postdoctoral Research Assistant, University of Stirling'),
('Inman Harvey', 'University of Sussex'),
('Minaya Villasana', 'Professor Applied Mathematics, Universidad Simn Bolvar'),
('Klaus Jaffe', 'Universidad Simon Bolivar'),
('Jorge Alberto Soria Alcaraz', 'Doctor en Ciencias en Computacion'),
('Darrell Whitley', 'Professor of Computer Science,  Colorado State University'),
('Francisco Chicano', 'Assistant Professor, University of Mlaga'),
('Eunice Lpez-Camacho', 'Worked as a Math, Statistics and Computer Science professor (ITESM)'),
('Hugo Terashima-Marn', 'Tecnolgico de Monterrey'),
('Jos Carlos Ortiz-Bayliss', 'Tecnolgico de Monterrey'),
('Olaf Lechtenfeld', 'Professor of Theoretical Physics, Leibniz University Hannover'),
('Ahmed Kheiri', 'Cardiff University, School of Mathematics'),
('Ed Keedwell', 'Senior Lecturer in Computer Science, University of Exeter, UK'),
('Dragan Savic', 'Professor, Centre for Water Systems, University of Exeter'),
('Warren G. Jackson', 'University of Nottingham'),
('Daniel Karapetyan', 'University of Essex'),
('G. Gutin', 'Professor of Computer Science, Royal Holloway, University of London'),
('Abraham P. Punnen', 'Professor of Operations Research, Simon Fraser University'),
('Igor Razgon', 'Lecturer, Department of Computer Science and Information Systems, Birkbeck, University of London'),
('Ben Paechter', 'Edinburgh Napier University'),
('Emma Hart', 'Edinburgh Napier University'),
('Manuel Lpez-Ibez', 'Lecturer, Manchester Business School, University of Manchester, UK'),
('A.E. Eiben', 'Professor of Computational Intelligence, VU University Amsterdam'),
('Joshua Knowles', 'School of Computer Science, University of Birmingham'),
('Juan J. Merelo Guervs', 'Professor of Computer Architecture, University of Granada'),
('Julio Ortega', 'University Granada'),
('Mark Jelasity', 'Senior Researcher, University of Szeged'),
('Marco Dorigo', 'FNRS Research Director, IRIDIA, Universit Libre de Bruxelles'),
('Marc Schoenauer', 'Senior Researcher, INRIA'),
('luca maria gambardella', 'IDSIA Istituto Dalle Molle USI-SUPSI, Lugano, Switzerland'),
('Monaldo Mastrolilli', 'IDSIA'),
('Marco Chiarandini', 'University of Southern Denmark'),
('Bart Craenen', 'University of Edinburgh'),
('Mike Preuss', 'WWU Mnster'),
('Alberto Guillen', 'University of Granada, University of Jan'),
('Mauro Birattari', 'IRIDIA, Universit Libre de Bruxelles'),
('Thomas Sttzle', 'Senior Research Associate of F.R.S.-FNRS, Universit Libre de Bruxelles (ULB)'),
('Lus Paquete', 'Assistant Professor, University of Coimbra'),
('Luca Di Gaspero', 'Associate Professor of Information Technology, University of Udine'),
('Vincenzo Della Mea', 'Assistant Professor of Medical Informatics, University of Udine'),
('Stefano Mizzaro', 'Associate professor of Computer Science and Information Technology'),
('Andrea Roli', 'Dept. of Computer Science and Engineering (DISI) - Universit di Bologna'),
('Paolo Coppola', 'Associate Professor of Computer Science, University of Udine'),
('Tommaso Urli', 'NICTA / CSIRO Data61 & the Australian National University'),
('Luca Vassena', 'Universit di Udine'),
('Wolfgang Slany', 'Professor of Computer Science, Technische Universitt Graz, Austria'),
('Sara Ceschia', 'DIEGM, University of Udine'),
('Nysret Musliu', 'Priv. Dozent and Senior Scientist, Vienna University of Technology'),
('Johannes Gaertner', 'ass. Prof. DI Dr.'),
('Andrea Rendl', 'Researcher at NICTA and Monash University'),
('Guy Kortsarz', 'Professor computer science'),
('Ruggero Bellio', 'Associate Professor of Statistics, University of Udine'),
('Giacomo Di Tollo', 'Universit Ca: Foscari, Venezia'),
('Agostino Dovier', 'Professor of Computer Science, University of Udine'),
('Andrea Schaerf', 'Professor of Computer Science, DPIA, University of Udine, Italy'),
('Francesco M. Donini', 'Full Professor, Universit della Tuscia - Viterbo'),
('Maurizio Lenzerini', 'Professor of Computer Science, Universit di Roma La Sapienza'),
('Daniele Nardi', 'Sapienza Univ. Roma, Dept. Computer, Control and Management Engineering'),
('Werner Nutt', 'Professor of Computer Science, Free University of Bozen-Bolzano'),
('Krzysztof R. Apt', 'CWI fellow, CWI , The Netherlands'),
('Amnon Meisels', 'Professor of Computer Science, Ben-Gurion University'),
('Gerhard Post', 'Unknown affiliation'),
('Luigi Palopoli', 'professor of computer science, University of Calabria'),
('Sophia Daskalaki', 'Assistant Professor, University of Patras'),
('Rhyd Lewis', 'Lecturer in Operational Research, Cardiff University'),
('\"C Mumford\" OR \"C Valenzuela\"', 'Cardiff University'),
('Jonathan W. Gillard', 'Cardiff School of Mathematics, Cardiff University'),
('Kate Smith-Miles', 'Professor of Mathematical Sciences, Monash University'),
('Matthew P. John', 'School of Computer Science, Cardiff University'),
('Fiona Carroll', 'University of South Wales'),
('Ian Cooper', 'Cardiff University'),
('Paul Harper', 'Professor of OR, Cardiff University'),
('Wasin Padungwech', 'PhD student, Cardiff University'),
('Yinghao Wu', 'Albert Einstein College of Medicine'),
('Wu  Yu-Huei ', 'National Central University'),
('Andrew J Parkes', 'School of Computer Science, University of Nottingham'),
('Edmund Kieran Burke', 'Queen Mary University of London');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
