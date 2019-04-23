from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)

bp = Blueprint('tag', __name__, url_prefix='/tags')


@bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page')
    if page is None: page = 1
    
    tag_repo = current_app.config['tag']
    tags = tag_repo.list_tags(page=page, page_size=20)
    return render_template('tags/index.html', tags=tags, page=int(page))

class TagRepo():
    def __init__(self, conn):
        self.conn = conn

    def create_tag(self, name=''):
        cursor = self.conn.cursor()
        cursor.execute('EXEC Soundfront.CreateTag @Name=?', name)
        return cursor.fetchone()
		
    def add_song_tag(self, tag_id='', song_id=''):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.AddSongTag
            @TagID=?,
            @SongID=?
            """, tag_id, song_id)
        return cursor.fetchone()
		
    def remove_song_tag(self, song_tag_id=''):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.RemoveSongTag
            @SongTagID=?
            """, song_tag_id)
        return cursor.fetchone()
		
    def list_tags(self, page, page_size):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.ListTags
            @Page=?,
            @PageSize=?
            """, page, page_size)
        return cursor.fetchall()
            
    def get_tags_by_songid(self, song_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.GetTagsBySongID
            @SongID=?
            """, song_id)
        return cursor.fetchall()