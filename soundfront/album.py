from flask import (Blueprint, render_template, current_app, request)

bp = Blueprint('album', __name__, url_prefix='/albums')


@bp.route('/', methods=['GET'])
def album_home():
    page = request.args.get('page')
    if page is None: page = 1
    
    album_repo = current_app.config['album']
    albums = album_repo.recent_albums(page=page, page_size=15)
    return render_template('albums/index.html', albums=albums, page=int(page))

@bp.route('/<album_id>', methods=['GET'])
def album(album_id):
    album_repo = current_app.config['album']
    album_songs = album_repo.list_songs(album_id)
    # TODO: Add check for when the album_id is not found.
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

    def list_songs(self, album_id):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.GetAlbumSongs @AlbumId=?', album_id)
        return cursor.fetchall()

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

    