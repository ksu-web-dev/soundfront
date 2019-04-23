from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)

bp = Blueprint('tags', __name__, url_prefix='/tags')


@bp.route('/', methods=['GET'])
@bp.route('/<page>', methods=['GET'])
def index(page=1):
    repo = current_app.config['tags']
    tags = repo.list_song(page, 20)
    return render_template('songs/index.html', songs=songs, page=int(page))


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


class TagRepo():
    def __init__(self, conn):
        self.conn = conn

	def create_tag(self, name=''):
		cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.CreateTag
                @Name=?
            """, name)
        return cursor.fetchone()
		
	def add_song_tag(self, tagid='', songid=''):
		cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.AddSongTag
                @TagID=?,
				@SongID=?
            """, tagid, songid)
        return cursor.fetchone()
		
	def remove_song_tag(self, songtagid=''):
		cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.RemoveSongTag
                @SongTagID=?
            """, songtagid)
        return cursor.fetchone()
		
	def list_tags(self, page, pagesize):
		cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.ListTags
                @Page=?,
				@PageSize=?
            """, page, pagesize)
        return cursor.fetchone()
		
	def get_tags_by_songid(self, songid):
		cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.GetTagsBySongID
                @SongID=?
            """, songid)
        return cursor.fetchone()