import logging
import threading
import time
import concurrent.futures


class Fila:
    def __init__(self):
        self.fila_comandos = []
        self.entrada_lock = threading.Lock()
        self.saida_lock = threading.Lock()
        self.saida_lock.acquire()

    def entrada(self, comando):
        logging.info("Thread : starting update")
        logging.debug("Thread about to lock")
        self.entrada_lock.acquire()
        if len(self.fila_comandos) >= 64:
            print('fila cheia') 
        else:
            self.fila_comandos.append(comando)
        self.entrada_lock.release()    


    def saida(self):
        logging.info("Thread : starting delete")
        logging.debug("Thread about to lock")
        self.entrada_lock.acquire()
        if len(self.fila_comandos)>0:
            del self.fila_comandos[0]
        self.entrada_lock.release()
        
        logging.debug("Thread after release")
        logging.info("Thread  finishing delete")             

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

def consumidor(fila):
    if len(fila.fila_comandos) > 5:
        #with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        #    executor.submit(fila.saida)
            fila.saida()
            print('Tamanho da fila', fila.fila_comandos)
            print('Tamanho da fila', len(fila.fila_comandos))
    elif len(fila.fila_comandos) <= 0:
        print('fila vazia')  
    #else:
    #    print('<10')  
    print('to rodando em bg')    
    threading.Timer(5.0, consumidor,[fila]).start()

fila = Fila()
first_pass = True
#t = threading.Timer(5.0, consumidor,[fila]).start
#t.start()
consumidor(fila)

x = threading.Thread(target=produtor, args=(fila,), daemon=True)
x.start()
#while True:
    #comando = input('Digite o comando: ')
    #print('Comando escolhido foi', comando)
    #fila.entrada(comando) 
    #time.sleep(1)
'''
    if first_pass == True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        #    print('a')
        #    executor.submit(produtor, fila)
        #    print('b')
            executor.submit(consumidor, fila)
            print('c')
            first_pass = False
    '''


