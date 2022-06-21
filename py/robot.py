from multiprocessing.connection import wait
from pickle import TRUE
import socket
from sqlite3 import connect
import time
from turtle import right

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Instancia do objeto socket(IPv4, TCP/IP)
#Variaveis Socket
server_IP = "10.0.0.66" # IP do server TCP/IP
server_address = (server_IP,4000) # Endereco do server
sock.bind(server_address) # Associando IP e num porta ao server
sock.listen(1) # Habilitando listening do server

result = 0
counter = 0
####--- Classes


from ast import For


class Fila:
    def __init__(self):
        self.fila_comandos = []

    def entrada(self, comando):
        if len(self.fila_comandos) >= 64:
            print('fila cheia') 
        else:
            self.fila_comandos.append(comando)

    def saida(self):
        del self.fila_comandos[0]


class StateControl:
    def __init__(self):
        self.passo_anterior = 0
        self.passo_atual = 1
        self.proximo_passo = 0
        self.status = 'stopped'

    def next_state(self, proximo_passo):
        if self.status == 'running':
            self.passo_anterior = self.passo_atual
            self.passo_atual = proximo_passo

        elif self.status == 'stopped':
            self.passo_anterior = self.passo_atual
            self.passo_atual = proximo_passo

        elif self.status == 'done':
            self.passo_anterior = self.passo_atual
            self.passo_atual = 0
        
        return self.passo_atual

    def comando(self,comando):
        if comando == 'start':
            self.status = 'running'
        elif comando == 'stop':
            self.status = 'stopped'
        elif comando == 'done':
            self.status = 'done'   
        else:
            self.status = 'stopped'
            print('Erro na maquina de passo')         

class socket_connection:

    def __init__(self):
        self.data = 0
        self.connection = ''
        self.client_address =''
        self.connected = False

    def connect_socket(self):
        wait_socket_connect = True
        print('Esperando por conexao com client!')
        while wait_socket_connect:
            self.connection, self.client_address = sock.accept() # Aguardando conexao do client
            try:
                print('Client conectado (IP,Num Porta): ', self.client_address)
                self.connected = True
            
            finally:
                wait_socket_connect = False
                return self.connected
            #    connection.close()

    def close_socket(self):
        try:
            self.connection.close()
            
        finally:
            print('Comunicação socket finalizada')   

    def read_data(self):
        try:
            data = self.connection.recv(1024).decode('utf-8')
        finally:
            return data    

    def write_data(self, message):
        try:
            self.connection.sendall(message.encode('utf-8')) # Envio dos dados
        finally: 
            return True
  
    
class Robo:
    def __init__(self):
        self.status = '' 
    def handshake_comm(self, socket_sctruct, command):
        try:
            waithandshake = True
            counter = 0
            ack = False
            while waithandshake:
                data = socket_sctruct.read_data()
                
                print('comando',command)
                print('hs',data)
                if data == command:
                    #print('Movimento recebido pelo robo')
                    counter = 0
                    ack = True
                    waithandshake = False
                elif counter >= 10:
                    #print('Falha no envio do comando')
                    ack = False
                    waithandshake = False   

                else:
                    counter += counter

        finally:
            return ack  

    def ControleStatus(self, socket_sctruct):
        try:
            waitstatus = True
            #print('a')
            while waitstatus:   
                #print('b')
                data = socket_sctruct.read_data()
                #print('c')
                #print(data)
                
                if data == 'home':
                    #print('robo em home')
                    self.status = 'home'
                    counter = 0
                    waitstatus = False
                elif data == 'idle':
                    #print('robo em Idle')
                    self.status = 'idle'
                    counter = 0
                    waitstatus = False
                elif data == 'cicle':
                    #print('Robo executando Comando')
                    self.status = 'cicle'
                    counter = 0
                    waitstatus = False
                elif data == 'done':
                    #print('Robo finaliou o comando')
                    self.status = 'done'
                    counter = 0
                    waitstatus = False       
                else:
                    counter += counter

        finally:
            connection.write_data(self.status)
            return True


fila = Fila()       
mp_Robo = StateControl()
connection = socket_connection()
robo = Robo()

