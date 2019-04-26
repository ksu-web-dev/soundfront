-- Create (Insert) Cart
CREATE OR ALTER PROCEDURE Soundfront.CreateCart
	@UserID INT
AS

INSERT Soundfront.Cart(UserID)
VALUES (@UserID)

GO

CREATE OR ALTER PROCEDURE Soundfront.GetCart
	@UserID INT
AS

SELECT C.CartID
FROM Soundfront.Cart C
WHERE C.UserID = @UserID
GO

-- Read/Select Cart
CREATE OR ALTER PROCEDURE Soundfront.ListCart
	@UserID INT
AS

SELECT S.SongID as ID, S.Title, S.Price, 'Song' as [Type]
FROM Soundfront.SongCart SC
	INNER JOIN Soundfront.Song S on S.SongID = SC.SongID
	INNER JOIN Soundfront.Cart C on C.CartID = SC.CartID
WHERE C.UserID = @UserID

UNION

SELECT A.AlbumID as ID, A.Title, A.Price, 'Album' as [Type]
FROM Soundfront.AlbumCart AC
	INNER JOIN Soundfront.Album A on A.AlbumID = AC.AlbumID
	INNER JOIN Soundfront.Cart C on C.CartID = AC.CartID
WHERE C.UserID = @UserID
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
	@CartID INT
AS

DELETE FROM Soundfront.SongCart
WHERE CartID = CartID

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
	@CartID INT
AS

DELETE FROM Soundfront.AlbumCart
WHERE CartID = @CartID

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

CREATE OR ALTER PROCEDURE Soundfront.CartTotalPrice
	@UserID INT
AS
WITH PriceCTE as
(
	SELECT S.Price
	FROM Soundfront.SongCart SC
		INNER JOIN Soundfront.Song S on S.SongID = SC.SongID
		INNER JOIN Soundfront.Cart C on C.CartID = SC.CartID
	WHERE C.UserID = @UserID

	UNION ALL

	SELECT A.Price
	FROM Soundfront.AlbumCart AC
		INNER JOIN Soundfront.Album A on A.AlbumID = AC.AlbumID
		INNER JOIN Soundfront.Cart C on C.CartID = AC.CartID
	WHERE C.UserID = @UserID
)
SELECT SUM(P.Price) as OrderTotal
FROM PriceCTE P
