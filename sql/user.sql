-- Soundfront.CreateUser
-- Create a new user
CREATE OR ALTER PROCEDURE Soundfront.CreateUser
    @Privacy BIT,
    @DisplayName NVARCHAR(32),
    @Email NVARCHAR(32),
    @EnteredPassword NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON

    INSERT Soundfront.[User](Privacy, DisplayName, Email, PasswordHash)
    OUTPUT Inserted.UserID, Inserted.DisplayName, Inserted.Email, Inserted.Privacy, Inserted.PasswordHash
    VALUES(@Privacy, @DisplayName, @Email, HASHBYTES('SHA2_256', @EnteredPassword));
END
GO

-- Soundfront.CheckLogin
-- Checks if the credentials entered match the ones in the database
CREATE OR ALTER PROCEDURE Soundfront.CheckLogin
    @Email NVARCHAR(32),
    @EnteredPassword NVARCHAR(50)
AS

SELECT U.UserID
FROM Soundfront.[User] U
WHERE U.PasswordHash = HASHBYTES('SHA2_256', @EnteredPassword)
GO

-- Soundfront.GetUser
-- Get a single user
CREATE OR ALTER PROCEDURE Soundfront.GetUser
    @UserID INT
AS
SELECT U.UserID, U.Privacy, U.LastLoginDate, U.JoinDate, U.DisplayName, U.Email, U.PasswordHash
FROM Soundfront.[User] U
WHERE U.UserID = @UserID;
GO

-- Soundfront.GetUserByEmail
-- Gets the user by the inputted email address
CREATE OR ALTER PROCEDURE Soundfront.GetUserByEmail
    @Email NVARCHAR(50)
AS
SELECT U.UserID, U.Privacy, U.LastLoginDate, U.JoinDate, U.DisplayName, U.Email, U.PasswordHash
FROM Soundfront.[User] U
WHERE U.Email = @Email;
GO

-- Soundfront.ListUser
-- Lists the users in the batabase (includes pagination parameters)
CREATE OR ALTER PROCEDURE Soundfront.ListUser
	@Page INT,
	@PageSize INT
AS
SELECT U.UserID, U.Privacy, U.LastLoginDate, U.JoinDate, U.DisplayName, U.Email
FROM Soundfront.[User] U
ORDER BY U.JoinDate DESC
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;
GO

-- Soundfront.FollowUser
-- Followers the User
CREATE OR ALTER PROCEDURE Soundfront.FollowUser
  @FollowerUserID INT,
  @FolloweeUserID INT
AS
INSERT Soundfront.Social(FollowerID, FollowingID)
OUTPUT Inserted.FollowerID, Inserted.FollowingID
VALUES(@FollowerUserID, @FolloweeUserID)
GO

-- Soundfront.ListFollowers
-- Lists the followers of a specific user
CREATE OR ALTER PROCEDURE Soundfront.ListFollowers
  @FolloweeUserID INT
AS
SELECT S.FollowerID, U.DisplayName, U.UserID
FROM Soundfront.Social S
  INNER JOIN Soundfront.[User] U ON U.UserID = S.FollowerID
WHERE S.FollowingID = @FolloweeUserID
GO

-- Soundfront.ListFollowing
-- Lists the users the inputted user follows
CREATE OR ALTER PROCEDURE Soundfront.ListFollowing
  @FollowerUserID INT
AS
SELECT S.FollowingID, U.DisplayName, U.UserID
FROM Soundfront.Social S
  INNER JOIN Soundfront.[User] U ON U.UserID = S.FollowingID
WHERE S.FollowerID = @FollowerUserID
GO

-- Soundfront.IsFollowing
-- Checks if the user is following the other
CREATE OR ALTER PROCEDURE Soundfront.IsFollowing
  @FollowerUserID INT,
  @FolloweeUserID INT
AS
SELECT *
FROM Soundfront.Social S
WHERE S.FollowerID = @FollowerUserID AND S.FollowingID = @FolloweeUserID
GO

-- Soundfront.Unfollow
-- Unfollows User
CREATE OR ALTER PROCEDURE Soundfront.Unfollow
  @FollowerUserID INT,
  @FolloweeUserID INT
AS
DELETE Soundfront.Social
WHERE @FollowerUserID = FollowerID
  AND @FolloweeUserID = FollowingID

GO

-- Soundfront.GetMostCriticalUsers
-- Gets the @Count most critical users based on lowest average rating for albums and songs
CREATE OR ALTER PROCEDURE Soundfront.GetMostCriticalUsers
  @Count INT
AS

WITH SourceCTE(UserID, DisplayName, AverageRating)
AS
(
    SELECT TOP (@Count)
        U.UserID, U.DisplayName,
        AVG(AR.Rating) AS AverageRating
    FROM Soundfront.[User] U
    INNER JOIN Soundfront.AlbumRating AR ON AR.UserID = U.UserID
    GROUP BY U.UserID, U.DisplayName

    UNION

    SELECT TOP (@Count)
        U.UserID, U.DisplayName,
        AVG(SR.Rating) AS AverageRating
    FROM Soundfront.[User] U
        INNER JOIN Soundfront.SongRating SR ON SR.UserID = U.UserID
    GROUP BY U.UserID, U.DisplayName
)
SELECT TOP (@Count)
  S.UserID, S.DisplayName, AVG(S.AverageRating) AS AverageRating
FROM SourceCTE S
GROUP BY S.UserID, S.DisplayName
ORDER BY AverageRating ASC
GO

CREATE OR ALTER PROCEDURE Soundfront.SearchUser
  @Search NVARCHAR(100)
AS

SELECT U.UserID, U.DisplayName
FROM Soundfront.[User] U
WHERE U.DisplayName LIKE @Search
