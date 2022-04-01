CREATE DATABASE IF NOT EXISTS CS3311;

USE CS3311;

DROP TABLE IF EXISTS `activities`;
DROP TABLE IF EXISTS `projects`;


CREATE TABLE IF NOT EXISTS `projects` (
  `ProjectID` int NOT NULL AUTO_INCREMENT,
  `Project` text,
  `State` text,
  `Budget_Period_Start` datetime,
  `Budget_Period_End` datetime,
  `Reporting_Period` text,
  `File_Name` text,
  PRIMARY KEY (`ProjectID`),
  UNIQUE KEY `ProjectID_UNIQUE` (`ProjectID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `activities` (
  `ActivityID` int NOT NULL AUTO_INCREMENT,
  `ProjectID` int NOT NULL,
  `Activity` text DEFAULT NULL,
  `Description` text,
  `Outcome` text,
  `Output` text,
  `Timeline` text,
  `Statistics` text,
  `Status` text,
  `Successes` text,
  `Challenges` text,
  `CDC_Support_Needed` text,
  `Parent_File` text,
  PRIMARY KEY (`ActivityID`),
  UNIQUE KEY `ProjectID_UNIQUE` (`ActivityID`),
  CONSTRAINT `ProjectID` FOREIGN KEY (`ProjectID`) REFERENCES `projects` (`ProjectID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

