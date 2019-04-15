
/* Create a new user.*/
CREATE OR ALTER PROCEDURE Soundfront.CreateUser
    @UserID INT,
    @Privacy BIT,
    @LastLoginDate DATETIMEOFFSET,
    @JoinDate DATETIMEOFFSET,
    @DisplayName NVARCHAR(32),
    @Email NVARCHAR(32),
    @PasswordHash BINARY
AS 

INSERT Soundfront.[User](Privacy, LastLoginDate, JoinDate, DisplayName, Email, PasswordHash)
VALUES(@Privacy, @LastLoginDate, @JoinDate, @DisplayName, @Email, HASHBYTES('SHA2_512', @PasswordHash));
GO

/* Read in a single user. */
CREATE OR ALTER PROCEDURE Soundfront.ReadUser
    @UserID INT
AS
SELECT U.UserID, U.Privacy, U.LastLoginDate, U.JoinDate, U.DisplayName, U.Email, U.PasswordHash
FROM Soundfront.[User] U
WHERE U.UserID = @UserID;
GO

/* Update a user. */
CREATE OR ALTER PROCEDURE Soundfront.UpdateUser
    @UserID INT,
    @Privacy BIT,
    @LastLoginDate DATETIMEOFFSET,
    @DisplayName NVARCHAR(32),
    @Email NVARCHAR(32)

AS

UPDATE Soundfront.User
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