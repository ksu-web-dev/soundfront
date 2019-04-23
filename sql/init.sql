DROP TABLE IF EXISTS Soundfront.SongTag;
DROP TABLE IF EXISTS Soundfront.Tag;
DROP TABLE IF EXISTS Soundfront.SongRating;
DROP TABLE IF EXISTS Soundfront.AlbumRating;
DROP TABLE IF EXISTS Soundfront.MusicCart;
DROP TABLE IF EXISTS Soundfront.Song;
DROP TABLE IF EXISTS Soundfront.Album;
DROP TABLE IF EXISTS Soundfront.Social;
DROP TABLE IF EXISTS Soundfront.Cart;
DROP TABLE IF EXISTS Soundfront.[User];
DROP TABLE IF EXISTS Soundfront.SongCart;
DROP TABLE IF EXISTS Soundfront.AlbumCart;

DROP PROCEDURE IF EXISTS Soundfront.[CreateUser];
DROP PROCEDURE IF EXISTS Soundfront.[GetUser];
DROP PROCEDURE IF EXISTS Soundfront.[UpdateUser];
DROP PROCEDURE IF EXISTS Soundfront.[RemoveUser];
DROP PROCEDURE IF EXISTS Soundfront.[ListUser];
DROP PROCEDURE IF EXISTS Soundfront.[GetUserByEmail];
DROP PROCEDURE IF EXISTS Soundfront.[CreateAlbum];
DROP PROCEDURE IF EXISTS Soundfront.[ReadAlbum];
DROP PROCEDURE IF EXISTS Soundfront.[ListAlbums];
DROP PROCEDURE IF EXISTS Soundfront.[DeleteAlbum];
DROP PROCEDURE IF EXISTS Soundfront.[UpdateAlbum];
DROP PROCEDURE IF EXISTS Soundfront.[RecentAlbums];
DROP PROCEDURE IF EXISTS Soundfront.[UserCount];
DROP PROCEDURE IF EXISTS Soundfront.[GetAlbumSongs];
DROP PROCEDURE IF EXISTS Soundfront.[CreateSong];
DROP PROCEDURE IF EXISTS Soundfront.[DeleteSong];
DROP PROCEDURE IF EXISTS Soundfront.[UpdateSong];
DROP PROCEDURE IF EXISTS Soundfront.[ReadSong];
DROP PROCEDURE IF EXISTS Soundfront.[InsertSong];
DROP PROCEDURE IF EXISTS Soundfront.[ListSong];

DROP SCHEMA IF EXISTS Soundfront;
GO

CREATE SCHEMA Soundfront;
GO

CREATE TABLE Soundfront.[User]
(
  UserID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
  Privacy BIT NOT NULL,
  LastLoginDate DATETIME NOT NULL DEFAULT(SYSDATETIMEOFFSET()),
  JoinDate DATETIME NOT NULL DEFAULT(SYSDATETIMEOFFSET()),
  DisplayName NVARCHAR(50) NOT NULL,
  Email NVARCHAR(50) NOT NULL,
  PasswordHash BINARY(512) NOT NULL,
  --CartID INT NOT NULL, -- FOREIGN KEY 
  --  REFERENCES Soundfront.Cart(CartID)

   UNIQUE(Email)
);

CREATE TABLE Soundfront.Cart
(
  CartID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
  UserID INT NOT NULL FOREIGN KEY 
    REFERENCES Soundfront.[User](UserID),

  UNIQUE(UserID)
);

-- Add the Foreign Key from User to Cart
-- ALTER TABLE Soundfront.[User]
--   ADD CONSTRAINT [fk_cart_user]
--   FOREIGN KEY (CartID) REFERENCES Soundfront.Cart(CartID);
  
CREATE TABLE Soundfront.Social
(
  SocialID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
  FollowerID INT NOT NULL FOREIGN KEY 
    REFERENCES Soundfront.[User](UserID),
  FollowingID INT NOT NULL FOREIGN KEY 
    REFERENCES Soundfront.[User](UserID),

  UNIQUE(FollowerID, FollowingID)
);

CREATE TABLE Soundfront.Album
(
  AlbumID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
  UserID INT NOT NULL FOREIGN KEY 
    REFERENCES Soundfront.[User](UserID),
  Title NVARCHAR(50) NOT NULL,
  Length INT NOT NULL,
  Price INT NOT NULL,
  UploadDate DATETIME NOT NULL DEFAULT(SYSDATETIMEOFFSET()),
  Description NVARCHAR(1024) NOT NULL
);

CREATE TABLE Soundfront.Song
(
  SongID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
  UserID INT NOT NULL FOREIGN KEY
    REFERENCES Soundfront.[User](UserID),
  AlbumID INT FOREIGN KEY
    REFERENCES Soundfront.Album(AlbumID),
  Title NVARCHAR(50) NOT NULL,
  Length INT NOT NULL,
  UploadDate DATETIME NOT NULL DEFAULT(SYSDATETIMEOFFSET()),
  Price INT NOT NULL,
  Description NVARCHAR(1024) 
);

CREATE TABLE Soundfront.SongCart
(
  SongCartID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
  SongID INT NOT NULL FOREIGN KEY 
    REFERENCES Soundfront.Song(SongID),
  CartID INT NOT NULL FOREIGN KEY 
    REFERENCES Soundfront.Cart(CartID)
);

CREATE TABLE Soundfront.AlbumCart
(
  AlbumCartID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
  AlbumID INT NOT NULL FOREIGN KEY 
    REFERENCES Soundfront.Album(AlbumID),
  CartID INT NOT NULL FOREIGN KEY 
    REFERENCES Soundfront.Cart(CartID)
);

--CREATE TABLE Soundfront.MusicCart
--(
--  MusicCartID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
-- AlbumID INT NOT NULL FOREIGN KEY 
--   REFERENCES Soundfront.Album(AlbumID),
--  SongID INT NOT NULL FOREIGN KEY 
--    REFERENCES Soundfront.Song(SongID)
--);

CREATE TABLE Soundfront.AlbumRating
(
  RatingID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
  UserID INT NOT NULL FOREIGN KEY
    REFERENCES Soundfront.[User](UserID),
  AlbumID INT NOT NULL FOREIGN KEY
    REFERENCES Soundfront.Album(AlbumID),
  Rating INT NOT NULL,
  ReviewText NVARCHAR(1024) NOT NULL,

  UNIQUE(RatingID, UserID)
);

CREATE TABLE Soundfront.SongRating
(
  RatingID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
  UserID INT NOT NULL FOREIGN KEY
    REFERENCES Soundfront.[User](UserID),
  SongID INT NOT NULL FOREIGN KEY
    REFERENCES Soundfront.Song(SongID),
  Rating INT NOT NULL,
  ReviewText NVARCHAR(1024) NOT NULL,

  UNIQUE(RatingID, UserID)
);

CREATE TABLE Soundfront.Tag
(
  TagID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
  [Name] NVARCHAR(50) NOT NULL,

  UNIQUE([Name])
);

CREATE TABLE Soundfront.SongTag
(
  SongTagID INT NOT NULL IDENTITY(1, 1) PRIMARY KEY,
  TagID INT NOT NULL FOREIGN KEY
    REFERENCES Soundfront.Tag(TagID),
  SongID INT NOT NULL FOREIGN KEY
    REFERENCES Soundfront.Song(SongID)
);
