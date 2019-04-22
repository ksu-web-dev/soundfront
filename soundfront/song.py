from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)

bp = Blueprint('songs', __name__, url_prefix='/songs')


@bp.route('/', methods=['GET'])
def index():
    return render_template('songs/index.html')


@bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        album = request.form['album'] or None
        price = request.form['price']
        length = request.form['length']
        description = request.form['description']

        error = None

        if not title:
            error = 'Title is required.'
        elif not price:
            error = 'Price is required.'
        elif not session['user_id']:
            return redirect(url_for('auth.login'))

        if error is None:
            repo = current_app.config['song']
            user_id = session['user_id']
            repo.insert_song(user_id, album, title, length, price, description)
            return redirect(url_for('songs.index'))

        flash(error)

    return render_template('songs/new.html')


class SongRepo():
    def __init__(self, conn):
        self.conn = conn

    def insert_song(self, userid='', albumid=None, title='', length=0, price=0, description=''):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.InsertSong
                @UserID=?,
	            @AlbumID=?,
	            @Title=?,
	            @Length=?,
	            @Price=?,
	            @Description=?
            """, userid, albumid, title, length, price, description)
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
        cursor.execute(
            'EXEC Soundfront.ListSong @Page=?, @PageSize=?', page, pagesize)
        return cursor.fetchall()
