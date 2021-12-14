SELECT v.VideoId, v.VideoName, v.OriginalName, v.VideoDescription, v.StartYear, v.EndYear, v.RuntimeMinutes, c.CategoryName, r.RateAvg
FROM Video v NATURAL JOIN Category c NATURAL JOIN
(SELECT VideoId, AVG(Rate) As RateAvg
FROM RateVideo
Group BY VideoId
ORDER BY RateAvg DESC, VideoId
LIMIT 100) r
ORDER BY VideoId;

SELECT v.VideoId, v.VideoName, v.OriginalName, v.VideoDescription, v.StartYear, v.EndYear, v.RuntimeMinutes, c.CategoryName, r.RateAvg
FROM Video v NATURAL JOIN Category c LEFT JOIN
(SELECT VideoId, AVG(Rate) As RateAvg
FROM RateVideo
Group BY VideoId
ORDER BY RateAvg DESC, VideoId) r ON v.VideoId = r.VideoId
ORDER BY ISNULL(r.RateAvg), r.RateAvg DESC, v.VideoId
LIMIT 100;

SELECT v.VideoId, v.VideoName, v.OriginalName, v.VideoDescription, v.StartYear, v.EndYear, v.RuntimeMinutes, c.CategoryName, r.RateAvg
FROM (SELECT *
FROM Video 
WHERE VideoName LIKE "Titanic%") v 
NATURAL JOIN Category c LEFT JOIN
(SELECT VideoId, AVG(Rate) As RateAvg
FROM RateVideo
Group BY VideoId
ORDER BY RateAvg DESC, VideoId) r ON v.VideoId = r.VideoId
ORDER BY ISNULL(r.RateAvg), r.RateAvg DESC, v.VideoId
LIMIT 200;

SELECT * FROM (SELECT * FROM Video WHERE  VideoId = 1) v NATURAL JOIN Category;

SELECT * FROM (SELECT * FROM Participate WHERE VideoId = 120338) p NATURAL JOIN People; -- Titanic
