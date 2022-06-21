import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Instancia do objeto socket(IPv4, TCP/IP)

server_IP = "10.0.0.66" # IP do server TCP/IP
server_address = (server_IP,4000) # Endereco do server
sock.bind(server_address) # Associando IP e num porta ao server
sock.listen(1) # Habilitando listening do server

result = 0
counter = 0

while True:
    print('Esperando por conexao com client!')
    connection, client_address = sock.accept() # Aguardando conexao do client
    try:
        print('Client conectado (IP,Num Porta): ', client_address)
        while True:
            result = input("Digite o lado: ")
            print("Lado Escolhido foi",result) 
            result = "(" + result + ")"

            if(result == "(1)" ):
                connection.sendall(result.encode('utf-8')) # Envio dos dados de pose ao robo
                print("Esquerda")
                time.sleep(1)
                
            if(result == "(2)" ):
                connection.sendall(result.encode('utf-8')) # Envio dos dados de pose ao robo
                print("Direita")
                time.sleep(1)

            print("Valor:", result)

    finally:
        connection.close()

class TestGit:
    github = "Em Teste"