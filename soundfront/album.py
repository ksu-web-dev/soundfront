from flask import (Blueprint, render_template, current_app)

bp = Blueprint('album', __name__, url_prefix='/album')

@bp.route('/', methods=['GET'])
def album_home():
    album_repo = current_app.config['album']
    albums = album_repo.recent_albums(page=1, page_size=10)
    # TODO: Update this, for now it is just rednering the same template as the homepage
    #       also populated with the most recent albums
    return render_template('index.html', albums=albums)

@bp.route('/<album_id>', methods=['GET'])
def album(album_id):
    album_repo = current_app.config['album']
    album_songs = album_repo.get_album_songs(album_id)
    print(album_songs)
    return render_template('album_id.html', album_songs=album_songs)

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

    def get_album(self, album_id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.ReadAlbum @AlbumAlbumId=?', album_id)
        return cursor.fetchone()

    def list_albums(self, page, page_size):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.ListAlbums
                @Page=?,
                @pageSize=?
            """, page, page_size)

        return cursor.fetchall()

    def recent_albums(self, page, page_size):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.RecentAlbums
                @Page=?,
                @PageSize=?
            """, page, page_size)

        return cursor.fetchall()

    def get_album_songs(self, album_id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.GetAlbumSongs @AlbumId=?', album_id)
        return cursor.fetchall()