import random
import string
import sys
import requests
import json

from db import Database
from user import UserRepo
from album import AlbumRepo
from song import SongRepo
from tag import TagRepo

from faker import Faker
fake = Faker()

database = Database()
database.connect()

user_repo = UserRepo(database.conn)
album_repo = AlbumRepo(database.conn)
song_repo = SongRepo(database.conn)
tag_repo = TagRepo(database.conn)

api_url = 'http://ws.audioscrobbler.com/2.0/'

if len(sys.argv) > 1 and sys.argv[1] == '--real':
    # create 50 totally random users to review the music
    reviewers = []
    for x in range(0, 50):
        user = user_repo.create_user(
            email=fake.email(),
            display_name=fake.name(),
            password='password'
        )

        reviewers.append(user)

    artists = ['Adult Mom', 'Kanye West', 'Death Cab For Cutie', 'Flume', 'Porter Robinson', 'Lomelda', 'Madlib', 'The Microphones', 'Tame Impala', 'Mount Eerie', 'Free Cake For Every Creature', 'Justice', 'Daft Punk', 'Massive Attack', 'Pinegrove', 'Lucy Dacus', 'Weyes Blood', 'American Football', 'LCD Soundsystem', 'The Postal Service', 'Mitski', 'Ben Gibbard', 'Radiohead', 'Father John Misty', 'Yo La Tengo', 'The War on Drugs',
    'Panucci\'s Pizza', 'Daniel Caesar', 'Sufjan Stevens', 'Stars', 'Frankie Cosmos', 'Hop Along']

    for artist in artists:

        user = user_repo.create_user(
            email=fake.email(),
            display_name=artist,
            password='password'
        )

        # call api to get data for up to 5 albums about each specified artist
        album_url = api_url + '?method=artist.gettopalbums&artist=' + artist + '&api_key=c87fd2e998db2442bcca8ed22c08dbf0&format=json'
        api_album_data = requests.get(album_url).content
        parsed_albums = json.loads(api_album_data)
        albums = parsed_albums['topalbums']['album']

        created_albums = []

        num_albums = len(albums)
        if num_albums > 5:
            num_albums = 5

        for i in range(0, num_albums):
            album_name = albums[i]['name']
            album_art = albums[i]['image'][len(albums[i]['image']) - 1]['#text']

            if album_name == '(null)':
                continue

            time_frames = ["-1y", "-30d", "-7d", "-1d"]
            album = album_repo.create_album_with_date(
                user_id=user.UserID,
                album_title=album_name,
                album_art=album_art,
                album_price=random.uniform(0.00, 9.99),
                upload_date=fake.date_time_between(start_date=random.choice(time_frames), end_date="now", tzinfo=None)

            )

            created_albums.append(album)

        for album in created_albums:

            # call api again to get all the songs for this album
            song_url = api_url + '?method=album.getinfo&api_key=c87fd2e998db2442bcca8ed22c08dbf0&format=json&artist=' + artist + '&album=' + album.Title + ''
            api_song_data = requests.get(song_url).content
            parsed_songs = json.loads(api_song_data)

            if 'error' in parsed_songs:
                continue

            songs = parsed_songs['album']['tracks']['track']
            song_tags = parsed_songs['album']['tags']['tag']

            if len(songs) == 0:
                # remove the album since it had no songs
                album_repo.delete_album(album_id=album.AlbumID)
                print('Removing (because no songs were found):\n\tAlbum: ' + album.Title + '\n\t' + 'Artist: ' + artist)
                continue

            # create some ratings for this album
            for n in range(2, len(reviewers)):
                album_rating = album_repo.rate_album(
                    user_id=reviewers[n].UserID,
                    album_id=album.AlbumID,
                    rating=random.randint(0, 10),
                    review_text=fake.sentence(nb_words=random.randint(12, 30))
                )

            # add 2 10/10 ratings to the newest albums to have them appear in top rated area
            for n in range(0, 2):
                album_rating = album_repo.rate_album(
                    user_id=reviewers[n].UserID,
                    album_id=album.AlbumID,
                    rating=10,
                    review_text=fake.sentence(nb_words=random.randint(12, 30))
                )

            # create tags
            created_tags = []
            for song_tag in song_tags:
                try:
                    tag = tag_repo.create_tag(song_tag['name'])
                    created_tags.append(tag)
                except:
                    try:
                        tag = tag_repo.get_tag_by_name(song_tag['name'])
                        if tag is None:
                            continue
                        created_tags.append(tag)
                    except:
                        pass

            # TODO: Currently this makes it so songs get aribrarily tagged with the last 15
            #       tags that were entered whenever we would otherwise be entering 0 tags. We should
            #       change this so that it is adding actually relevant tags to songs in the album
            if len(created_tags) == 0:
                created_tags = tag_repo.list_tags(1, 15)


            for song in songs:
                song_name = song['name']
                song_length = song['duration']

                # create the song
                created_song = song_repo.create_song_with_date(
                    user_id=user.UserID,
                    album_id=album.AlbumID,
                    title=song_name,
                    length=song_length,
                    price=0.99,
                    upload_date=fake.date_time_between(start_date=random.choice(time_frames), end_date="now", tzinfo=None)
                )

                # create a song_tag for every tag that was found for the album
                for tag in created_tags:
                    song_tag = tag_repo.add_song_tag(
                        tag_id=tag.TagID,
                        song_id=created_song.SongID
                    )

                # create some ratings for this song (between 1 and 5 ratings)
                last_reviewer = 0
                for n in range(0, random.randint(1, 5)):
                    song_rating = song_repo.rate_song(
                        user_id=reviewers[n].UserID,
                        song_id=created_song.SongID,
                        rating=random.randint(0, 10),
                        review_text=fake.sentence(nb_words=random.randint(5, 15))
                    )
                    last_reviewer = n

                # create some "bad" ratings for this song (between 1 and 5 ratings)
                for n in range(last_reviewer+1, random.randint(last_reviewer+2, last_reviewer+6)):
                    song_rating = song_repo.rate_song(
                        user_id=reviewers[n].UserID,
                        song_id=created_song.SongID,
                        rating=random.randint(0, 5),
                        review_text=fake.sentence(nb_words=random.randint(5, 15))
                    )

    # create some random follower/following relationships for at most 250 users
    users = user_repo.list_users(1, 250)
    for base_user in users:
        for user in users:
            if user.UserID == base_user.UserID:
                continue
                
            user_repo.follow_user(follower_user_id=base_user.UserID, followee_user_id=user.UserID)

    sys.exit()

