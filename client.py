import socket
import json
import time

def send_move_to_server(client_socket, player_symbol, row_index, column_index):
    move_dictionary = {}
    move_dictionary["player"] = player_symbol
    move_dictionary["row"] = row_index
    move_dictionary["col"] = column_index
    
    json_string = json.dumps(move_dictionary)
    message_to_send = json_string + "\n"
    
    encoded_message = message_to_send.encode('utf-8')
    client_socket.sendall(encoded_message)
    
    print("Отправили ход: Игрок " + str(player_symbol) + " на координаты " + str(row_index) + ", " + str(column_index))

def start_client_function():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 65432))
    print("Подключились к серверу")

    send_move_to_server(client_socket, "X", 10, 10)
    time.sleep(0.5)
    
    send_move_to_server(client_socket, "O", 10, 11)
    time.sleep(0.5)
    
    send_move_to_server(client_socket, "X", 11, 10)
    time.sleep(0.5)
    
    send_move_to_server(client_socket, "O", 10, 12)
    time.sleep(0.5)
    
    send_move_to_server(client_socket, "X", 12, 10)
    time.sleep(0.5)
    
    send_move_to_server(client_socket, "O", 10, 13)
    time.sleep(0.5)
    
    send_move_to_server(client_socket, "X", 13, 10)
    time.sleep(0.5)
    
    send_move_to_server(client_socket, "X", 14, 10)
    
    time.sleep(2)
    client_socket.close()
    print("Соединение закріто")

if __name__ == "__main__":
    start_client_function()