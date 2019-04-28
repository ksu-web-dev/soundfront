-- Soundfront.CreateCart
-- Create (Insert) Cart into database
CREATE OR ALTER PROCEDURE Soundfront.CreateCart
	@UserID INT
AS

INSERT Soundfront.Cart(UserID)
VALUES (@UserID)

GO

-- Soundfront.GetCart
-- Gets the CartID of the inputted UserID
CREATE OR ALTER PROCEDURE Soundfront.GetCart
	@UserID INT
AS

SELECT C.CartID
FROM Soundfront.Cart C
WHERE C.UserID = @UserID
GO

-- Soundfront.ListCart
-- Lists the SongCarts and AlbumCarts of the inputted UserID
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

-- Soundfront.InsertSongCart
-- Insert (Create) SongCart into database
CREATE OR ALTER PROCEDURE Soundfront.InsertSongCart
	@SongID INT,
	@CartID INT
AS

INSERT Soundfront.SongCart(SongID, CartID)
VALUES (@SongID, @CartID)
GO

-- Soundfront.DeleteSongCart
-- Delete SongCart from database
CREATE OR ALTER PROCEDURE Soundfront.DeleteSongCart
	@CartID INT
AS

DELETE FROM Soundfront.SongCart
WHERE CartID = CartID

GO

-- Soundfront.ReadSongCart
-- Get information of SongCart from inputted SongCartID
CREATE OR ALTER PROCEDURE Soundfront.ReadSongCart
	@SongCartID INT
AS

SELECT S.SongCartID, S.SongID, S.CartID
FROM Soundfront.SongCart S
WHERE S.SongCartID = @SongCartID

GO

-- Soundfront.ListSongCart
-- List SongCarts in database (includes pagination parameters)
CREATE OR ALTER PROCEDURE Soundfront.ListSongCart
	@Page INT,
	@PageSize INT
AS

SELECT S.SongCartID, S.SongID, S.CartID
FROM Soundfront.SongCart S
ORDER BY S.SongCartID
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;

GO

-- Soundfront.InsertAlbumCart
-- Insert (Create) AlbumCart into database
CREATE OR ALTER PROCEDURE Soundfront.InsertAlbumCart
	@AlbumID INT,
	@CartID INT
AS

INSERT Soundfront.AlbumCart(AlbumID, CartID)
VALUES (@AlbumID, @CartID)

GO

-- Soundfront.DeleteAlbumCart
-- Delete AlbumCart from database
CREATE OR ALTER PROCEDURE Soundfront.DeleteAlbumCart
	@CartID INT
AS

DELETE FROM Soundfront.AlbumCart
WHERE CartID = @CartID

GO

-- Soundfront.ReadAlbumCart
-- Get AlbumCart information from database with inputted AlbumCartID
CREATE OR ALTER PROCEDURE Soundfront.ReadAlbumCart
	@AlbumCartID INT
AS

SELECT A.AlbumCartID, A.AlbumID, A.CartID
FROM Soundfront.AlbumCart A
WHERE A.AlbumCartID = @AlbumCartID

GO

-- Soundfront.ListAlbumCart
-- List SongCarts in database (includes pagination parameters)
CREATE OR ALTER PROCEDURE Soundfront.ListAlbumCart
	@Page INT,
	@PageSize INT
AS

SELECT A.AlbumCartID, A.AlbumID, A.CartID
FROM Soundfront.AlbumCart A
ORDER BY A.AlbumCartID
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;

GO

-- Soundfront.CartTotalPrice
-- Gets the total price of all the items in both the SongCart and AlbumCart
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
