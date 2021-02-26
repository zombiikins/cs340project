-- show all current data for all tables
SELECT * FROM Claims;
SELECT * FROM Patients;
SELECT * FROM Providers;
SELECT * FROM Facilities;
SELECT * FROM PatientsProviders;
SELECT * FROM ProvidersFacilities;

-- add a new row for all tables
INSERT INTO `Claims` (`patientID`, `patProvID`, `provFacID`, `dateOfService`, `procedureDesc`, `billedAmount`) VALUES
  (input[1], input[2], input[3], input[4], input[5], input[6], input[7], input[8]);
INSERT INTO `Patients` (`firstName`, `lastName`, `age`, `gender`, `phonenumber`, `email`) VALUES
  (input[1], input[2], input[3], input[4], input[5], input[6]);
INSERT INTO `Providers` (`provFirstName`, `provLastName`, `provSpecialty`) VALUES
  (input[1], input[2], input[3]);
INSERT INTO `Facilities` (`facilityAddress`, `facilityCity`, `facilityState`, `facilityZip`) VALUES
  (input[1], input[2], input[3], input[4]);
INSERT INTO `PatientsProviders` (`patientID`, `provID`) VALUES
  (input[1], input[2]);
INSERT INTO `ProvidersFacilities` (`provID`, `facilityID`) VALUES
  (input[1], input[2]);

-- edit a row
UPDATE Claims SET patientID = input[1], patProvID = input[4],
  provFacID = input[5], dateOfService = input[6], procedureDesc = input[7], billedAmount = input[8]
  WHERE claimID = input[0];
UPDATE Patients SET firstName = input[1], lastName = input[2], age = input[3], gender = input[4],
  phoneNumber = input[5], email = input[6]
  WHERE patientID = input[0];
UPDATE Providers SET provFirstName = input[1], provLastName = input[2], provSpecialty = input[3]
  WHERE provID = input[0];
UPDATE Facilities SET facilityAddress = input[1], facilityCity = input[2], facilityState = input[3],
  facilityZip = input[4]
  WHERE facilityID = input[0];
UPDATE PatientsProviders SET patientID = input[1], provID = input[2]
  WHERE patProvID = input[0];
update ProvidersFacilities SET provID = input[1], facilityID = input[2]
  WHERE provFacID = input[0];

-- delete a row
DELETE FROM Claims WHERE claimID = input[0];
DELETE FROM Patients WHERE patientID = input[0];
DELETE FROM Providers WHERE provID = input[0];
DELETE FROM Facilities WHERE facilityID = input[0];
DELETE FROM PatientsProviders WHERE patProvID = input[0];
DELETE FROM ProvidersFacilities WHERE provFacID = input[0];

-- filter tables
-- use python for condition check in order to concatenate query string for filter/search,
-- which is not showing here
SELECT * FROM Claims
WHERE
  claimID = input[0] AND
  patientID = input[1] AND
  provID = input[2] AND
  facilityID = input[3] AND
  patProvID = input[4] AND
  provFacID = input[5] AND
  dateOfService = input[6] AND
  procedureDesc = input[7] AND
  billedAmount = input[8];

SELECT * FROM Patients
WHERE
  age >= lowerlimit AND age < upperlimit AND
  patientID = input[0] AND
  firstName = input[1] AND
  lastName = input[2] AND
  gender = input[3] AND
  phoneNumber = input[4] AND
  email = input[5];

SELECT * FROM Providers
WHERE 
  provID = input[0] AND
  provFirstName = input[1] AND
  provLastName = input[2] AND
  provSpecialty = input[3];

SELECT * FROM Facilities
WHERE 
  facilityID = input[0] AND
  facilityAddress = input[1] AND
  facilityCity = input[2] AND
  facilityState = input[3] AND
  facilityZip = input[4];

SELECT * FROM PatientsProviders
WHERE
  patientID = input[0] AND
  provID = input[1];

SELECT * FROM ProvidersFacilities
  provID = input[0] AND
  facilityID = input[1];

-- query for See Provider button under Patients page
SELECT * FROM PatientsProviders WHERE patientID = input[0];

-- query for See Patient button under Provider page
SELECT * FROM PatientsProviders WHERE provID = input[0];

-- a drop down list which will dynamically populate current data
-- under search menu and in both PatientsProviders and ProvidersFacilities pages
SELECT patientID from PatientsProviders;
SELECT provID from PatientsProviders;
SELECT provID from ProvidersFacilities;
select facilityID from ProvidersFacilities;