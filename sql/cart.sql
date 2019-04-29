-- Soundfront.CreateCart
-- Creates a User's one and only cart
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
-- Lists all items in a cart by the specified user
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

-- Soundfront.AddSongToCart
-- Creates a SongCart which adds a Song to a User's Cart
CREATE OR ALTER PROCEDURE Soundfront.AddSongToCart
	@SongID INT,
	@CartID INT
AS

INSERT Soundfront.SongCart(SongID, CartID)
VALUES (@SongID, @CartID)
GO

-- Soundfront.ClearSongCart
-- Removes all Songs from a User's Cart
CREATE OR ALTER PROCEDURE Soundfront.ClearSongCart
	@CartID INT
AS

DELETE FROM Soundfront.SongCart
WHERE CartID = CartID

GO

-- Soundfront.AddAlbumToCart
-- Adds an album to the cart which creates an AlbumCart row
CREATE OR ALTER PROCEDURE Soundfront.AddAlbumToCart
	@AlbumID INT,
	@CartID INT
AS

INSERT Soundfront.AlbumCart(AlbumID, CartID)
VALUES (@AlbumID, @CartID)

GO

-- Soundfront.ClearAlbumCart
-- Removes all albums from a User's Cart
CREATE OR ALTER PROCEDURE Soundfront.ClearAlbumCart
	@CartID INT
AS

DELETE FROM Soundfront.AlbumCart
WHERE CartID = @CartID

GO

-- Soundfront.CartTotalPrice
-- Computes the sum of the prices in a Cart
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
