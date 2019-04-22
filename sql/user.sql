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
