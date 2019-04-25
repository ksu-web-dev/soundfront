-- Insert
CREATE OR ALTER PROCEDURE Soundfront.CreateAlbum
	@AlbumUserId INT,
	@AlbumTitle NVARCHAR(50),
	@AlbumPrice INT,
	@AlbumDescription NVARCHAR(1024)

AS
BEGIN
	SET NOCOUNT ON
	INSERT Soundfront.Album(UserID, Title, Price, [Description])
	OUTPUT Inserted.AlbumID, Inserted.Title, Inserted.Price, Inserted.Description, Inserted.UserID
	VALUES
		(@AlbumUserId, @AlbumTitle, @AlbumPrice, @AlbumDescription)
END
GO

-- Update
CREATE OR ALTER PROCEDURE Soundfront.UpdateAlbum
	@AlbumAlbumId INT,
	@AlbumTitle NVARCHAR(50),
	@AlbumPrice INT,
	@AlbumDescription NVARCHAR(1024)

AS

UPDATE Soundfront.Album
	SET
		Title = @AlbumTitle,
		Price = @AlbumPrice,
		[Description] = @AlbumDescription
WHERE AlbumID = @AlbumAlbumId
GO

-- Read
CREATE OR ALTER PROCEDURE Soundfront.ReadAlbum
	@AlbumAlbumId INT
AS

SELECT A.AlbumID, A.UserID, A.Title, A.Price, A.UploadDate, A.[Description]
FROM Soundfront.Album A
WHERE A.AlbumID = @AlbumAlbumId
GO

-- Get all the Songs from an Album
CREATE OR ALTER PROCEDURE Soundfront.GetAlbumSongs
	@AlbumID INT
AS

SELECT A.AlbumID, A.Title AS AlbumTitle, S.Title, S.[Length], S.Price, S.UploadDate, U.DisplayName as Artist, U.UserID, S.SongID
FROM Soundfront.Album A
	INNER JOIN Soundfront.Song S ON S.AlbumID = A.AlbumID
    INNER JOIN Soundfront.[User] U ON U.UserID = A.UserID
WHERE A.AlbumID = @AlbumID
ORDER BY S.SongID

GO

-- Get Top by Average Rating
--	-> "select the top 5 albums ordered by hightest average rating"
CREATE OR ALTER PROCEDURE Soundfront.GetTopRatedAlbums
	@TimeFrameInDays INT
AS

SELECT TOP 5 
	A.AlbumID, U.DisplayName, A.Title, A.Price, AVG(AR.Rating) AS "Average Rating"
FROM Soundfront.AlbumRating AR
    INNER JOIN Soundfront.Album A ON A.AlbumID = AR.AlbumID
    INNER JOIN Soundfront.[User] U ON U.UserID = A.UserID
WHERE A.UploadDate < DATEADD(DAY, @TimeFrameInDays, SYSDATETIMEOFFSET())
GROUP BY A.AlbumID, U.DisplayName, A.Title, A.Price
ORDER BY AVG(AR.Rating) DESC, A.Price DESC

GO


-- Delete
CREATE OR ALTER PROCEDURE Soundfront.DeleteAlbum
	@AlbumAlbumID INT
AS

DELETE FROM Soundfront.Album
WHERE AlbumID = @AlbumAlbumId

GO

-- List
CREATE OR ALTER PROCEDURE Soundfront.ListAlbums
	@Page INT,
	@PageSize INT
AS

SELECT A.AlbumID, A.UserID, A.Title, A.Price, A.UploadDate, A.[Description]
FROM Soundfront.Album A
ORDER BY A.UploadDate DESC
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;

GO

CREATE OR ALTER PROCEDURE Soundfront.RecentAlbums
	@Page INT,
	@PageSize INT
AS
BEGIN
	SET NOCOUNT ON
	SELECT A.AlbumID, A.UserID, A.Title, U.DisplayName
	FROM Soundfront.Album A 
		INNER JOIN Soundfront.[User] U ON A.UserID = U.UserID
	ORDER BY A.UploadDate DESC
	OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;
END

GO

CREATE OR ALTER PROCEDURE Soundfront.ListAlbumsByUser
	@UserID INT
AS

SELECT A.AlbumID, A.UserID, A.Title, A.Price, A.UploadDate, A.[Description]
FROM Soundfront.Album A
WHERE A.UserID = @UserID
ORDER BY A.UploadDate DESC;
