-- Create entity tables

CREATE TABLE `Patients` (
    `patientID` smallint AUTO_INCREMENT NOT NULL,
    `firstName` varchar(50) NOT NULL,
    `lastName` varchar(50) NOT NULL,
    `age` tinyint,
    `gender` varchar(1),
    `phoneNumber` varchar(50),
    `email` varchar(100),
    PRIMARY KEY(`patientID`)
);

CREATE TABLE `Providers` (
    `provID` smallint AUTO_INCREMENT NOT NULL,
    `provFirstName` varchar(50) NOT NULL,
    `provLastName` varchar(50) NOT NULL,
    `provSpecialty` varchar(50) NOT NULL, 
    PRIMARY KEY (`provID`)
);

CREATE TABLE `Facilities` (
    `facilityID` tinyint AUTO_INCREMENT NOT NULL,
    `facilityAddress` varchar(100) NOT NULL,
    `facilityCity` varchar(100) NOT NULL,
    `facilityState` varchar(2) NOT NULL,
    `facilityZip` varchar(10) NOT NULL,
    PRIMARY KEY(`facilityID`)
);

CREATE TABLE `PatientsProviders` (
    `patProvID` smallint AUTO_INCREMENT NOT NULL,
    `patientID` smallint NOT NULL,
    `provID` smallint NOT NULL,
    PRIMARY KEY(`patProvID`),
    FOREIGN KEY(`patientID`)
        REFERENCES `Patients`(`patientID`) on delete cascade on update cascade,
    FOREIGN KEY(`provID`)
        REFERENCES `Providers`(`provID`) on delete cascade on update cascade,
    CONSTRAINT `patprov`
        UNIQUE (`patientID`, `provID`)
);

CREATE TABLE `ProvidersFacilities` (
    `provFacID` smallint AUTO_INCREMENT NOT NULL,
    `provID` smallint NOT NULL,
    `facilityID` tinyint NOT NULL,
    PRIMARY KEY(`provFacID`),
    FOREIGN KEY(`provID`)
        REFERENCES `Providers`(`provID`) on delete cascade on update cascade,
    FOREIGN KEY(`facilityID`)
        REFERENCES `Facilities`(`facilityID`) on delete cascade on update cascade,
    CONSTRAINT `provfac`
        UNIQUE (`provID`, `facilityID`)
);

CREATE TABLE `Claims` (
    `claimID` int AUTO_INCREMENT NOT NULL,
    `patientID` smallint NOT NULL,
    `patProvID` smallint DEFAULT NULL,
    `provFacID` smallint DEFAULT NULL,
    `dateOfService` date NOT NULL,
    `procedureDesc` varchar(50) NOT NULL,
    `billedAmount` decimal(6,2) NOT NULL DEFAULT 0.00,
    PRIMARY KEY(`claimID`),
    FOREIGN KEY(`patientID`)
        REFERENCES `Patients`(`patientID`)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(`patProvID`)
        REFERENCES `PatientsProviders`(`patProvID`) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY(`provFacID`)
        REFERENCES `ProvidersFacilities`(`provFacID`)
        ON DELETE SET NULL ON UPDATE CASCADE
);


-- Insert data into tables

INSERT INTO `Patients` (`firstName`, `lastName`, `age`, `gender`, `phonenumber`, `email`) VALUES
('Laverne', 'Roberts', '60', 'F', '111-222-1234', 'l.roberts@scrubs.com'),
('Jordan', 'Sullivan', '44', 'F', '987-483-2000', 'j.sullivan@scrubs.com'),
('Ben', 'Sullivan', '46', 'M', '987-394-3748', 'b.sully@scrubs.com'),
('Kim', 'Briggs', '34', 'F', '384-495-2930', 'k.briggs@scrubs.com');

INSERT INTO `Providers` (`provFirstName`, `provLastName`, `provSpecialty`) VALUES
('John', 'Dorian', 'Resident'),
('Elliot', 'Reed', 'Endocinology'),
('Chris', 'Turk', 'Surgeon'),
('Percival', 'Cox', 'Resident Advisor'),
('Bob', 'Kelso', 'Chief of Medicine');

INSERT INTO `Facilities` (`facilityAddress`, `facilityCity`, `facilityState`, `facilityZip`) VALUES
('2000 Sacred Dr', 'Heartland', 'MI', '93840'),
('2948 Heart Blvd', 'Sacredsalt', 'WA', '29380'),
('900 North Hollywood Blvd', 'Los Angeles', 'CA', '29333');

INSERT INTO `PatientsProviders` (`patientID`, `provID`) VALUES
(1, 1),
(4, 1),
(3, 2),
(2, 3),
(2, 5);

INSERT INTO `ProvidersFacilities` (`provID`, `facilityID`) VALUES
(1, 1),
(5, 1),
(2, 2),
(3, 2),
(2, 3);

INSERT INTO `Claims` (`patientID`, `patProvID`, `provFacID`, `dateOfService`, `procedureDesc`, `billedAmount`) VALUES
(4, 2, 1, '2021-01-02', 'TDAP Vaccination', 20.00),
(3, 3, 5, '2020-11-27', 'E&M Level 3', 125.00),
(2, 5, 2, '2020-12-06', 'E&M Level 4', 150.00),
(2, 5, 2, '2020-12-19', 'Biopsy', 750.00);
