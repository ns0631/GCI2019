import socket, time, sys, os, subprocess

class socket_client:
    def __init__(self):
        #this Functions as the transmitter
        try:
            port = 31989
            shell_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            requested_ip_address = input('Enter the IP address with which you\'d like to connect: ')
            shell_socket.connect((requested_ip_address, port))
            user_name = input('Enter your username: ')
            while 1:
                try:
                    command = input('Send a command: ').lower()
                    if command == "quit" or command == "exit" or command == "logout" or command == "bye" or command == "goodbye":
                        shell_socket.sendall(bytes('quit', 'UTF-8'))
                        print('This shell is now closed.')
                        shell_socket.close()
                        sys.exit()
                    shell_socket.sendall(bytes(command, 'UTF-8'))
                    received_data = shell_socket.recv(4096).decode('UTF-8').lower()
                    print('pysh:', received_data)
                    if received_data == 'timeout':
                        print('Program timed out.')
                except(KeyboardInterrupt, EOFError):
                    print('To quit, type \'bye\'.')
        except ConnectionRefusedError:
            print('You must activate the server before making a connection.')
            sys.exit()
        except OSError as os_error:
            os_error_code = ((str(os_error)).lower()).rstrip('\n')
            if os_error_code == '[errno 51] network is unreachable':
                print('It looks like your internet connection is a bit slow. Try fixing that or try a little later.')
                shell_socket.close()
                sys.exit()
            elif os_error_code == '[errno 48] address already in use':
                print('It looks like you are unable to connect. Try a little later, please.')
                shell_socket.close()
                sys.exit()
            elif os_error_code == '[errno 57] socket is not connected':
                print('You must activate the server before making a connection.')
                shell_socket.close()
                sys.exit()
            elif os_error_code == "[errno 49] can't assign requested address":
                print('You must activate the server before making a connection.')
                shell_socket.close()
                sys.exit()
        except socket.gaierror as gaierror:
            gaierror_code = str(gaierror)
            print('Oops! It looks like the host was not found. Try again later or try resetting the host connection.')
            print('Error code:', str(gaierror_code).rstrip('\n'))
        except (socket.timeout, TimeoutError):
            prunt('The server took too long to respond. ')
        except SystemExit:
            pass
        except:
            exception = str(sys.exc_info()[0])
            print('An unexpected exception occurred. Exception:', exception)

if __name__ == '__main__':
    try:
        instance = socket_client()
    except(KeyboardInterrupt, EOFError):
        print('\nEnding client program.')
