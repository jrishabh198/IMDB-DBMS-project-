CREATE TABLE `Movie` (
  `MID` char(9) NOT NULL,
  `title` varchar(50) NOT NULL,
  `year` year(4) DEFAULT NULL,
  `rating` float(2,1) DEFAULT NULL,
  `num_votes` int(11) DEFAULT NULL,
  PRIMARY KEY (`MID`)
) ;

CREATE TABLE `Person` (
  `PID` char(9) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`PID`)
);

CREATE TABLE `Country` (
  `CID` int(11) NOT NULL,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`CID`)
);

CREATE TABLE `Genre` (
  `GID` int(11) NOT NULL,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`GID`)
);

CREATE TABLE `Language` (
  `LAID` int(11) NOT NULL,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`LAID`)
);

CREATE TABLE `Location` (
  `LID` int(11) NOT NULL,
  `Name` varchar(200) NOT NULL,
  PRIMARY KEY (`LID`)
);

CREATE TABLE `M_Cast` (
  `ID` int(11) NOT NULL,
  `MID` char(9) NOT NULL,
  `PID` char(9) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `MID` (`MID`),
  KEY `PID` (`PID`),
  FOREIGN KEY (`MID`) REFERENCES `Movie` (`MID`) ON DELETE CASCADE,
  FOREIGN KEY (`PID`) REFERENCES `Person` (`PID`) ON DELETE CASCADE
) ;

CREATE TABLE `M_Country` (
  `ID` int(11) NOT NULL,
  `MID` char(9) NOT NULL,
  `CID` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `MID` (`MID`),
  KEY `CID` (`CID`),
  FOREIGN KEY (`MID`) REFERENCES `Movie` (`MID`) ON DELETE CASCADE,
  FOREIGN KEY (`CID`) REFERENCES `Country` (`CID`) ON DELETE CASCADE
) ;

CREATE TABLE `M_Director` (
  `ID` int(11) NOT NULL,
  `MID` char(9) NOT NULL,
  `PID` char(9) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `MID` (`MID`),
  KEY `PID` (`PID`),
  FOREIGN KEY (`MID`) REFERENCES `Movie` (`MID`) ON DELETE CASCADE,
  FOREIGN KEY (`PID`) REFERENCES `Person` (`PID`) ON DELETE CASCADE
) ;

CREATE TABLE `M_Genre` (
  `ID` int(11) NOT NULL,
  `MID` char(9) NOT NULL,
  `GID` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `MID` (`MID`),
  KEY `GID` (`GID`),
  FOREIGN KEY (`MID`) REFERENCES `Movie` (`MID`) ON DELETE CASCADE,
  FOREIGN KEY (`GID`) REFERENCES `Genre` (`GID`) ON DELETE CASCADE
) ;

CREATE TABLE `M_Language` (
  `ID` int(11) NOT NULL,
  `MID` char(9) NOT NULL,
  `LAID` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `MID` (`MID`),
  KEY `LAID` (`LAID`),
  FOREIGN KEY (`MID`) REFERENCES `Movie` (`MID`) ON DELETE CASCADE,
  FOREIGN KEY (`LAID`) REFERENCES `Language` (`LAID`) ON DELETE CASCADE
) ;

CREATE TABLE `M_Location` (
  `ID` int(11) NOT NULL ,
  `MID` char(9) NOT NULL,
  `LID` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `MID` (`MID`),
  KEY `LID` (`LID`),
  FOREIGN KEY (`MID`) REFERENCES `Movie` (`MID`) ON DELETE CASCADE,
  FOREIGN KEY (`LID`) REFERENCES `Location` (`LID`) ON DELETE CASCADE
) ;

CREATE TABLE `M_Producer` (
  `ID` int(11) NOT NULL ,
  `MID` char(9) NOT NULL,
  `PID` char(9) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `MID` (`MID`),
  KEY `PID` (`PID`),
  FOREIGN KEY (`MID`) REFERENCES `Movie` (`MID`) ON DELETE CASCADE,
  FOREIGN KEY (`PID`) REFERENCES `Person` (`PID`) ON DELETE CASCADE
) ;