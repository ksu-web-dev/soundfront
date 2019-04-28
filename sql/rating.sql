-- INSERT AlbumRating
CREATE OR ALTER PROCEDURE Soundfront.InsertAlbumRating
	@UserID INT,
	@AlbumID INT,
	@Rating FLOAT,
	@ReviewText NVARCHAR(1024)
AS

INSERT Soundfront.AlbumRating(UserID, AlbumID, Rating, ReviewText)
OUTPUT Inserted.UserID, Inserted.AlbumID, Inserted.Rating, Inserted.ReviewText
VALUES (@UserID, @AlbumID, @Rating, @ReviewText)

GO

-- UPDATE AlbumRating
CREATE OR ALTER PROCEDURE Soundfront.UpdateAlbumRating
	@RatingID INT,
	@Rating FLOAT,
	@ReviewText NVARCHAR(1024)
AS

UPDATE Soundfront.AlbumRating
	SET
		Rating = @Rating,
		ReviewText = @ReviewText
WHERE RatingID = @RatingID

GO

-- DELETE AlbumRating
CREATE OR ALTER PROCEDURE Soundfront.DeleteAlbumRating
	@RatingID INT
AS

DELETE FROM Soundfront.AlbumRating
WHERE RatingID = @RatingID

GO

-- READ AlbumRating
CREATE OR ALTER PROCEDURE Soundfront.ReadAlbumRating
	@RatingID INT
AS

SELECT A.RatingID, A.UserID, A.AlbumID, A.Rating, A.ReviewText
FROM Soundfront.AlbumRating A
WHERE A.RatingID = @RatingID

GO

-- LIST AlbumRating
CREATE OR ALTER PROCEDURE Soundfront.ListAlbumRatings
	@AlbumID INT
AS

SELECT A.RatingID, A.UserID, A.AlbumID, A.Rating, A.ReviewText, U.DisplayName as [User]
FROM Soundfront.AlbumRating A
	INNER JOIN Soundfront.[User] U on A.UserID = U.UserID
WHERE A.AlbumID = @AlbumID
ORDER BY A.RatingID
GO

-- INSERT SongRating
CREATE OR ALTER PROCEDURE Soundfront.InsertSongRating
	@UserID INT,
	@SongID INT,
	@Rating FLOAT,
	@ReviewText NVARCHAR(1024)
AS

INSERT Soundfront.SongRating(UserID, SongID, Rating, ReviewText)
OUTPUT Inserted.SongID
VALUES (@UserID, @SongID, @Rating, @ReviewText)

GO

-- UPDATE SongRating
CREATE OR ALTER PROCEDURE Soundfront.UpdateSongRating
	@RatingID INT,
	@Rating FLOAT,
	@ReviewText NVARCHAR(1024)
AS

UPDATE Soundfront.SongRating
	SET
		Rating = @Rating,
		ReviewText = @ReviewText
WHERE RatingID = @RatingID

GO

-- DELETE SongRating
CREATE OR ALTER PROCEDURE Soundfront.DeleteSongRating
	@RatingID INT
AS

DELETE FROM Soundfront.SongRating
WHERE RatingID = @RatingID

GO

-- READ SongRating
CREATE OR ALTER PROCEDURE Soundfront.ReadSongRating
	@RatingID INT
AS

SELECT S.RatingID, S.UserID, S.SongID, S.Rating, S.ReviewText
FROM Soundfront.SongRating S
WHERE S.RatingID = @RatingID

GO

-- LIST SongRating
CREATE OR ALTER PROCEDURE Soundfront.ListSongRating
	@Page INT,
	@PageSize INT,
	@SongID INT
AS

SELECT S.RatingID, S.UserID, S.SongID, S.Rating, S.ReviewText,  U.DisplayName as [User]
FROM Soundfront.SongRating S
	INNER JOIN Soundfront.[User] U ON S.UserID = U.UserID
WHERE S.SongID = @SongID
ORDER BY S.RatingID
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;
GO

CREATE OR ALTER PROCEDURE Soundfront.ListRatings
	@UserID INT,
	@Album nvarchar(50),
	@Song nvarchar(50)
AS

SELECT TOP(10) AR.RatingID, AR.Rating, AR.ReviewText, U.DisplayName, A.Title as [Name], A.AlbumID AS ID, @Album AS Type
FROM Soundfront.AlbumRating AR
	INNER JOIN Soundfront.[User] U ON U.UserID = AR.UserID
	INNER JOIN Soundfront.Album A ON A.AlbumID = AR.AlbumID
WHERE U.UserID = @UserID

UNION ALL

SELECT TOP(10) SR.RatingID, SR.Rating, SR.ReviewText, U.DisplayName, S.Title as [Name], S.SongID AS ID, @Song AS Type
FROM Soundfront.SongRating SR
	INNER JOIN Soundfront.[User] U ON U.UserID = SR.UserID
	INNER JOIN Soundfront.Song S ON S.SongID = SR.SongID
WHERE U.UserID = @UserID
