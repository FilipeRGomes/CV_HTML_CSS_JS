from math import prod
from multiprocessing.connection import wait
from pickle import TRUE
import socket
import threading

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
        self.lock = threading.Lock()

    def entrada(self, comando):
        #self.lock.acquire()
        if len(self.fila_comandos) >= 64:
            print('fila cheia') 
        else:
            self.fila_comandos.append(comando)
        #self.lock.release()
        
    def saida(self):
        #self.lock.acquire()
        if len(self.fila_comandos)>0:
            del self.fila_comandos[0]    
        #self.lock.release()
        
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
            #print('read', data)
            return data    

    def write_data(self, message):
        try:
            self.connection.sendall(message.encode('utf-8')) # Envio dos dados
        finally: 
            return True
  
    
class Robo:
    def __init__(self):
        self.status = '' 
        self.posicao = ''
    def handshake_comm(self, socket_sctruct, command):
        try:
            waithandshake = True
            counter = 0
            ack = False
            #while waithandshake:
            data = socket_sctruct.read_data()
                
                #print('comando',command)
                #print('hs',data)
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
    #####-----------
    def ControleStatus(self, socket_sctruct):
        try:
            waitstatus = True
            i = 0
            #print('a')
            while waitstatus:   
                #print('b')
                estatus = socket_sctruct.read_data()
                #print('c')
                #print(estatus)

                if estatus == 'idle':
                    #print('robo em Idle')
                    self.status = 'idle'
                    counter = 0
                    waitstatus = False
                elif estatus == 'cicle':
                    #print('Robo executando Comando')
                    self.status = 'cicle'
                    counter = 0
                    waitstatus = False
                elif estatus == 'done':
                    #print('Robo finaliou o comando')
                    self.status = 'done'
                    counter = 0
                    waitstatus = False       
                else:
                    counter += counter

        finally:
            #for i in range(1):
            connection.write_data(self.status)
            print(self.status)
            return True
            
    #####-----------
    def ControlePosicao(self, socket_sctruct):
        try:
            waitposicao = True
            #print('a')
            while waitposicao:   
                #print('b')
                pos = socket_sctruct.read_data()
                #print('c')
                #print(data)
                
                if pos == 'home':
                    #print('robo em home')
                    self.posicao = 'home'
                    counter = 0
                    waitposicao = False
                elif pos == 'direita':
                    #print('robo em Idle')
                    self.posicao = 'direita'
                    counter = 0
                    waitposicao = False

                elif pos == 'sobe':
                    #print('robo em Idle')
                    self.posicao = 'sobe'
                    counter = 0
                    waitposicao = False
        
                else:
                    counter += counter

        finally:
            #for i in range(5):
            #    connection.write_data(self.posicao)
            #    print(self.status)
            #connection.write_data(self.posicao)
            return True

fila = Fila()       
mp_Robo = StateControl()
connection = socket_connection()
robo = Robo()


def RecebeComando(fila):
    fila.entrada(input('Digite o comando: '))
    print('Comando escolhido foi', fila.fila_comandos)
    print('Tamanho da fila', len(fila.fila_comandos))
    conta_comando = conta_comando + 1



