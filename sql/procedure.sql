DELIMITER //
CREATE Procedure SelectBestMovie()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE CurrentMovieId INT;
    DECLARE CurrentAvgScore FLOAT;
    DECLARE CurrentMovieName VARCHAR(64);
    DECLARE MyCursor CURSOR FOR (
        SELECT VideoId, VideoName, AVG(Rate)
        FROM Video NATURAL JOIN RateVideo
        GROUP BY VideoId, VideoName
    );
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    DROP TABLE IF EXISTS BestMovies;
    CREATE TABLE BestMovies(
        VideoId INT,
        VideoName VARCHAR(64),
        AvgScore REAL
    );
    OPEN MyCursor;
    REPEAT
        FETCH MyCursor INTO CurrentMovieId, CurrentMovieName, CurrentAvgScore;
        IF CurrentAvgScore >= 8 THEN
            INSERT IGNORE INTO BestMovies VALUES (CurrentMovieId, CurrentMovieName, CurrentAvgScore);
        END IF;
    UNTIL done OR (SELECT Count(*) FROM BestMovies) >= 10
    END REPEAT;
    CLOSE MyCursor;
END //
DELIMITER ;



DELIMITER //
CREATE Procedure SelectBestActor()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE CurrentActorId INT;
    DECLARE CurrentAvgScore FLOAT;
    DECLARE CurrentActorName VARCHAR(256);
    DECLARE MyCursor CURSOR FOR (
        SELECT PeopleId, PeopleName, AVG(Rate)
        FROM People NATURAL JOIN RatePeople
        GROUP BY PeopleId, PeopleName
    );
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    DROP TABLE IF EXISTS BestActors;
    CREATE TABLE BestActors(
        PeopleId INT,
        PeopleName VARCHAR(256),
        AvgScore REAL
    );
    OPEN MyCursor;
    REPEAT
        FETCH MyCursor INTO CurrentActorId, CurrentActorName, CurrentAvgScore;
        IF CurrentAvgScore >= 5 THEN
            INSERT IGNORE INTO BestActors VALUES (CurrentActorId, CurrentActorName, CurrentAvgScore);
        END IF;
    UNTIL done OR (SELECT Count(*) FROM BestActors) >= 10
    END REPEAT;
    CLOSE MyCursor;
END //
DELIMITER ;


