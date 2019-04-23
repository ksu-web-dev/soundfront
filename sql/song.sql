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

-- Update
CREATE OR ALTER PROCEDURE Soundfront.UpdateSong
	@SongID INT,
	@Title NVARCHAR(50),
	@Length INT,
	@Price INT,
	@Description NVARCHAR(1024)
AS

UPDATE Soundfront.Song
	SET
		Title = @Title,
		[Length] = @Length,
		Price = @Price,
		[Description] = @Description
WHERE SongID = @SongID

GO

-- Read
CREATE OR ALTER PROCEDURE Soundfront.ReadSong
	@SongID INT
AS

SELECT S.SongID, S.UserID, S.AlbumID, S.Title, S.[Length],
	S.UploadDate, S.Price, S.[Description]
FROM Soundfront.Song S
WHERE S.SongID = @SongID

GO

-- Delete
CREATE OR ALTER PROCEDURE Soundfront.DeleteSong
	@SongID INT
AS

DELETE FROM Soundfront.Song
WHERE SongID = @SongID

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