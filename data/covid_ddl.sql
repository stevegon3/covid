-- Create TABLE stat_nc
CREATE TABLE stat_nc (
    county              VARCHAR(50),
    catch               TINYINT,
    row_type            VARCHAR(10),
    stat_date           DATETIME,
    total               INT,
    new                 INT,
    death               INT,
    new_death           INT,
    new_ma              FLOAT,
    new_death_ma        FLOAT,
    conc_new_ma         FLOAT,
    conc_new_death_ma   FLOAT,
    prev10_pos_total    TINYINT,
    prev10_neg_total    TINYINT,
    prev10_pos_death    TINYINT,
    prev10_neg_death    TINYINT
);

-- DROP TABLE pred_us
CREATE TABLE pred_us (
    state         VARCHAR(2),
    stat_date     DATETIME,
    total         FLOAT,
    new           FLOAT,
    death         FLOAT,
    new_death     FLOAT
);

-- DROP TABLE pred_nc
CREATE TABLE pred_nc (
    county        VARCHAR(50),
    stat_date     DATETIME,
    total         FLOAT,
    new           FLOAT,
    death         FLOAT,
    new_death     FLOAT
);

-- DROP TABLE pop_nc
CREATE TABLE pop_nc (
    state         TEXT,
    state_name    TEXT,
    county        TEXT,
    population    INT,
    lat           REAL,
    lon           REAL,
    fips          INT,
    catch         TINYINT
);

-- DROP TABLE pred_perf
CREATE TABLE pred_perf (
    state               VARCHAR(2),
    county              VARCHAR(50),
    catch               TINYINT,
    row_type            VARCHAR(10),
    stat_date           DATETIME,
    calc_date           DATETIME,
    total               INT,
    death               INT,
    pred_total          INT,
    pred_death          INT
);
