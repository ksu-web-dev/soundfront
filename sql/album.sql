-- Insert
CREATE OR ALTER PROCEDURE Soundfront.CreateAlbum
	@AlbumUserId INT,
	@AlbumTitle NVARCHAR(50),
	@AlbumLength INT,
	@AlbumPrice INT,
	@AlbumDescription NVARCHAR(1024)

AS
BEGIN
	SET NOCOUNT ON
	INSERT Soundfront.Album(UserID, Title, [Length], Price, [Description])
	OUTPUT Inserted.AlbumID, Inserted.Title, Inserted.Length, Inserted.Price, Inserted.Description
	VALUES
		(@AlbumUserId, @AlbumTitle, @AlbumLength, @AlbumPrice, @AlbumDescription)
END

GO

-- Update
CREATE OR ALTER PROCEDURE Soundfront.UpdateAlbum
	@AlbumAlbumId INT,
	@AlbumTitle NVARCHAR(50),
	@AlbumLength INT,
	@AlbumPrice INT,
	@AlbumDescription NVARCHAR(1024)

AS

UPDATE Soundfront.Album
	SET
		Title = @AlbumTitle,
		[Length] = @AlbumLength,
		Price = @AlbumPrice,
		[Description] = @AlbumDescription
WHERE AlbumID = @AlbumAlbumId

GO

-- Read
CREATE OR ALTER PROCEDURE Soundfront.ReadAlbum
	@AlbumAlbumId INT
AS

SELECT A.AlbumID, A.UserID, A.Title, A.[Length], A.Price, A.UploadDate, A.[Description]
FROM Soundfront.Album A
WHERE A.AlbumID = @AlbumAlbumId

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

SELECT A.AlbumID, A.UserID, A.Title, A.[Length], A.Price, A.UploadDate, A.[Description]
FROM Soundfront.Album A
ORDER BY A.UploadDate DESC
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;

GO