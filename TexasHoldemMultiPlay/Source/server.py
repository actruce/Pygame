import socket
from _thread import *
from Game import Game
import pickle

#server = "192.168.219.102"
server = "192.168.219.171"
port = 5555
player_cnt = Game.MAX_PLAYER_CNT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    
s.listen(player_cnt) # blank means unlimited connections
print("Waiting for a connection, Server Started")

game = Game()

def threaded_client(conn, player):
    conn.send(pickle.dumps(player))
    reply = None

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            data_key = list(data.keys())[0]
            data_val = list(data.values())[0]

            if data_key == "connect_player":
                game.connect_player(player, data_val)
            elif data_key == "player_bet":
                game.player_bet(player, data_val)
            elif data_key == "player_fold":
                game.player_fold(player)
            elif data_key == "player_check":
                game.player_check(player)
            elif data_key == "get_game":
                game.get_game()
            elif data_key == "start_game":
                game.start_game(player) 
            elif data_key == "init_round":
                game.init_round(player)
            elif data_key == "preflop":
                game.preflop(player)
            elif data_key == "flop":
                game.flop(player)
            elif data_key == "turn":
                game.turn(player)
            elif data_key == "river":
                game.river(player)
            elif data_key == "showdown":
                game.showdown(player)
            elif data_key == "quitround":
                game.quitround(player)
            
            if data_key != "get_game":
                print("player {0}: , data_key {1}, data_val {2}".format(player, data_key, data_val))
            
            reply = game.reply_to_client()
            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print (str(e))
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1