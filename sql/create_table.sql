USE garlic;

SELECT DATABASE();

STATUS;

SHOW TABLES;

CREATE TABLE User(
        UserId INT PRIMARY KEY NOT NULL,
        UserName VARCHAR(64) NOT NULL,
        Email VARCHAR(128) NOT NULL,
        EmailVerification BOOL NOT NULL,
        Password VARCHAR(128) NOT NULL,
        Admin BOOL NOT NULL,
        SelfIntroduction VARCHAR(512)
);

CREATE TABLE Profession(
        ProfessionId INT PRIMARY KEY NOT NULL,
        ProfessionName VARCHAR(32) NOT NULL,
        ProfessionDescription VARCHAR(64)
);

CREATE TABLE People(
        PeopleId INT PRIMARY KEY NOT NULL,
        PeopleName VARCHAR(256) NOT NULL,
        BirthYear YEAR,
        DeathYear YEAR,
        PeopleDescription VARCHAR(512)
);

CREATE TABLE PeopleProfession(
        PeopleId INT NOT NULL,
        ProfessionId INT NOT NULL,
        PRIMARY KEY (PeopleId, ProfessionId),
        FOREIGN KEY(PeopleId) REFERENCES People(PeopleId)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY(ProfessionId) REFERENCES Profession(ProfessionId)
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

CREATE TABLE Category(
        CategoryId INT PRIMARY KEY NOT NULL,
        CategoryType VARCHAR(32) NOT NULL,
        CategoryName VARCHAR(32) NOT NULL,
        CategoryDescription VARCHAR(64)
);

CREATE TABLE Video(
        VideoId INT PRIMARY KEY NOT NULL,
        VideoName VARCHAR(64) NOT NULL,
        OriginalName VARCHAR(64) NOT NULL,
        VideoDescription VARCHAR(1024),
        StartYear YEAR,
        EndYear YEAR,
        RuntimeMinutes INT,
        CategoryId INT NOT NULL,
        FOREIGN KEY(CategoryId) REFERENCES Category(CategoryId)
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

CREATE TABLE Participate(
        VideoId INT NOT NULL,
        PeopleId INT NOT NULL,
        ParticipateDescription VARCHAR(256),
        PRIMARY KEY (VideoId, PeopleId),
        FOREIGN KEY(VideoId) REFERENCES Video(VideoId)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY(PeopleId) REFERENCES People(PeopleId)
                ON DELETE CASCADE
                ON UPDATE CASCADE
);
       
CREATE TABLE RateVideo(
        VideoId INT NOT NULL,
        UserId INT NOT NULL,
        Rate INT NOT NULL,
        TIMESTAMP_R TIMESTAMP NOT NULL,
        PRIMARY KEY (VideoId, UserId),
        FOREIGN KEY(VideoId) REFERENCES Video(VideoId)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY(UserId) REFERENCES User(UserId)
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

CREATE TABLE AvgRateVideo(
        VideoId INT PRIMARY KEY NOT NULL,
        AvgRate FLOAT NOT NULL,
        CountRate INT NOT NULL,
        FOREIGN KEY(VideoId) REFERENCES Video(VideoId)
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

CREATE TABLE CommentVideo(
        VideoId INT NOT NULL,
        UserId INT NOT NULL,
        Comment VARCHAR(1024) NOT NULL,
        TIMESTAMP_C TIMESTAMP NOT NULL,
        PRIMARY KEY (VideoId, UserId),
        FOREIGN KEY(VideoId) REFERENCES Video(VideoId)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY(UserId) REFERENCES User(UserId)
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

CREATE TABLE RatePeople(
        PeopleId INT NOT NULL,
        UserId INT NOT NULL,
        Rate INT NOT NULL,
        TIMESTAMP_R TIMESTAMP NOT NULL,
        PRIMARY KEY (PeopleId, UserId),
        FOREIGN KEY(PeopleId) REFERENCES People(PeopleId)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY(UserId) REFERENCES User(UserId)
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

CREATE TABLE CommentPeople(
        PeopleId INT NOT NULL,
        UserId INT NOT NULL,
        Comment VARCHAR(1024) NOT NULL,
        TIMESTAMP_C TIMESTAMP NOT NULL,
        PRIMARY KEY (PeopleId, UserId),
        FOREIGN KEY(PeopleId) REFERENCES People(PeopleId)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY(UserId) REFERENCES User(UserId)
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

CREATE TABLE FavoriteFolder(
        FolderId INT PRIMARY KEY NOT NULL,
        FolderName VARCHAR(256) NOT NULL,
        UserId INT NOT NULL,
        CreateTime TIMESTAMP NOT NULL,
        FolderDescription VARCHAR(128),
        FOREIGN KEY(UserId) REFERENCES User(UserId)
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

CREATE TABLE InFolder(
        VideoId INT NOT NULL,
        FolderID INT NOT NULL,
        IncludeTime TIMESTAMP NOT NULL,
        PRIMARY KEY (VideoId, FolderId),
        FOREIGN KEY(VideoId) REFERENCES Video(VideoId)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY(FolderId) REFERENCES FavoriteFolder(FolderId)
                ON DELETE CASCADE
                ON UPDATE CASCADE
);
