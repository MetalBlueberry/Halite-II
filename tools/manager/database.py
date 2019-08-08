import sqlite3
import datetime
import util
import os

import pymysql.cursors

# Connect to the database


class Database:

    def connection(self, db):
        return pymysql.connect(
            host='halitedb.cluster-cgeszsxebj04.us-east-1.rds.amazonaws.com',
            user="admin",
            password=os.environ['DB_PASSWORD'],
            db=db,
            charset='utf8mb4',
            # cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )

    def __init__(self, filename):
        self.db = self.connection(filename)
        self.recreate()

    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def recreate(self):
        cursor = self.db.cursor()
        try:
            cursor.execute("create table results(id int NOT NULL, game_id int, name text, finish int, num_players int, map_width int, map_height int, map_seed int, map_generator text, timestamp DATETIME, logs text, replay_file text)")
            cursor.execute("create table players(name text(100) NOT NULL, path text, newCodeAvailable int, lastseen DATETIME, rank int default 1000, skill real default 0.0, mu real default 25.0, sigma real default 8.33,ngames int default 0, active int default 1, primary key (name(100)))")
            self.db.commit()
        except:
            pass

    def update_deferred(self, sql, tup=()):
        cursor = self.db.cursor()
        cursor.execute(sql, tup)

    def update(self, sql, tup=()):
        self.update_deferred(sql, tup)
        self.db.commit()

    def update_many(self, sql, iterable):
        cursor = self.db.cursor()
        cursor.executemany(sql, iterable)
        self.db.commit()

    def retrieve(self, sql, tup=()):
        cursor = self.db.cursor()
        cursor.execute(sql, tup)
        return cursor.fetchall()

    def add_match(self, match):
        sql = 'SELECT max(game_id) FROM results'
        game_id = self.retrieve(sql)[0][0]
        game_id = int(game_id) + 1 if game_id else 1
        self.update_many("INSERT INTO results (game_id, name, finish, num_players, map_width, map_height, map_seed, map_generator, timestamp, logs, replay_file) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [
                         (game_id, player.name, rank, match.num_players, match.map_width, match.map_height, match.map_seed, match.map_generator, self.now(), str(match.logs), str(match.replay_file)) for player, rank in zip(match.players, match.results)])

        # for player, rank in zip(match.players, match.results):
        #    print(player, rank)
        #    self.update_many("INSERT INTO results (game_id, name, finish, num_players, map_width, map_height, map_seed, map_generator, timestamp, logs, replay_file) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [(game_id, player.name, rank, match.num_players, match.map_width, match.map_height, match.map_seed, match.map_generator, self.now(), str(match.logs), str(match.replay_file))])

    def add_player(self, name, path, active=True):
        self.update("insert into players  (name, path, newCodeAvailable, lastseen, rank, skill, mu, sigma ,ngames, active) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (name, path, 1, self.now(), 1000, 0.0, 25.0, 25.0/3.0, 0, active))

    def delete_player(self, name):
        self.update("delete from players where name=%s", [name])

    def get_players(self):
        player_records = self.retrieve(
            "select * from players where active > 0")
        players = [util.parse_player_record(player) for player in player_records]
        return players

    def get_player(self, names):
        sql = 'select * from players where name=%s ' + \
            ' '.join('or name=%s' for _ in names[1:])
        return self.retrieve(sql, names)

    def get_result(self, game_id):
        sql = 'select * from results where game_id=%s '
        return self.retrieve(sql, game_id)

    def get_results(self, offset, limit):
        sql = 'SELECT game_id, GROUP_CONCAT(name), GROUP_CONCAT(finish), map_width, map_height, map_seed, map_generator, timestamp, logs, replay_file FROM results GROUP BY game_id ORDER BY game_id DESC LIMIT %d OFFSET %d' % (
            limit, offset)
        return self.retrieve(sql)

    def get_replay_filename(self, id):
        print(id)
        sql = 'SELECT replay_file FROM results WHERE game_id = %s'
        result = self.retrieve(sql, (id,))
        print(result[0][0])
        return result[0][0]

    def get_last_replay_filename(self):
        print(id)
        sql = 'SELECT replay_file FROM results ORDER BY game_id desc LIMIT 1'
        result = self.retrieve(sql)
        print(result[0][0])
        return result[0][0]

    def save_player(self, player):
        self.update_player_skill(
            player.name, player.skill, player.mu, player.sigma)

    def update_player_skill(self, name, skill, mu, sigma):
        self.update("update players set ngames=ngames+1,lastseen=%s,skill=%s,mu=%s,sigma=%s where name=%s",
                    (self.now(), skill, mu, sigma, name))

    def update_player_rank(self, name, rank):
        self.update("update players set rank=%s where name=%s", (rank, name))

    def update_player_ranks(self):
        for i, p in enumerate(self.retrieve("select name from players order by skill desc", ())):
            self.update_player_rank(p[0], i+1)

    def activate_player(self, name):
        self.update("update players set active=%s where name=%s", (1, name))

    def deactivate_player(self, name):
        self.update("update players set active=%s where name=%s", (0, name))

    def update_player_path(self, name, path):
        self.update(
            "update players set path=%s, newCodeAvailable=1 where name=%s", (path, name))
    
    def update_player_code_loaded(self, name):
        self.update(
            "update players set newCodeAvailable=0 where name=%s", (name))

    def reset(self, filename):
        players = list(map(util.parse_player_record,
                           self.retrieve('select * from players')))
        assert players, 'No players recovered from database%s  Reset aborted.'
        # blow out database
        self.update("drop table players")
        self.update("drop table results")

        self.recreate()
        for player in players:
            self.add_player(player.name, player.path, player.active)
