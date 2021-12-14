Delimiter //

CREATE TRIGGER VideoRateTRIGGERInsert
    AFTER INSERT ON RateVideo FOR EACH ROW
        BEGIN
            DECLARE ID INTEGER;
            DECLARE Average FLOAT;
            DECLARE Num INTEGER;
            SELECT VideoID, AvgRate, CountRate INTO ID, Average, NUM FROM AvgRateVideo WHERE VideoId = new.VideoId;
            IF NULL = ID THEN
                INSERT INTO AvgRateVideo VALUES (new.VideoID, new.Rate, 1);
            ELSE
                SET Average = (Average * Num + new.Rate) / (Num + 1);
                SET Num = Num + 1;
                UPDATE AvgRateVideo SET AvgRate = Average, CountRate=Num where VideoId = new.VideoId;
            END IF;
        END//


Delimiter ;

Delimiter //

CREATE TRIGGER VideoRateTRIGGERDelete
    BEFORE DELETE ON RateVideo FOR EACH ROW
        BEGIN
            DECLARE ID INTEGER;
            DECLARE Average FLOAT;
            DECLARE Num INTEGER;
            SELECT VideoID, AvgRate, CountRate INTO ID, Average, NUM FROM AvgRateVideo WHERE VideoId = old.VideoId;
            IF NUM=1 THEN
                DELETE FROM AvgRateVideo WHERE VideoId = old.VideoId;
            ELSE
                SET Average = (Average * Num - old.Rate) / (Num - 1);
                SET Num = Num - 1;
                UPDATE AvgRateVideo SET AvgRate = Average, CountRate=Num where VideoId = old.VideoId;
            END IF;
        END//


Delimiter ;

Delimiter //

CREATE TRIGGER VideoRateTRIGGERUpdate
    BEFORE UPDATE ON RateVideo FOR EACH ROW
        BEGIN
            DECLARE ID INTEGER;
            DECLARE Average FLOAT;

            DECLARE OldAverage FLOAT;
            DECLARE Num INTEGER;
            SELECT VideoID, AvgRate, CountRate INTO ID, Average, NUM FROM AvgRateVideo WHERE VideoId = new.VideoId;

            SELECT Rate INTO OldAverage from RateVideo where UserId = new.UserId and VideoId = new.VideoId; 
            IF NULL = ID THEN
                INSERT INTO AvgRateVideo VALUES (new.VideoID, new.Rate, 1);
            ELSE
                SET Average = (Average * Num - OldAverage+new.Rate) / (Num);
                UPDATE AvgRateVideo SET AvgRate = Average, CountRate=Num where VideoId = new.VideoId;
            END IF;
        END//


Delimiter ;

