USE garlic;

SELECT DATABASE();

STATUS;

-- query --

SELECT v.VideoName, AVG(rv.Rate) AS RateAvg
FROM Video v NATURAL JOIN RateVideo rv
GROUP BY v.VideoId
ORDER BY RateAvg DESC
LIMIT 15;

SELECT DISTINCT VideoId, VideoName
FROM Participate NATURAL JOIN Video
WHERE PeopleId IN (
    SELECT PeopleId FROM Profession NATURAL JOIN PeopleProfession
    WHERE ProfessionId IN (
        SELECT ProfessionId
        FROM Profession
        WHERE ProfessionName = "stunts"
      )
)
ORDER BY VideoId
LIMIT 15;

SELECT DISTINCT p.PeopleId, p.PeopleName
FROM (
    SELECT VideoId, VideoName
    FROM Video
    WHERE RuntimeMinutes < 100) v NATURAL JOIN Participate par NATURAL JOIN People p
ORDER BY p.PeopleId
LIMIT 15;

SELECT DISTINCT p.PeopleId, p.PeopleName, p.BirthYear
FROM (
    SELECT VideoId, VideoName
    FROM Video
    WHERE RuntimeMinutes < 100) v NATURAL JOIN Participate par NATURAL JOIN People p
ORDER BY p.BirthYear DESC
LIMIT 15;

SELECT DISTINCT COUNT(p.PeopleId)
FROM (
    SELECT VideoId, VideoName
    FROM Video
    WHERE RuntimeMinutes < 100) v NATURAL JOIN Participate par NATURAL JOIN People p;

SELECT DISTINCT VideoId, VideoName
FROM Participate NATURAL JOIN Video
WHERE PeopleId IN (
    SELECT PeopleId
    FROM Profession NATURAL JOIN PeopleProfession NATURAL JOIN People
    WHERE ProfessionId IN (
        SELECT ProfessionId FROM Profession
        WHERE ProfessionName = "composer"
    ) AND BirthYear > 1940 AND BirthYear < 1980
)
LIMIT 15;

-- index --

SHOW INDEX FROM User;

SHOW INDEX FROM Profession;

SHOW INDEX FROM People;

SHOW INDEX FROM PeopleProfession;

SHOW INDEX FROM Category;

SHOW INDEX FROM Video;

SHOW INDEX FROM Participate;

SHOW INDEX FROM RateVideo;

SHOW INDEX FROM CommentVideo;

SHOW INDEX FROM RatePeople;

SHOW INDEX FROM CommentPeople;

SHOW INDEX FROM FavoriteFolder;

SHOW INDEX FROM InFolder;

EXPLAIN ANALYZE (
    SELECT CategoryId FROM Category
);

-- Not Used
CREATE INDEX Idx_RunTimeMinutes ON Video(RuntimeMinutes);
DROP INDEX Idx_RunTimeMinutes ON Video;

-- Not Used
CREATE INDEX Idx_Birthyear ON People(Birthyear);
DROP INDEX Idx_Birthyear ON People;
