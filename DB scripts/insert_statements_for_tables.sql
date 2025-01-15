--DROP TABLE PSYCHOMETRY_RESPONSE;
--DROP TABLE emotions_spider_chart;
--DROP TABLE session_summary;
--drop table Chat_history;
--drop table user_activity;
--drop table user_detail;


select * from user_activity ud ;
select * from user_detail ud ;
select * from PSYCHOMETRY_RESPONSE ud ;
select * from Chat_history ud ;
select * from session_summary ud ;
select * from emotions_spider_chart ud ;


INSERT INTO USER_DETAIL (user_name, Gender, Age, password, email_id) VALUES
('Alice Johnson', 'Female', 28, 'alicejohnson', 'alicejohnson123@gmail.com'),
('Bob Smith', 'Male', 35, 'bobsmith', 'bobsmith123@gmail.com'),
('Charlie Brown', 'Non-binary', '22', 'charliebrown', 'charliebrown@gmail.com');

INSERT INTO user_activity (user_id, session_start_date, session_end_date) VALUES
(2, '2024-09-01 08:00:00', '2024-09-01 09:00:00'),
(3, '2024-09-02 10:00:00', '2024-09-02 11:00:00'),
(4, '2024-09-03 12:00:00', '2024-09-03 13:00:00');

INSERT INTO PSYCHOMETRY_RESPONSE (USER_ID, Question, Response) VALUES
(2, 'How did you feel today?', 'Happy'),
(3, 'How did you feel today?', 'Stressed'),
(4, 'How did you feel today?', 'Neutral');

INSERT INTO emotions_spider_chart (session_id, happiness, sadness, disgust, love, stress) VALUES
(1, 80, 10, 5, 70, 20),
(2, 60, 20, 10, 50, 30),
(3, 50, 30, 15, 40, 40);

INSERT INTO SESSION_Summary (session_id, Summary) VALUES
(1, 'Session 1 summary: The user was mostly happy and engaged.'),
(2, 'Session 2 summary: The user showed signs of stress and anxiety.'),
(3, 'Session 3 summary: The user had a balanced mood with some stress.');

INSERT INTO Chat_history (session_id, user_text, model_response, time) VALUES
(1, 'What is the weather today?', 'The weather is sunny.', '2024-09-01 08:05:00'),
(2, 'Can you recommend a movie?', 'Sure, I recommend "Inception".', '2024-09-02 10:15:00'),
(3, 'What is the time?', 'It is 12:30 PM.', '2024-09-03 12:10:00');
