class AlbumRepo():
    def __init__(self, conn):
        self.conn = conn

    def create_album(self, user_id='', album_title='', album_length='', album_price='', album_description=''):
        cursor = self.conn.cursor()
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

    def list_albums(self, page, page_size):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.ListAlbums
                @Page=?,
                @pageSize=?
            """, page, page_size)

        return cursor.fetchall()

