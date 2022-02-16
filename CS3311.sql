CREATE DATABASE IF NOT EXISTS CS3311;

USE CS3311;

CREATE TABLE IF NOT EXISTS `projects` (
  `ProjectID` int NOT NULL,
  `Project` text,
  `State` text,
  `Budget_Period` text,
  `Reporting_Period` text,
  PRIMARY KEY (`ProjectID`),
  UNIQUE KEY `ProjectID_UNIQUE` (`ProjectID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `activities` (
  `ID` int NOT NULL,
  `Activity` varchar(100) DEFAULT NULL,
  `Description` text,
  `Outcome` text,
  `Output` text,
  `Timeline` text,
  `Statistics` text,
  `Status` text,
  `Successes` text,
  `Challenges` text,
  `CDC_Support_Needed` text,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ProjectID_UNIQUE` (`ID`),
  CONSTRAINT `ProjectID` FOREIGN KEY (`ID`) REFERENCES `projects` (`ProjectID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

