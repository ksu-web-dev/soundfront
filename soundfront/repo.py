class UserRepo():
    def __init__(self, conn):
        self.conn = conn

    def create_user(self, email='', display_name='', password=''):
        cursor = self.conn.cursor()
        cursor.execute("""
        EXEC Soundfront.CreateUser 
            @Privacy=?,
            @DisplayName=?,
            @Email=?,
            @EnteredPassword=?
        """, 1, email, display_name, password)
        return cursor.fetchone()

    def get_user(self, id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.GetUser @UserID=?', id)
        return cursor.fetchone()

class AlbumRepo():
    def __init__(self, conn):
        self.conn = conn

    def create_album(self, user_id='', album_title='', album_length='', album_price='', album_description=''):
        cursor = self.conn.cursor()
        # execute stored proc for creating album
        cursor.execute("""
        EXEC Soundfront.CreateAlbum
            @AlbumUserId=?,
            @AlbumTitle=?,
            @AlbumLength=?,
            @AlbumPrice=?,
            @AlbumDescription=?
            """, user_id, album_title, album_length, album_price, album_description)
        return cursor.fetchone()

    def get_album(self, id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ReadAlbum @AlbumAlbumId=?', id)
        return cursor.fetchone()