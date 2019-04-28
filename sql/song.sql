-- Insert
CREATE OR ALTER PROCEDURE Soundfront.InsertSong
	@UserID INT,
	@AlbumID INT,
	@Title NVARCHAR(50),
	@Length INT,
	@Price INT,
	@Description NVARCHAR(1024)
AS

INSERT Soundfront.Song(UserID, AlbumID, Title, [Length], Price, [Description])
OUTPUT Inserted.SongID
VALUES (@UserID, @AlbumID, @Title, @Length, @Price, @Description)

GO

-- Read
CREATE OR ALTER PROCEDURE Soundfront.ReadSong
	@SongID INT
AS

SELECT S.SongID, S.UserID, S.AlbumID, S.Title, S.[Length],
	S.UploadDate, S.Price, S.[Description], U.DisplayName as Artist,
	A.Title as AlbumTitle
FROM Soundfront.Song S
	LEFT JOIN Soundfront.Album A ON A.AlbumID = S.AlbumID
	INNER JOIN Soundfront.[User] U ON U.UserID = S.UserID
WHERE S.SongID = @SongID

GO

-- List
CREATE OR ALTER PROCEDURE Soundfront.ListSong
	@Page INT,
	@PageSize INT
AS

SELECT S.SongID, S.UserID, S.AlbumID, S.Title, S.[Length],
	S.UploadDate, S.Price, S.[Description], U.DisplayName as Artist,
	A.Title as AlbumTitle
FROM Soundfront.Song S
	LEFT JOIN Soundfront.Album A ON A.AlbumID = S.AlbumID
	INNER JOIN Soundfront.[User] U ON U.UserID = S.UserID
ORDER BY S.UploadDate DESC
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;
GO

-- List songs by user
CREATE OR ALTER PROCEDURE Soundfront.ListSongsByUser
	@UserID INT
AS

SELECT S.SongID, S.UserID, S.AlbumID, S.Title, S.[Length],
	S.UploadDate, S.Price, S.[Description], U.DisplayName as Artist,
	A.Title as AlbumTitle
FROM Soundfront.Song S
	LEFT JOIN Soundfront.Album A ON A.AlbumID = S.AlbumID
	INNER JOIN Soundfront.[User] U ON U.UserID = S.UserID
WHERE S.UserID = @UserID
ORDER BY S.UploadDate DESC;

GO

-- Search for song
CREATE OR ALTER PROCEDURE Soundfront.SearchForSong
	@Search NVARCHAR(100)
AS

SELECT S.SongID, S.UserID, S.AlbumID, S.Title, S.[Length],
	S.UploadDate, S.Price, S.[Description], U.DisplayName as Artist,
	A.Title as AlbumTitle
FROM Soundfront.Song S
	LEFT JOIN Soundfront.Album A ON A.AlbumID = S.AlbumID
	INNER JOIN Soundfront.[User] U ON U.UserID = S.UserID
WHERE S.Title LIKE @Search
ORDER BY S.Title
GO

CREATE OR ALTER PROCEDURE Soundfront.ListSimilarSongs
	@SongID INT
AS

WITH TagCountCTE(SongID, SharedTagCount) AS (
    SELECT TOP 5 SST.SongID, COUNT(*) as SharedTagCount
    FROM Soundfront.SongTag IST
        INNER JOIN Soundfront.SongTag SST  ON SST.TagID = IST.TagID
    WHERE IST.SongID = @SongID
    GROUP BY SST.SongID
    ORDER BY COUNT(*) DESC
)
SELECT TC.SongID, T.Name
FROM TagCountCTE TC
    INNER JOIN Soundfront.SongTag ST ON TC.SongID = ST.SongID
    INNER JOIN Soundfront.Tag T ON T.TagID = ST.TagID
