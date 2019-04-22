class SongRepo():
    def __init__(self, conn):
        self.conn = conn

    def insert_song(self, userid='', albumid='', title='', length='', price='', description=''):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.InsertSong
                @UserID=?,
	            @AlbumID=?,
	            @Title=?,
	            @Length=?,
	            @Price=?,
	            @Description=?
            """, 1, userid, albumid, title, length, price, description)
        return cursor.fetchone()

    def update_song(self, songid='', title='', length='', price='', description=''):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.UpdateSong
                @SongID=?,
	            @Title=?,
	            @Length=?,
	            @Price=?,
	            @Description=?
            """, songid, title, length, price, description)
        return cursor.fetchone()

    def read_song(self, songid):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ReadSong @SongID=?', songid)
        return cursor.fetchone()

    def delete_song(self, songid):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.DeleteSong @SongID=?', songid)

    def list_song(self, page, pagesize):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ListSong @Page=?, @PageSize=?', page, pagesize)
        return cursor.fetchall()
