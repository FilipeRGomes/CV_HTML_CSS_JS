import cv2
import socket
import HandTrackingModule as htm
import GripperControlModule as gc
import WaveControlModule as wc
import FollowHandModule as fh
import threading

## Conexão com o Robô
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Instância do objeto socket(IPv4, TCP/IP)
server_IP      = "10.0.0.20"                             # IP do server TCP/IP
server_address = (server_IP, 3000)                       # Endereco do server
sock.bind(server_address)                                # Associando IP e num porta ao server
sock.listen(1)                                           # Habilitando listening do server

## Aquisição da Imagem
wCam = 1366 # Largura da Imagem
hCam = 768  # Altura da Imagem

# Indice da webcam que tera imagem capturada
webcam_number = 0

cap = cv2.VideoCapture(webcam_number,cv2.CAP_DSHOW) # Capturando stream de webcam Logitech
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wCam)  # Define Largura da Janela da WebCam
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hCam) # Define Altura da Janela da WebCam

detector = htm.handDetector(maxHands = 1, detectionCon = 0.7)  # Define variável que chamará função de detecção de mãos.
                                                               # Define quantidade máxima de mãos e threshold de identificação.
## Inicialização de Variáveis - Abre/Fecha Garra
last_length            = 0  # Última largura medida entre dedão e indicador
last_length_ind_middle = 0  # Última largura medida entre indicador e dedo do meio
result_open_close      = "" # Resultado obtido na interação atual com o usuário
last_result            = "" # Resultado obtido na última interação com o usuário
gripperList = []

## Inicialização de Variáveis - Aceno
wave_result   = 0  # Resultado obtido na interação atual com o usuário
last_wave_res = 0  # Resultado obtido na última interação com o usuário
count         = 0  # Contador para evitar que o robô acene em qualquer sinal de movimento do usuário
resList       = [] # Lista com os últimos 06 resultados do aceno do usuário 
angleList     = [] # Lista com os ângulos relativos a movimentação de aceno do usuário
result_wave   = "" # String que contém se usuário fez aceno ou não na atual iteração
waveList = []

## Inicialização das variaveis - Tracking do movimento da mão pela imagem
last_coords = (-1.0,-1.0)
fist_coords = (-1.0,-1.0)
result_follow = ""
last_result_follow = ""
followList = []

lmList = None
first_detection = True

def FollowHandPeriodically():
    ## TRACK DO MOVIMENTO DA MÃO PELA IMAGEM
    global result_follow
    global last_coords
    global fist_coords

    followList = fh.FollowHandControl.control(lmList,last_coords,fist_coords)
            
    result_follow = followList[0]
    last_coords = followList[1]
    fist_coords = followList[2]

    threading.Timer(0.200,FollowHandPeriodically).start()

def FollowWavePeriodically():
    # DETECÇÃO ACENO
    global last_wave_res
    global wave_result
    global result_wave
    global count
    global resList
    global angleList

    waveList = wc.wavingControl.control(lmList,wave_result,last_wave_res,count,resList,angleList,result_wave)

    wave_result = waveList[0]
    last_wave_res = waveList[1]
    count = waveList[2]
    resList = waveList[3]
    angleList = waveList[4]
    result_wave = waveList[5]

    threading.Timer(0.050,FollowWavePeriodically).start()

print("Esperando conexão com cliente!")
while True:

    connection, client_address = sock.accept() # Aguardando conexão com client
    print("Client conectado. Seu endereço IP é " + str(client_address))

    while True:

        success, img = cap.read()                             # Pega o frame atual da WebCam (img)
        if success:
            img = cv2.flip(img,1)                             # Invertendo horizontalmente a imagem
                                                              # Retorna um booleano que diz se o frame foi lido corretamente (success)
            img    = detector.findHands(img)                  # Chama função de detecção das mãos
            lmList = detector.findPosition(img, draw = False) # Gera uma lista com as posições do punho + falanges dos dedos

            if first_detection == True: # Inicializa execução de threads temporizadas
                FollowHandPeriodically()
                FollowWavePeriodically()
                first_detection = False

            ## ABRE/FECHA GARRA        
            controlList = gc.gripperControl.control(img,lmList,last_length,last_length_ind_middle,result_open_close,last_result) # Chama função de abre/fecha garra

            last_length            = controlList[0] # Recebe resultado da variável last_length referente à última execução da função abre/fecha garra
            last_length_ind_middle = controlList[1]
            result_open_close      = controlList[2] # Recebe resultado da variável result referente à última execução da função abre/fecha garra
            last_result            = controlList[3] # Recebe resultado da variável last_result referente à última execução da função abre/fecha garra

            if result_open_close != "":
                cv2.putText(img, result_open_close,(10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                connection.sendall(result_open_close.encode('utf-8'))
                result_open_close = ""
            if result_wave != "":
                cv2.putText(img, result_wave,(10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                connection.sendall(result_wave.encode('utf-8'))
                result_wave = ""
            if result_follow != "":
                if last_result_follow == result_follow:
                    result_follow = ""
                cv2.circle(img,(int(last_coords[0]),int(last_coords[1])),5,(0,255,0),2,cv2.LINE_AA)
                cv2.putText(img, result_follow,(10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                connection.sendall(result_follow.encode('utf-8'))
                result_follow = ""                

            cv2.namedWindow("Live Image", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Live Image",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Live Image", img) # Abre janela da imagem (WebCam)
            cv2.waitKey(1)