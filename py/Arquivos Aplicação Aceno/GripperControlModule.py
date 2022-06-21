import cv2
import math

## FUNÇÃO ABRE/FECHA GARRA
class gripperControl():
    
    def control(img,lmList,last_length,last_length_index_middle,result,last_result): 

        if len(lmList) != 0:                              # Laço executado apenas se alguma mão for encontrada
            x1, y1 = lmList[4][1], lmList[4][2]           # Pega as coordenadas da ponta do dedão
            x2, y2 = lmList[8][1], lmList[8][2]           # Pega as coordenadas da ponta do indicador
            cx, cy = (x1 + x2)//2, (y1 + y2)//2           # Ponto médio entre as coordenadas obtidas
            x3, y3 = lmList[0][1], lmList[0][2]           # Pega as coordenadas do punho
            x4, y4 = lmList[12][1], lmList[12][2]         # Pega as coordenadas do dedo medio
            
            length = math.hypot(x2 - x1, y2 - y1)              # Calcula a distância entre os dois dedos (dedão e indicador)
            length_index_middle = math.hypot(x4 - x2, y4 - y2) # Calcula a distância entre os dois dedos (dedão e indicador)
            size_hand = abs(y3-y4)                             # Distancia vertical entre punho e dedo medio detectados
            nominal_size = 250.0                               # Tamanho nominal da mao em uma distancia que funciona bem

            offset_scale = 50*(size_hand/nominal_size)
            #offset_index_middle = 35*(size_hand/nominal_size)
            
            print(f"Length: {length}")
            print(f"Length Index Middle: {length_index_middle}")
            print(f"Vertical size of hand: {size_hand}")

            print(f"Difference Length: {length-last_length}")
            print(f"Difference Index-Middle: {length_index_middle-last_length_index_middle}")

            print(f"Offset scale: {offset_scale}")
            #print(f"Offset index-middle: {offset_index_middle}")
            print("-------------------------------")

            #difference = length_index_middle - last_length_index_middle
            last_length_index_middle = length_index_middle
            
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)  # Desenha Círculo Vermelho no Ponto 01
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED)  # Desenha Círculo Vermelho no Ponto 02
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)  # Desenha Círculo Vermelho no Ponto Médio
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)       # Desenha Linha entre os 03 pontos

            if length > (last_length + offset_scale) and length >= 0.5*size_hand:        # Verifica se o movimento da mão é de abrir
                #if difference < -offset_index_middle:
                result = "OPEN GRIPPER"                                                  # Altera a string de resultado para "OPEN GRIPPER"
                if (result != last_result):                                              # Entra no laço caso o resultado atual seja diferente do anterior
                    last_length   = length                                               # Troca o objeto de comparação (a atual vira largura anterior)
                    last_length_index_middle = length_index_middle
                last_result   = result                                                   # Troca o objeto de comparação (o atual vira resultado anterior)
            elif length < (last_length - offset_scale) and length <= 0.1*size_hand:      # Verifica se o movimento da mão é de fechar
                #if difference > offset_index_middle:
                result = "CLOSE GRIPPER"                                                 # Altera a string de resultado para "CLOSE GRIPPER"
                if (result != last_result):                                              # Entra no laço caso o resultado atual seja diferente do anterior
                    last_length   = length                                               # Troca o objeto de comparação (a atual vira largura anterior)
                    last_length_index_middle = length_index_middle
                last_result   = result                                                   # Troca o objeto de comparação (o atual vira resultado anterior)

        return last_length,last_length_index_middle,result,last_result                   # Retorna os resultados da função