# create many faker users
users = []
for x in range(0, 300):
    user = user_repo.create_user(
        email=fake.email(),
        display_name=fake.name(),
        password='password'
    )

    users.append(user)

for user in users:
    # followers following the user
    for x in range(0,10):
        try:
            follower = random.choice(users)
            if follower.UserID is not user.UserID:
                user_repo.follow_user(
                    follower_user_id = follower.UserID,
                    followee_user_id = user.UserID
                )
        except: pass
    # people the user is following
    for x in range(0,10):
        try:
            follower = random.choice(users)
            if follower.UserID is not user.UserID:
                user_repo.follow_user(
                    follower_user_id = user.UserID,
                    followee_user_id = follower.UserID
                )
        except: pass
# create some albums
albums = []
for x in range(0, 300):
    user = random.choice(users)

    album = album_repo.create_album(
        user_id=user.UserID,
        album_title=fake.sentence(nb_words=3)[:-1],
        album_price=random.uniform(0.00, 9.99),
        album_description=fake.text()
    )

    # create some ratings for this album (between 2 and 6)
    for n in range(0, random.randint(2,6)):
        album_rating = album_repo.rate_album(
            user_id=user.UserID,
            album_id=album.AlbumID,
            rating=random.randint(0, 10),
            review_text=fake.sentence(nb_words=random.randint(12, 30))
        )

    albums.append(album)

taglist = []
for x in range(0,5):
    tagName = fake.sentence(nb_words=3)[:-1]

    tag = tag_repo.create_tag(
        name=tagName
    )

    taglist.append(tag)

for album in albums:
    for x in range(1, random.randint(5, 12)):
        song = song_repo.create_song(
            title=fake.sentence(nb_words=4)[:-1],
            userid=album.UserID,
            albumid=album.AlbumID,
            length=random.randint(120,240),
            price=9.99
        )

        tag = random.choice(taglist)

        song_tag = tag_repo.add_song_tag(
            tag_id=tag.TagID,
            song_id=song.SongID
        )

#creating tags for testing
#taglist = []
#for x in range(0,100):
#    tagName = fake.sentence(nb_words=3)[:-1]
#    taglist.append(tagName)
#
#    tag_repo.create_tag(
#        name=tagName
#    )