while True:

    if mp_Robo.passo_atual == 1: #Inicializa MP
        conectado = False
        comando = ''
        conta_comando = 0
        mp_Robo.comando('start')
        mp_Robo.next_state(10)
        print('start')
        
    elif mp_Robo.passo_atual == 10: #Inicializa Comunicação socket com o robo
        connectado = connection.connect_socket()
        if connectado:
            mp_Robo.next_state(20)
            print('Conectado')
        elif not(connectado):
            mp_Robo.next_state(1001)
            print('Erro de Conexão')

    elif mp_Robo.passo_atual == 20: #Verifica se o robo esta em home
        check_status = robo.ControleStatus(connection)
        if check_status:
            #print(robo.status)
            if robo.status == 'home':
                #print('esta em home vai para 30')    
                #send = connection.write_data('start')
                mp_Robo.next_state(30)
            else:
                #print('N esta em home vai para 21', robo.status)
                mp_Robo.next_state(21)
            #print('Conectado')
        elif not(check_status):
            mp_Robo.next_state(1001)
            print('Erro de status')

    elif mp_Robo.passo_atual == 21: #Chama home do robo
        fila.entrada('home')
        comando = fila.fila_comandos[0]
        mp_Robo.next_state(51)
        
    elif mp_Robo.passo_atual == 30: #Reserva
        mp_Robo.next_state(40)

    elif mp_Robo.passo_atual == 40: #Verifica status do robo
        #print('a')
        check_status = robo.ControleStatus(connection)
        print(robo.status)
        #print('b')
        if check_status:
            if robo.status == 'idle':
                #connection.write_data(robo.status)
                mp_Robo.next_state(50)
            elif robo.status == 'cicle':
                mp_Robo.next_state(60)
            elif robo.status == 'done' or robo.status == 'home':
                mp_Robo.next_state(70)
            #print('Conectado')
        elif not(check_status):
            mp_Robo.next_state(1001)
            print('Erro de status')


    elif mp_Robo.passo_atual == 50: #Aguarda Comando para o robo
        #print('a')
        #if conta_comando < 3:
            fila.entrada(input('Digite o comando: '))
            print('Comando escolhido foi', fila.fila_comandos)
            print('Tamanho da fila', len(fila.fila_comandos))
            conta_comando = conta_comando + 1
        #else:
        #comando = input('Digite o comando: ')
        #print('Comando escolhido foi',comando)
            comando = fila.fila_comandos[0]
            #print(comando)
            if len(comando) > 0:
                #print('a')
                mp_Robo.next_state(51)
            elif len(comando) == 0:
                print('Comando Vazio')
                mp_Robo.next_state(50)

    elif mp_Robo.passo_atual == 51: #Envia comando para o robo
        #print('b')
        send = connection.write_data(comando)
        #print('c')
        if send:
            mp_Robo.next_state(52)
            #print('Enviado')
        elif not(send):
            mp_Robo.next_state(1001)
            print('Erro ao enviar')

    elif mp_Robo.passo_atual == 52: #Reserva handshake robo
        print('a')
        ack_commando = robo.handshake_comm(connection, comando)
        print('b')
        if ack_commando:
            print('c')
            #if comando != 'home':
                #print('vai para o 60')
            mp_Robo.next_state(60)
            #elif comando == 'home':
            #mp_Robo.next_state(20)
                #print('vai para o 20')
        else:
            print('Erro')

    elif mp_Robo.passo_atual == 60: #Aguarda execução do comando pelo robo
        print('Robo executando Comando')
        mp_Robo.next_state(40)
        #print('Conectado')

    elif mp_Robo.passo_atual == 70: #Robo finalizou o comando
        fila.saida()
        comando = ''
        print('Done')
        mp_Robo.next_state(40)
        #print('Conectado')        


     ##Finalização MP                       
    elif mp_Robo.passo_atual == 1000: #Finaliza MP
        mp_Robo.comando('done')
        print('executa comando 1')
    elif mp_Robo.passo_atual == 1001: #Para MP
        mp_Robo.comando('stop')

    #Aguarda start do socket
    #Recebe dados
    #data = socket_connection.read_data(socket_sctruct)
    #print(data)
'''    
    while True:
        status_robo = robo.ControleStatus(connection)
        flag = True
        if status_robo == 'idle' and flag == True:
            flag = False                
            #result = input("Digite o lado: ")
            #print("Lado Escolhido foi",result)
            #fila.insere(result)
            #print(fila)
            #print(fila.primeiro.dado)
            #Envia comando para o robo
            #send = connection.write_data(result)
            #print(send)
            #Aguarda hand shake do comando do robo
            print(robo.handshake_comm(connection, result))
        elif status_robo == 'cicle':
            print('Robo executando Comando') 
        elif status_robo == 'done':
            print('Done')
            flag = True
        else:
            print('')
    
    while send:
        data = socket_connection.read_data(socket_sctruct)
        print(data)
        if data == result:
            print('Movimento recebido pelo robo')
            counter = 0
            send = False
        elif counter >= 10:
            print('Falha no envio do comando')
            send = False    
        else:
            counter += counter
    '''
    #while True:
    #    result = input("Digite o lado: ")
    #    print("Lado Escolhido foi",result)
    #    socket_connection.write_data(socket_sctruct, result)
    #    socket_connection.close_socket(socket_sctruct)
        

'''
while True:
    print('Esperando por conexao com client!')
    connection, client_address = sock.accept() # Aguardando conexao do client
    try:
        print('Client conectado (IP,Num Porta): ', client_address)

        while connection:
            #true
            #Verifica Home do Robo
            #result = input("Digite o lado: ")
            #print("Lado Escolhido foi",result)
            status = 'home'
            ack_wait = True
            while ack_wait:
                data = connection.recv(1024).decode('utf-8')
                
                print (data)
                ack_wait = False
                if data == status:
                    print ('ok')
                else:
                    print ('nok')
            #connection.sendall(result.encode('utf-8')) # Envio dos dados de pose ao robo 

                

        with connection:
            #print(f"Connected by {addr}")
            while True:
                data = connection.recv(1024)
                print (data)
                if not data:
                    print('erro')
                    break

                #connection.sendall(data)
            

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
'''        