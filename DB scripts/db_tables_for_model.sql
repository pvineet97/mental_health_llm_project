-- DROP TABLE PSYCHOMETRY_RESPONSE;
-- DROP TABLE emotions_spider_chart;
-- DROP TABLE session_summary;
-- drop table Chat_history;
-- drop table user_activity;
-- drop table user_detail;

-- Creating the USER table
CREATE TABLE USER_DETAIL (
    user_id TEXT NOT NULL,
    name TEXT NOT NULL,
    password TEXT NOT NULL,  -- Store hashed passwords
    email_id TEXT NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Phone_number text ,
    Age INT,
    CONSTRAINT PK_user PRIMARY KEY (email_id),
    constraint UK_USER1 unique (user_id)
);
-- Creating the user_activity table with a foreign key reference to user_id in the USER table
CREATE TABLE user_activity (
    user_id text NOT NULL,
    session_id SERIAL NOT NULL,
    session_start_date TIMESTAMP,
    session_end_date TIMESTAMP,
    CONSTRAINT PK_user_activity PRIMARY KEY (session_id),
    CONSTRAINT FK_user_activity_user FOREIGN KEY (user_id) REFERENCES USER_DETAIL (user_id)
);

-- Creating the PSYCHOMETRY_RESPONSE table with a foreign key reference to user_id in the USER table
CREATE TABLE PSYCHOMETRY_RESPONSE (
    USER_ID text NOT NULL,
    Question TEXT,
    Response TEXT,
    CONSTRAINT PK_PSYCH PRIMARY KEY (USER_ID),
    CONSTRAINT FK_psychometry FOREIGN KEY (USER_ID) REFERENCES USER_DETAIL (user_id)
);

-- Creating the emotions_spider_chart table with a foreign key reference to session_id in the user_activity table
CREATE TABLE emotions_spider_chart (
    session_id INT NOT NULL,
    happiness INT,
    sadness INT,
    disgust INT,
    love INT,
    stress INT,
    CONSTRAINT PK_emotions PRIMARY KEY (session_id),
    CONSTRAINT FK_emotions FOREIGN KEY (session_id) REFERENCES user_activity (session_id)
);

-- Creating the SESSION_Summary table with a foreign key reference to session_id in the user_activity table
CREATE TABLE SESSION_Summary (
    session_id INT NOT NULL,
    Summary TEXT,
    CONSTRAINT PK_SESSION_Summary PRIMARY KEY (session_id),
    CONSTRAINT FK_SESSION_Summary FOREIGN KEY (session_id) REFERENCES user_activity (session_id)
);

-- Creating the Chat_history table with a foreign key reference to session_id in the user_activity table
CREATE TABLE Chat_history (
    session_id INT NOT NULL,
    chat_id SERIAL NOT NULL,
    user_text TEXT,
    model_response TEXT,
    time TIMESTAMP,
    CONSTRAINT PK_Chat_history PRIMARY KEY (chat_id),
    CONSTRAINT FK_Chat_history FOREIGN KEY (session_id) REFERENCES user_activity (session_id)
);
