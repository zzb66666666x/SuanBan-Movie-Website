SELECT VideoId, AVG(Rate) AS AvgRate, COUNT(Rate) As CountRate
FROM RateVideo
Group BY VideoId
ORDER BY VideoId
LIMIT 100;

INSERT INTO AvgRateVideo
SELECT VideoId, AVG(Rate) AS AvgRate, COUNT(Rate) As CountRate
FROM RateVideo
Group BY VideoId;
