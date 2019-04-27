from flask import (Blueprint, flash, g, redirect,
                   render_template, request, session, url_for, current_app)

bp = Blueprint('tag', __name__, url_prefix='/tags')


@bp.route('/', methods=['GET'])
def index():
    page = request.args.get('page')
    if page is None: 
        page = 1

    pagination_data = {}
    pagination_data['page'] = int(page)
    pagination_data['href'] = '/tags'
    pagination_data['add_button_text'] = 'Add a Tag'
    
    tag_repo = current_app.config['tag']
    tags = tag_repo.list_tags(page=page, page_size=50)
    return render_template('tags/index.html', tags=tags, page=int(page), pagination_data=pagination_data)
    
@bp.route('/<tag_id>', methods=['GET'])
def index_id(tag_id):
    page = request.args.get('page')
    if page is None: page = 1
    
    pagination_data = {}
    pagination_data['page'] = int(page)
    pagination_data['href'] = '/tags/'+str(tag_id)
      
    tag_repo = current_app.config['tag']
    tag_songs = tag_repo.list_songs_by_tag(tag_id, page=page, page_size=20)

    tag = tag_repo.read_tag(tag_id)
    # TODO: Add check for when the tag_id is not found.
    return render_template('tags/tag_id.html', tag_songs=tag_songs, page=int(page), tag=tag, pagination_data=pagination_data)

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
        
    def list_songs_by_tag(self, tag_id, page, page_size):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.ListSongsByTag
            @TagID=?,
            @Page=?,
            @PageSize=?
            """, tag_id, page, page_size)
        return cursor.fetchall()

    def read_tag_by_name(self, tag_name):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.ReadTagByName
            @TagName=?
         """, tag_name)
        return cursor.fetchone()
        
    def read_tag(self, tag_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            EXEC Soundfront.ReadTag
            @TagID=?
            """, tag_id)
        return cursor.fetchone()