def mp_controle_robo(connectado):
    while True:
        if mp_Robo.passo_atual == 1: #Inicializa MP
            conectado = False
            comando = ''
            conta_comando = 0
            em_posicao = False
            mp_Robo.comando('start')
            mp_Robo.next_state(10)
            print('start')
            
        elif mp_Robo.passo_atual == 10: #Inicializa Comunicação socket com o robo
            #connectado = connection.connect_socket()
            if connectado:
                mp_Robo.next_state(20)
                print('Conectado')
            elif not(connectado):
                mp_Robo.next_state(1001)
                print('Erro de Conexão')
        
        elif mp_Robo.passo_atual == 20: #Reserva
            mp_Robo.next_state(30)

    ###---STATUS DO ROBO
        elif mp_Robo.passo_atual == 30: #Atualiza status do robo
                #check_status = False
                #print('a')
                if em_posicao:
                    check_status = True
                elif not(em_posicao):    
                    check_status = robo.ControleStatus(connection)

                #print(robo.status)
                #print('b')
                if check_status:
                    #print('a')
                    print('Fila aq:',len(fila.fila_comandos))
                    print('status:',robo.status)
                    if robo.status == 'idle':
                        connection.write_data(robo.status)
                        print('c')
                        mp_Robo.next_state(40)
                    elif robo.status == 'cicle':
                        mp_Robo.next_state(200)
                    elif robo.status == 'done':
                        mp_Robo.next_state(70)
                    #print('Conectado')
                elif not(check_status):
                    mp_Robo.next_state(1001)
                    print('Erro de status')

    ##--- ROTINA POS IDLE
        elif mp_Robo.passo_atual == 40: #RESERVA (pos idle)
            mp_Robo.next_state(50)

        elif mp_Robo.passo_atual == 50: #Atualiza posição do robo
                check_status = False
                if em_posicao:
                    check_status = True
                
                elif not(em_posicao):        
                    check_pos = robo.ControlePosicao(connection)
                
                #print('P50',robo.posicao)
                #print('b')
                if check_pos:
                    mp_Robo.next_state(60)
                elif not(check_pos):
                    mp_Robo.next_state(1001)
                    print('Erro de posicao')  

        elif mp_Robo.passo_atual == 60: #Aguarda Comando para o robo
            #print('a')

            # Logica com fila    
            #if conta_comando < 10:
            #    fila.entrada(input('Digite o comando: '))
            #    print('Comando escolhido foi', fila.fila_comandos)
            #    print('Tamanho da fila', len(fila.fila_comandos))
            #    conta_comando = conta_comando + 1

            # Logica sem fila    
            #comando = input('Digite o comando: ')
            #print('Comando escolhido foi',comando)
            #elif conta_comando >= 10:  and len(fila.fila_comandos) > 0


            if len(fila.fila_comandos) > 0:
                    print('P60 -> P70')
                    comando = fila.fila_comandos[0]
                    print(comando)
                    mp_Robo.next_state(70)
            elif len(fila.fila_comandos) == 0:
                    #print('Comando Vazio')
                    mp_Robo.next_state(mp_Robo.passo_atual)

        elif mp_Robo.passo_atual == 70: #RESERVA
            mp_Robo.next_state(80)

        elif mp_Robo.passo_atual == 80: #Verifica se o robo esta na posição selecionada
            
            #print(em_posicao)
            if comando == robo.posicao:
                print(' P80 - IN POS')
                em_posicao = True
                mp_Robo.next_state(300) #vai para a rotina de done
            elif comando != robo.posicao:
                #print('Comando Vazio')
                print(' P80 - N POS')
                em_posicao = False
                mp_Robo.next_state(90)

        elif mp_Robo.passo_atual == 90: #Envia comando para o robo
            print('P90')
            send = False
            ack_commando = False
            while not(ack_commando):
                #print('a')
                send = connection.write_data(comando)
                #print('b')
                ack_commando = robo.handshake_comm(connection, comando)
                #print('c')
            
            if send:          
                print('P90 - COMANDO ENVIADO')
                mp_Robo.next_state(110) #era 100
                #print('Enviado')
            elif not(send):
                mp_Robo.next_state(1001)
                print('Erro ao enviar')

        elif mp_Robo.passo_atual == 100: #Aguarda handshake robo
            #print('a')
            print('P100 - hand b')
            ack_commando = robo.handshake_comm(connection, comando)
            
            print('P100 - hand A')
            #print('b')
            if ack_commando:
                print('c')
                mp_Robo.next_state(110)
            else:
                mp_Robo.next_state(mp_Robo.passo_atual)
                print('Erro')

        elif mp_Robo.passo_atual == 110: #RESERVA
            mp_Robo.next_state(200)

    ##--- ROTINA POS CICLE
        elif mp_Robo.passo_atual == 200: #RESERVA (pos CICLE)
            mp_Robo.next_state(210)

        elif mp_Robo.passo_atual == 210: #Aguarda execução do comando pelo robo
            #print('Robo executando Comando',robo.status)
            check_status = False
            check_status = robo.ControleStatus(connection)
            if check_status:
                while robo.status == 'cicle':
                    check_status = robo.ControleStatus(connection)
                if robo.status == 'done':
                    mp_Robo.next_state(300)            
                    print(robo.status)
                else:
                    mp_Robo.next_state(1001)
                    print('Erro no ciclo')
            elif not(check_status):
                mp_Robo.next_state(1001)
                print('Erro de status')        

    ##--- ROTINA DONE

        elif mp_Robo.passo_atual == 300: #RESERVA (done)
            mp_Robo.next_state(310)


        elif mp_Robo.passo_atual == 310: #Robo finalizou o comando
            fila.saida()
            if len(fila.fila_comandos) <= 0:
                conta_comando = 0
            comando = ''
            print('Done')
            mp_Robo.next_state(30)
            #print('Conectado')        


        ##Finalização MP                       
        elif mp_Robo.passo_atual == 1000: #Finaliza MP
            mp_Robo.comando('done')
            print('executa comando 1')
        elif mp_Robo.passo_atual == 1001: #Para MP
            mp_Robo.comando('stop')

def produtor(fila):
    while True:
        comando = input('Digite o comando: ')
        print('Comando escolhido foi', comando)
        fila.entrada(comando) 
    #print('Tamanho da fila', len(fila.fila_comandos))
    #conta_comando = conta_comando + 1
    #with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #    executor.submit(fila.entrada, comando)
        print('Tamanho da fila', fila.fila_comandos)
        print('Tamanho da fila', len(fila.fila_comandos))


connectado = connection.connect_socket()
x = threading.Thread(target=mp_controle_robo, args=(connectado,), daemon=True)
x.start()
produtor(fila)

