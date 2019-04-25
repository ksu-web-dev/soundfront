-- Create (Insert) Cart
CREATE OR ALTER PROCEDURE Soundfront.CreateCart
	@UserID INT
AS

INSERT Soundfront.Cart(UserID)
VALUES (@UserID)

GO

-- Read/Select Cart
CREATE OR ALTER PROCEDURE Soundfront.ReadCart
	@UserID INT
AS

SELECT SC.SongCartID, S.Title, S.Price, 'Song' as [Type]
FROM Soundfront.SongCart SC
	INNER JOIN Soundfront.Song S on S.SongID = SC.SongID
	INNER JOIN Soundfront.Cart C on C.CartID = SC.SongCartID
WHERE @UserID = C.UserID

UNION

SELECT AC.AlbumCartID, A.Title, A.Price, 'Album' as [Type]
FROM Soundfront.AlbumCart AC
	INNER JOIN Soundfront.Album A on A.AlbumID = AC.AlbumID
	INNER JOIN Soundfront.Cart C on C.CartID = AC.AlbumCartID
WHERE @UserID = C.UserID

GO

-- Insert (Create) SongCart
CREATE OR ALTER PROCEDURE Soundfront.InsertSongCart
	@SongID INT,
	@CartID INT
AS

INSERT Soundfront.SongCart(SongID, CartID)
VALUES (@SongID, @CartID)

GO

-- Delete SongCart
CREATE OR ALTER PROCEDURE Soundfront.DeleteSongCart
	@SongCartID INT
AS

DELETE FROM Soundfront.SongCart
WHERE SongCartID = @SongCartID

GO

-- Read SongCart
CREATE OR ALTER PROCEDURE Soundfront.ReadSongCart
	@SongCartID INT
AS

SELECT S.SongCartID, S.SongID, S.CartID
FROM Soundfront.SongCart S
WHERE S.SongCartID = @SongCartID

GO

-- List SongCarts
CREATE OR ALTER PROCEDURE Soundfront.ListSongCart
	@Page INT,
	@PageSize INT
AS

SELECT S.SongCartID, S.SongID, S.CartID
FROM Soundfront.SongCart S
ORDER BY S.SongCartID
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;

GO

-- Insert (Create) AlbumCart
CREATE OR ALTER PROCEDURE Soundfront.InsertAlbumCart
	@AlbumID INT,
	@CartID INT
AS

INSERT Soundfront.AlbumCart(AlbumID, CartID)
VALUES (@AlbumID, @CartID)

GO

-- Delete AlbumCart
CREATE OR ALTER PROCEDURE Soundfront.DeleteAlbumCart
	@AlbumCartID INT
AS

DELETE FROM Soundfront.AlbumCart
WHERE AlbumCartID = @AlbumCartID

GO

-- Read SongCart
CREATE OR ALTER PROCEDURE Soundfront.ReadAlbumCart
	@AlbumCartID INT
AS

SELECT A.AlbumCartID, A.AlbumID, A.CartID
FROM Soundfront.AlbumCart A
WHERE A.AlbumCartID = @AlbumCartID

GO

-- List SongCarts
CREATE OR ALTER PROCEDURE Soundfront.ListAlbumCart
	@Page INT,
	@PageSize INT
AS

SELECT A.AlbumCartID, A.AlbumID, A.CartID
FROM Soundfront.AlbumCart A
ORDER BY A.AlbumCartID
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;

GO

