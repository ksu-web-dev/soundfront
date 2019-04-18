/* Create a general tag. */

CREATE OR ALTER PROCEDURE Soundfront.CreateTag
    @TagID INT,
    @Name NVARCHAR(50)
AS
INSERT Soundfront.Tag(TagID, [Name])
VALUES(@TagID, @Name)
GO

/* Add a tag to a song. */

CREATE OR ALTER PROCEDURE Soundfront.AddSongTag
    @SongTagID INT
AS
INSERT Soundfront.SongTag(SongTagID)
VALUES (@SongTagID)
GO

/* Delete a tag. (Remove the tag for the song, but not the tag itself.) */

CREATE OR ALTER PROCEDURE Soundfront.RemoveSongTag
    @TagID INT
AS 
    DELETE FROM Soundfront.SongTag
    WHERE TagID = @TagID;
GO