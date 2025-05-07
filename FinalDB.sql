-- Author: Danny Regan
-- Contributors: Amanda Menier
-- Created: 2025-05-05
-- Last Updated: 2025-05-08
-- Version: 0.1.0
-- Description: Database for managing teams, players, and game stats for a pickup sports league.

DROP DATABASE IF EXISTS `league`;
CREATE DATABASE IF NOT EXISTS `league`; 
USE `league`;

/* Tables */ 

DROP TABLE IF EXISTS `teams`;
CREATE TABLE `teams` (
	`team_id` INT NOT NULL AUTO_INCREMENT,
	`team_name` VARCHAR(50) NOT NULL,
	PRIMARY KEY (`team_id`)
);

INSERT INTO `teams` (`team_name`)
VALUES
	('Warriors'),
	('Lions'),
	('Eagles'),
	('Legends'),
	('Knights');

DROP TABLE IF EXISTS `players`;
CREATE TABLE `players` (
	`player_id` INT NOT NULL AUTO_INCREMENT,
	`player_name` VARCHAR(50),
	`team_id` INT,
	`jersey_number` INT,
	PRIMARY KEY (`player_id`),
	FOREIGN KEY (`team_id`) REFERENCES `teams`(`team_id`)
);

INSERT INTO `players` (`player_name`, `team_id`, `jersey_number`)
VALUES
	('John Doe', 1, 10),
	('Jane Smith', 1, 23),
	('Michael Johnson', 1, 47),
	('Emily Davis', 1, 8),
	('Daniel Brown', 1, 51),
	('Sarah Wilson', 1, 12),
	('David Moore', 1, 35),
	('James White', 2, 72),
	('Alice Harris', 2, 19),
	('Robert Clark', 2, 63),
	('Maria Lewis', 2, 5),
	('William Walker', 2, 38),
	('Sophia Young', 2, 56),
	('Jacob Allen', 2, 84),
	('Liam Scott', 3, 61),
	('Isabella King', 3, 11),
	('Noah Green', 3, 22),
	('Ava Adams', 3, 77),
	('Mason Nelson', 3, 59),
	('Chloe Carter', 3, 3),
	('Benjamin Mitchell', 3, 91),
	('Oliver Perez', 4, 27),
	('Charlotte Roberts', 4, 9),
	('Elijah Perez', 4, 55),
	('Amelia White', 4, 39),
	('Jack Lee', 4, 72),
	('Harper Walker', 4, 21),
	('Henry Hall', 4, 60),
	('Lucas Young', 5, 14),
	('Ethan Harris', 5, 26),
	('Madison Martin', 5, 68),
	('Alexander Thompson', 5, 48),
	('Mia Jackson', 5, 82),
	('Logan Robinson', 5, 37),
	('Zoe Lewis', 5, 91);

