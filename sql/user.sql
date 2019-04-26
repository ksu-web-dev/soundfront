/* Create a new user.*/
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
    VALUES(@Privacy, @DisplayName, @Email, HASHBYTES('SHA2_512', @EnteredPassword));
END
GO

CREATE OR ALTER PROCEDURE Soundfront.CheckLogin
    @Email NVARCHAR(32),
    @EnteredPassword NVARCHAR(50)
AS

SELECT U.UserID
FROM Soundfront.[User] U
WHERE U.PasswordHash = HASHBYTES('SHA2_512', @EnteredPassword)
GO

/* Get a single user. */
CREATE OR ALTER PROCEDURE Soundfront.GetUser
    @UserID INT
AS
SELECT U.UserID, U.Privacy, U.LastLoginDate, U.JoinDate, U.DisplayName, U.Email, U.PasswordHash
FROM Soundfront.[User] U
WHERE U.UserID = @UserID;
GO

CREATE OR ALTER PROCEDURE Soundfront.GetUserByEmail
    @Email NVARCHAR(50)
AS
SELECT U.UserID, U.Privacy, U.LastLoginDate, U.JoinDate, U.DisplayName, U.Email, U.PasswordHash
FROM Soundfront.[User] U
WHERE U.Email = @Email;
GO

/* Update a user. */
CREATE OR ALTER PROCEDURE Soundfront.UpdateUser
    @UserID INT,
    @Privacy BIT,
    @LastLoginDate DATETIMEOFFSET,
    @DisplayName NVARCHAR(32),
    @Email NVARCHAR(32)

AS

UPDATE Soundfront.[User]
    SET
       Privacy = @Privacy,
       LastLoginDate =  @LastLoginDate,
       DisplayName = @DisplayName,
       Email = @Email
WHERE UserID = @UserID;
GO

/* Delete a user. */
CREATE OR ALTER PROCEDURE Soundfront.RemoveUser
    @UserID INT
AS
    DELETE FROM Soundfront.[User]
    WHERE UserID = @UserID;

GO

CREATE OR ALTER PROCEDURE Soundfront.ListUser
	@Page INT,
	@PageSize INT
AS
SELECT U.UserID, U.Privacy, U.LastLoginDate, U.JoinDate, U.DisplayName, U.Email, U.PasswordHash
FROM Soundfront.[User] U
ORDER BY U.JoinDate DESC
OFFSET ((@Page * @PageSize) - @PageSize) ROWS FETCH NEXT @PageSize ROWS ONLY;
GO

CREATE OR ALTER PROCEDURE Soundfront.UserCount
AS
SELECT COUNT(*)
FROM Soundfront.[User] U
GO

CREATE OR ALTER PROCEDURE Soundfront.FollowUser
  @FollowerUserID INT,
  @FolloweeUserID INT
AS
INSERT Soundfront.Social(FollowerID, FollowingID)
OUTPUT Inserted.FollowerID, Inserted.FollowingID
VALUES(@FollowerUserID, @FolloweeUserID)
GO

CREATE OR ALTER PROCEDURE Soundfront.ListFollowers
  @FolloweeUserID INT
AS
SELECT S.FollowerID, U.DisplayName, U.UserID
FROM Soundfront.Social S
  INNER JOIN Soundfront.[User] U ON U.UserID = S.FollowerID
WHERE S.FollowingID = @FolloweeUserID
GO

CREATE OR ALTER PROCEDURE Soundfront.ListFollowing
  @FollowerUserID INT
AS
SELECT S.FollowingID, U.DisplayName, U.UserID
FROM Soundfront.Social S
  INNER JOIN Soundfront.[User] U ON U.UserID = S.FollowingID
WHERE S.FollowerID = @FollowerUserID
