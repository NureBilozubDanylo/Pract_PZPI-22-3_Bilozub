import socket
import queue
import threading
import json
import time

size = 100
board = []
for r_number in range(size):
    r_list = []
    for column_number in range(size):
        r_list.append(' ')
    board.append(r_list)

r_queue = queue.Queue(maxsize=50)

def check_if_player_won(r_index, c_i, symbol):
    count_horizontal = 1
    
    current_column = c_i + 1
    while current_column < 100:
        if board[r_index][current_column] == symbol:
            count_horizontal = count_horizontal + 1
            current_column = current_column + 1
        else:
            break
            
    current_column = c_i - 1
    while current_column >= 0:
        if board[r_index][current_column] == symbol:
            count_horizontal = count_horizontal + 1
            current_column = current_column - 1
        else:
            break

    if count_horizontal >= 5:
        return True

    count_vertical = 1
    
    current_row = r_index + 1
    while current_row < 100:
        if board[current_row][c_i] == symbol:
            count_vertical = count_vertical + 1
            current_row = current_row + 1
        else:
            break
            
    current_row = r_index - 1
    while current_row >= 0:
        if board[current_row][c_i] == symbol:
            count_vertical = count_vertical + 1
            current_row = current_row - 1
        else:
            break

    if count_vertical >= 5:
        return True

    count_diagonal_one = 1
    
    current_row = r_index + 1
    current_column = c_i + 1
    while current_row < 100 and current_column < 100:
        if board[current_row][current_column] == symbol:
            count_diagonal_one = count_diagonal_one + 1
            current_row = current_row + 1
            current_column = current_column + 1
        else:
            break
            
    current_row = r_index - 1
    current_column = c_i - 1
    while current_row >= 0 and current_column >= 0:
        if board[current_row][current_column] == symbol:
            count_diagonal_one = count_diagonal_one + 1
            current_row = current_row - 1
            current_column = current_column - 1
        else:
            break

    if count_diagonal_one >= 5:
        return True

    count_diagonal_two = 1
    
    current_row = r_index + 1
    current_column = c_i - 1
    while current_row < 100 and current_column >= 0:
        if board[current_row][current_column] == symbol:
            count_diagonal_two = count_diagonal_two + 1
            current_row = current_row + 1
            current_column = current_column - 1
        else:
            break
            
    current_row = r_index - 1
    current_column = c_i + 1
    while current_row >= 0 and current_column < 100:
        if board[current_row][current_column] == symbol:
            count_diagonal_two = count_diagonal_two + 1
            current_row = current_row - 1
            current_column = current_column + 1
        else:
            break

    if count_diagonal_two >= 5:
        return True

    return False

def game_function():
    while True:
        request_data = r_queue.get(block=True)
        player_symbol = request_data.get('player')
        row_index = request_data.get('row')
        column_index = request_data.get('col')

        if row_index >= 0 and row_index < 100 and column_index >= 0 and column_index < 100:
            if board[row_index][column_index] == ' ':
                board[row_index][column_index] = player_symbol
                print("Игрок " + str(player_symbol) + " поставил на строку " + str(row_index) + " и колонку " + str(column_index))
                
                is_winner = check_if_player_won(row_index, column_index, player_symbol)
                if is_winner == True:
                    print("Игрок " + str(player_symbol) + " собрал 5 в ряд")
            else:
                print("Єта клетка уже занята")
        else:
            print("Неправильные координаты")
            
        r_queue.task_done()

def start_function():
    logic_thread = threading.Thread(target=game_function)
    logic_thread.daemon = True
    logic_thread.start()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 65432))
    server_socket.listen(10)
    server_socket.setblocking(False)

    list_of_clients = []
    print("Сервер запущен")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            client_socket.setblocking(False)
            list_of_clients.append(client_socket)
            print("Игрок подключился")
        except BlockingIOError:
            pass

        for current_client_socket in list_of_clients.copy():
            try:
                received_data = current_client_socket.recv(1024)
                if len(received_data) > 0:
                    data_string = received_data.decode('utf-8')
                    messages_list = data_string.strip().split('\n')
                    
                    for message in messages_list:
                        if len(message) > 0:
                            json_data = json.loads(message)
                            
                            queue_size = r_queue.qsize()
                            if queue_size < 50:
                                r_queue.put(json_data, block=False)
                            else:
                                print("Очередь переполнена!")
                else:
                    print("Игрок отключился")
                    list_of_clients.remove(current_client_socket)
                    current_client_socket.close()
                    
            except BlockingIOError:
                pass
            except Exception:
                list_of_clients.remove(current_client_socket)
                current_client_socket.close()

        time.sleep(0.01)

if __name__ == "__main__":
    start_function()