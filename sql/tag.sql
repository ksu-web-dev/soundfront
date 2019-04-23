/* Create a general tag. */

CREATE OR ALTER PROCEDURE Soundfront.CreateTag
    @Name NVARCHAR(50)
AS
INSERT Soundfront.Tag([Name])
OUTPUT Inserted.[Name]
VALUES(@Name)

GO

/* Add a tag to a song. */

CREATE OR ALTER PROCEDURE Soundfront.AddSongTag
    @TagID INT,
	@SongID INT
AS
INSERT Soundfront.SongTag(TagID, SongID)
VALUES (@TagID, @SongID)
GO

/* Delete a tag. (Remove the tag for the song, but not the tag itself.) */

CREATE OR ALTER PROCEDURE Soundfront.RemoveSongTag
    @SongTagID INT
AS 
    DELETE FROM Soundfront.SongTag
    WHERE SongTagID = @SongTagID;
GO

CREATE OR ALTER PROCEDURE Soundfront.ListTags
	@Page INT,
	@PageSize INT
AS

SELECT T.TagID, T.[Name]
FROM Soundfront.Tag T
ORDER BY T.TagID DESC
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;

GO

CREATE OR ALTER PROCEDURE Soundfront.GetTagsBySongID
	@SongID INT
AS

SELECT T.TagID, T.[Name]
FROM Soundfront.SongTag ST
	INNER JOIN Soundfront.Tag T ON T.TagID = ST.TagID
WHERE ST.SongID = @SongID