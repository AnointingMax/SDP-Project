--
-- File generated with SQLiteStudio v3.2.1 on Sun Feb 14 17:30:54 2021
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: person
CREATE TABLE person (
    id       INTEGER      NOT NULL,
    fname    VARCHAR (30) NOT NULL,
    lname    VARCHAR (30) NOT NULL,
    location VARCHAR (15) NOT NULL,
    password VARCHAR (60) NOT NULL,
    type     VARCHAR (20),
    PRIMARY KEY (
        id
    )
);

-- Table: user
CREATE TABLE user (
    id    INTEGER      NOT NULL,
    email VARCHAR (25) NOT NULL,
    phone VARCHAR (11) NOT NULL,
    PRIMARY KEY (
        id
    ),
    FOREIGN KEY (
        id
    )
    REFERENCES person (id),
    UNIQUE (
        email
    ),
    UNIQUE (
        phone
    )
);


-- Table: worker
CREATE TABLE worker (
    id          INTEGER      NOT NULL,
    email       VARCHAR (25) NOT NULL,
    phone       VARCHAR (11) NOT NULL,
    job         VARCHAR (20) NOT NULL,
    description TEXT         NOT NULL,
    image       VARCHAR (20) NOT NULL,
    rate        FLOAT,
    active      BOOLEAN      NOT NULL,
    available   BOOLEAN      NOT NULL,
    PRIMARY KEY (
        id
    ),
    FOREIGN KEY (
        id
    )
    REFERENCES person (id),
    UNIQUE (
        email
    ),
    UNIQUE (
        phone
    ),
    CHECK (active IN (0, 1) ),
    CHECK (available IN (0, 1) ) 
);

-- Table: address
CREATE TABLE address (
    id       INTEGER       NOT NULL,
    user_id  INTEGER       NOT NULL,
    address  VARCHAR (120) NOT NULL,
    city     VARCHAR (15)  NOT NULL,
    landmark VARCHAR (120),
    PRIMARY KEY (
        id
    ),
    FOREIGN KEY (
        user_id
    )
    REFERENCES user (id) 
);


-- Table: work_log
CREATE TABLE work_log (
    id          INTEGER      NOT NULL,
    user_id     INTEGER      NOT NULL,
    worker_id   INTEGER      NOT NULL,
    address_id  INTEGER      NOT NULL,
    duration    VARCHAR (15) NOT NULL,
    description TEXT         NOT NULL,
    date        DATETIME     NOT NULL,
    accepted    BOOLEAN      NOT NULL,
    completed   BOOLEAN      NOT NULL,
    PRIMARY KEY (
        id
    ),
    FOREIGN KEY (
        user_id
    )
    REFERENCES user (id),
    FOREIGN KEY (
        worker_id
    )
    REFERENCES worker (id),
    FOREIGN KEY (
        address_id
    )
    REFERENCES address (id),
    CHECK (accepted IN (0, 1) ),
    CHECK (completed IN (0, 1) ) 
);

-- Table: rating
CREATE TABLE rating (
    id          INTEGER  NOT NULL,
    user_id     INTEGER  NOT NULL,
    worker_id   INTEGER  NOT NULL,
    rating      INTEGER  NOT NULL,
    description TEXT     NOT NULL,
    date        DATETIME NOT NULL,
    PRIMARY KEY (
        id
    ),
    FOREIGN KEY (
        user_id
    )
    REFERENCES user (id),
    FOREIGN KEY (
        worker_id
    )
    REFERENCES worker (id) 
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
