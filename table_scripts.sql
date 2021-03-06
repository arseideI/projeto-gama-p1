CREATE DATABASE BD_COVID_GAMMA;

USE BD_COVID_GAMMA;

CREATE TABLE COUNTRY (
    ID_COUNTRY INT NOT NULL IDENTITY(1, 1),
    NM_COUNTRY VARCHAR(50) NOT NULL,
    NM_COUNTRY_SLUG VARCHAR(50) NOT NULL,
    NM_COUNTRY_ISO2 VARCHAR(2) NOT NULL,
    CONSTRAINT PK_ID_COUNTRY PRIMARY KEY (ID_COUNTRY)
);

ALTER TABLE COUNTRY ADD LATITUDE VARCHAR(10);
ALTER TABLE COUNTRY ADD LONGITUDE VARCHAR(10);

CREATE TABLE CASE_COUNTRY(
	ID_CASE INT NOT NULL IDENTITY(1, 1),
	ID_CASE_SISTEM VARCHAR(50),
	ID_COUNTRY INT NOT NULL,
	CONFIRMED INT,
	DEATHS INT,
	RECOVERED INT,
	ACTIVE INT,
	DT_CASE DATE,
	CONSTRAINT PK_CASE_COUNTRY PRIMARY KEY (ID_CASE),
	CONSTRAINT FK_CASE_COUNTRY_COUNTRY FOREIGN KEY (ID_COUNTRY) REFERENCES COUNTRY(ID_COUNTRY)
);

UPDATE COUNTRY SET LATITUDE = '-14.24' WHERE ID_COUNTRY = 2;
UPDATE COUNTRY SET LONGITUDE = '-51.93' WHERE ID_COUNTRY = 2;

INSERT INTO COUNTRY(NM_COUTNRY, NM_COUNTRY_SLUG, NM_COUNTRY_ISO2) VALUES ('Barbados', 'barbados', 'BB');
INSERT INTO COUNTRY(NM_COUTNRY, NM_COUNTRY_SLUG, NM_COUNTRY_ISO2) VALUES ('Brazil', 'brazil', 'BR');

INSERT INTO CASE_COUNTRY VALUES ('7d1ad578-db6d-4698-a2bd-487b201c90c6', 2, 10646926, 257361, 9506251, 883314, '2021-03-02T00:00:00Z')
INSERT INTO CASE_COUNTRY VALUES ('42d54a0a-5616-41bc-b8aa-ff4b54676cfa', 2, 10587001, 255720, 9437611, 893670, '2021-03-01T00:00:00Z')
INSERT INTO CASE_COUNTRY VALUES ('6556ed35-4cbe-4a1a-8a05-85616f30d3e8', 2, 10718630, 259271, 9548315, 911044, '2021-03-03T00:00:00Z')

SELECT
CO.NM_COUTNRY AS PAIS
,CS.CONFIRMED
,CS.DEATHS
,CS.RECOVERED
,CS.ACTIVE
,CS.DT_CASE
FROM CASE_COUNTRY CS
INNER JOIN COUNTRY CO ON CS.ID_COUNTRY = CO.ID_COUNTRY
ORDER BY DT_CASE ASC