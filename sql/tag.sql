-- Soundfront.CreateTag
-- Create a tag
CREATE OR ALTER PROCEDURE Soundfront.CreateTag
    @Name NVARCHAR(50)
AS
INSERT Soundfront.Tag([Name])
OUTPUT Inserted.TagID, Inserted.[Name]
VALUES(@Name)

GO

-- Soundfront.GetTag
-- Gets information of Tag based on entered TagID
CREATE OR ALTER PROCEDURE Soundfront.GetTag
    @TagID INT
AS

SELECT T.TagID, T.[Name]
FROM Soundfront.Tag T
WHERE T.TagID = @TagID
GO

-- Soundfront.GetTagByName
-- Gets tag details by its name
CREATE OR ALTER PROCEDURE Soundfront.GetTagByName
    @TagName NVARCHAR
AS
SELECT T.TagID, T.[Name]
FROM Soundfront.Tag T
WHERE T.[Name] = @TagName

GO

-- Soundfront.AddSongTag
-- Add a tag to a song.
CREATE OR ALTER PROCEDURE Soundfront.AddSongTag
    @TagID INT,
	@SongID INT
AS
INSERT Soundfront.SongTag(TagID, SongID)
OUTPUT Inserted.SongTagID, Inserted.TagID, Inserted.SongID
VALUES (@TagID, @SongID)
GO

-- Soundfront.RemoveSongTag
-- Delete a tag. (Remove the tag for the song, but not the tag itself.)
CREATE OR ALTER PROCEDURE Soundfront.RemoveSongTag
    @SongTagID INT
AS
    DELETE FROM Soundfront.SongTag
    WHERE SongTagID = @SongTagID;
GO

-- Soundfront.ListTags
-- Lists the Tags in the database (includes pagination parameters)
CREATE OR ALTER PROCEDURE Soundfront.ListTags
	@Page INT,
	@PageSize INT
AS

SELECT T.TagID, T.[Name]
FROM Soundfront.Tag T
ORDER BY T.TagID DESC
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;

GO

-- Soundfront.ListSongsByTag
-- Lists all songs with a certain tag based on the inputted TagID
CREATE OR ALTER PROCEDURE Soundfront.ListSongsByTag
    @TagID INT,
    @Page INT,
    @PageSize INT
AS

SELECT S.SongID, S.UserID, S.AlbumID, S.Title, S.[Length],
	S.UploadDate, S.Price, S.[Description], U.DisplayName as Artist,
    A.Title as AlbumTitle
FROM Soundfront.Song S
    INNER JOIN Soundfront.SongTag ST ON ST.SongID = S.SongID
    INNER JOIN Soundfront.Tag T ON T.TagID = ST.TagID
    INNER JOIN Soundfront.Album A ON A.AlbumID = S.AlbumID
    INNER JOIN Soundfront.[User] U ON U.UserID = A.UserID
WHERE T.TagID = @TagID
ORDER BY S.SongID
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;
GO

-- Soundfront.ListSongTags
-- Lists the SongTags in the database
CREATE OR ALTER PROCEDURE Soundfront.ListSongTags
	@SongID INT
AS

SELECT T.Name
FROM Soundfront.SongTag ST
    INNER JOIN Soundfront.Tag T ON T.TagID = ST.TagID
WHERE ST.SongID = @SongID
GO

-- Soundfront.ListAlbumTags
-- Lists the tags of an album by looking at the tags of the songs in the album
CREATE OR ALTER PROCEDURE Soundfront.ListAlbumTags
	@AlbumID INT
AS

SELECT DISTINCT T.Name, T.TagID
FROM Soundfront.SongTag ST
    INNER JOIN Soundfront.Tag T ON T.TagID = ST.TagID
    INNER JOIN Soundfront.Song S ON S.SongID = ST.SongID
WHERE S.AlbumID = @AlbumID
