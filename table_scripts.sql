CREATE TABLE COUNTRY (
    ID_COUNTRY INT IDENTITY(1, 1),
    NM_COUTNRY VARCHAR(50),
    NM_COUNTRY_SLUG VARCHAR(50),
    NM_COUNTRY_ISO2 VARCHAR(2)
    CONSTRAINT PK_ID_COUNTRY PRIMARY KEY (ID_COUNTRY)
);