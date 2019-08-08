import player as pl

def parse_player_record (player):
    (name, path, newCodeAvailable, last_seen, rank, skill, mu, sigma, ngames, active) = player
    return pl.Player(name, path, newCodeAvailable, last_seen, rank, skill, mu, sigma, ngames, active)
    