DROP TABLE IF EXISTS `games`;
CREATE TABLE `games` (
	`game_id` INT NOT NULL AUTO_INCREMENT,
	`home_team_id` INT NOT NULL,
	`home_team_score` INT,
	`away_team_id` INT NOT NULL,
	`away_team_score` INT,
	`date_and_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
	`game_type` ENUM('pre-season', 'regular-season', 'post-season') DEFAULT 'regular-season',
	`completed` BOOL DEFAULT FALSE,
	PRIMARY KEY (`game_id`),
	FOREIGN KEY (`home_team_id`) REFERENCES `teams` (`team_id`),
	FOREIGN KEY (`away_team_id`) REFERENCES `teams` (`team_id`)
);

INSERT INTO `games` (`home_team_id`, `home_team_score`, `away_team_id`, `away_team_score`, `date_and_time`, `game_type`, `completed`)
VALUES
	(1, 4, 2, 3, '2025-04-27 20:00:00', 'pre-season', TRUE),
	(3, 1, 4, 2, '2025-04-28 20:00:00', 'regular-season', TRUE),
	(5, 6, 1, 1, '2025-04-29 20:00:00', 'regular-season', TRUE),
    (2, NULL, 3, NULL, '2025-04-30 20:00:00', 'regular-season', TRUE); -- A future game, not yet played

DROP TABLE IF EXISTS `points_scored`;
CREATE TABLE `points_scored` (
	`player_id` INT NOT NULL,
	`game_id` INT NOT NULL,
	`points_scored` INT NOT NULL DEFAULT 0,
	PRIMARY KEY (`player_id`,`game_id`),
	FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`),
	FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`)
);

INSERT INTO `points_scored` (`player_id`, `game_id`, `points_scored`)
VALUES
    (1, 1, 2),
	(2, 1, 2),
	(8, 1, 1),
	(12, 1, 1),
	(13, 1, 1),
	(20, 2, 1),
	(23, 2, 1),
	(24, 2, 1),
	(29, 3, 2),
	(30, 3, 3),
	(33, 3, 1),
	(1, 3, 1);

/* Views */

DROP VIEW IF EXISTS top_scorers;
CREATE VIEW top_scorers AS
	SELECT
		SUM(ps.points_scored) AS TotalPoints,
        p.player_name AS Name,
        t.team_name AS Team
	FROM teams t
	JOIN players p ON t.team_id = p.team_id
	JOIN points_scored ps ON p.player_id = ps.player_id
	GROUP BY t.team_name, p.player_name
	ORDER BY TotalPoints DESC LIMIT 10;
SELECT * FROM top_scorers;

DROP VIEW IF EXISTS league_standings;
CREATE VIEW league_standings AS
	-- Team Name
	SELECT 
		t.team_name AS Team,
    -- Games Played
    (
		SELECT COUNT(*)
        FROM games g
        WHERE (t.team_id = g.home_team_id OR t.team_id = g.away_team_id)
			AND completed = TRUE
    ) AS GP,
    -- Wins
    (
		SELECT COUNT(*)
        FROM games g 
        WHERE g.completed = TRUE 
			AND (
				(t.team_id = g.home_team_id AND g.home_team_score > g.away_team_score)
				OR
				(t.team_id = g.away_team_id AND g.away_team_score > g.home_team_score)
			)
    ) AS W,
    -- Losses
    (
		SELECT COUNT(*)
        FROM games g 
        WHERE g.completed = TRUE
			AND (
				(t.team_id = g.home_team_id AND g.home_team_score < g.away_team_score)
				OR
				(t.team_id = g.away_team_id AND g.away_team_score < g.home_team_score)
			)
    ) AS L,
    -- Win Percentage
    (
		SELECT ROUND(100.0 * wins / games_played, 1)
        FROM
        (
			SELECT COUNT(*) AS wins
            FROM games g 
			WHERE g.completed = TRUE
				AND (
					(t.team_id = g.home_team_id AND g.home_team_score > g.away_team_score)
					OR
					(t.team_id = g.away_team_id AND g.away_team_score > g.home_team_score)
				)
		) wins,
        (
			SELECT COUNT(*) AS games_played
			FROM games g
			WHERE (t.team_id = g.home_team_id OR t.team_id = g.away_team_id)
				AND completed = TRUE
			) games_played
    ) AS WP
FROM teams t;

DROP VIEW IF EXISTS game_results;
CREATE VIEW game_results AS
SELECT 
	g.date_and_time AS Date,
	ht.team_name AS Home,
    g.home_team_score AS 'Home Score',
    at.team_name AS Away,
	g.away_team_score AS 'Away Score'
FROM games g
JOIN teams ht ON g.home_team_id = ht.team_id
JOIN teams at ON g.away_team_id = at.team_id
ORDER BY g.date_and_time;
SELECT * FROM game_results;

/* Functions */

DROP FUNCTION IF EXISTS getPlayerId;    
Delimiter $$
CREATE FUNCTION getPlayerId(myPlayerName VARCHAR(50))
RETURNS INT DETERMINISTIC
BEGIN
	DECLARE foundPlayerId INT;
    SELECT player_id INTO foundPlayerId 
    FROM players
    WHERE player_name = myPlayerName;
	
    IF foundPlayerId IS NULL
    THEN SET foundPlayerId = -1;
    END IF;

    RETURN foundPlayerId;
END$$
Delimiter ;
SELECT getPlayerId('Emily Davis') AS playerId; -- Exists
SELECT getPlayerId('Danny Regan') AS playerId; -- Does not exist

DROP FUNCTION IF EXISTS getTeamId;    
Delimiter $$
CREATE FUNCTION getTeamId(myTeamName VARCHAR(50))
RETURNS INT DETERMINISTIC
BEGIN
	DECLARE foundTeamId INT;
    SELECT team_id INTO foundTeamId 
    FROM teams
    WHERE team_name = myTeamName;
	
    IF foundTeamId IS NULL
    THEN SET foundTeamId = -1;
    END IF;

    RETURN foundTeamId;
END$$
Delimiter ;
SELECT getTeamId('Warriors') AS teamId; -- Exists
SELECT getTeamId('Red Sox') AS teamId; -- Does not exist

DROP FUNCTION IF EXISTS getGameId;    
Delimiter $$
CREATE FUNCTION getGameId(myGameDateAndTime DATETIME, myTeamName VARCHAR(50))
RETURNS INT DETERMINISTIC
BEGIN
	DECLARE foundGameId INT;
    DECLARE teamId INT;
    
	SET teamId = getTeamId(myTeamName);
    
    SELECT g.game_id INTO foundGameId 
    FROM games g
    JOIN teams t ON g.home_team_id = t.team_id OR g.away_team_id = t.team_id
    WHERE g.date_and_time = myGameDateAndTime 
		AND (g.home_team_id = teamId OR g.away_team_id = teamId)
	LIMIT 1;
	
    IF foundGameId IS NULL
    THEN SET foundGameId = -1;
    END IF;

    RETURN foundGameId;
END$$
Delimiter ;
SELECT getGameId('2025-04-28 20:00:00', 'Legends') AS gameId; -- Exists
SELECT getGameId('2025-04-29 20:00:00', 'Legends') AS gameId; -- Does not exist

/* Procedures */

DROP PROCEDURE IF EXISTS showLeagueStandings;
DELIMITER $$
CREATE PROCEDURE showLeagueStandings()
BEGIN
	SELECT *
    FROM league_standings ls
    ORDER BY (
		SELECT (ls.W * 3 - ls.L * 2)
    ) DESC;
END$$
DELIMITER ;
CALL showLeagueStandings();

DROP PROCEDURE IF EXISTS getTeamRoster;
DELIMITER $$
CREATE PROCEDURE getTeamRoster(IN myTeamName VARCHAR(50))
BEGIN
	SELECT p.player_name, p.jersey_number
    FROM players p
    JOIN teams t ON t.team_id = p.team_id
    WHERE t.team_name = myTeamName
    ORDER BY p.jersey_number;
END$$
DELIMITER ;
CALL getTeamRoster('Knights');

DROP PROCEDURE IF EXISTS getAllTeams;
DELIMITER $$
CREATE PROCEDURE getAllTeams()
BEGIN
	SELECT team_name AS Teams
    FROM teams
    ORDER BY team_name;
END$$
DELIMITER ;
CALL getAllTeams();

DROP PROCEDURE IF EXISTS getPlayerGoals;
DELIMITER $$
CREATE PROCEDURE getPlayerGoals(IN playerName VARCHAR(50))
BEGIN
	SELECT
		p.player_name AS Name,
        SUM(ps.points_scored) AS Points
    FROM players p
    JOIN points_scored ps ON p.player_id = ps.player_id
    WHERE p.player_name = playerName
    GROUP BY p.player_name;
END$$
DELIMITER ;
CALL getPlayerGoals('John Doe');

DROP PROCEDURE IF EXISTS getTeamSchedule;
DELIMITER $$
CREATE PROCEDURE getTeamSchedule(IN teamName VARCHAR(50))
BEGIN
	DECLARE teamId INT;
	SET teamId = getTeamId(teamName);
    
	SELECT 
		ht.team_name AS Home,
        at.team_name AS Away,
        g.date_and_time AS Date,
        CASE
			WHEN g.completed = TRUE AND (
				(g.home_team_id = teamId AND g.home_team_score > g.away_team_score) OR 
				(g.away_team_id = teamId AND g.away_team_score > g.home_team_score)
            )
            THEN 'W'
            WHEN g.completed = TRUE AND (
				(g.home_team_id = teamId AND g.home_team_score < g.away_team_score) OR 
				(g.away_team_id = teamId AND g.away_team_score < g.home_team_score)
            )
            THEN 'L'
            WHEN g.completed = TRUE AND (
				(g.home_team_id = teamId AND g.home_team_score = g.away_team_score)
            )
            THEN 'T'
            ELSE ''
		END AS Result,
        g.game_type AS Season
    FROM games g 
    JOIN teams ht ON g.home_team_id = ht.team_id
    JOIN teams at ON g.away_team_id = at.team_id
    WHERE g.home_team_id = teamId OR g.away_team_id = teamId
    ORDER BY g.date_and_time;
END$$
DELIMITER ;
CALL getTeamSchedule('Lions');

DROP PROCEDURE IF EXISTS updateGame;
DELIMITER $$
CREATE PROCEDURE updateGame(IN gameId INT, homeScore INT, awayScore INT)
BEGIN
	UPDATE games
    SET home_team_score = homeScore, away_team_score = awayScore
    WHERE gameId = game_id;
    COMMIT;
END$$
DELIMITER ;
CALL updateGame(4, 2, 2);

DROP PROCEDURE IF EXISTS deletePlayer;
DELIMITER $$
CREATE PROCEDURE deletePlayer(IN playerName VARCHAR(50))
BEGIN
	DELETE
    FROM players
    WHERE player_id = getPlayerId(playerName);
    COMMIT;
END$$
DELIMITER ;
CALL deletePlayer('Zoe Lewis');

SELECT * FROM top_scorers;
SELECT * FROM game_results;
SELECT * FROM players; -- Not a view, but to show that Zoe Lewis was deleted from the db