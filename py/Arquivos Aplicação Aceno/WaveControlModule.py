from math import atan2, degrees
import cv2

# FUNÇÃO CHECA ACENO
class wavingControl():
    
    def control(lmList,wave_result,last_wave_res,count,resList,angleList,result):
        
        list01 = [1, -1, 1, -1, 1, -1]
        list02 = [-1, 1, -1, 1, -1, 1]

        angleList_1 = [True,False,True,False,True,False]
        angleList_2 = [False,True,False,True,False,True]
        sequence_angles = [True,True,True,True,True,True]

        if len(lmList) != 0:                              # Laço executado apenas se alguma mão for encontrada
            x1, y1 = lmList[4][1], lmList[4][2]           # Pega as coordenadas da ponta do dedão
            x2, y2 = lmList[20][1], lmList[20][2]         # Pega as coordenadas da ponta do mindinho
            x3, y3 = lmList[0][1],lmList[0][2]            # Pega as coordenadas do punho  
            diff   = y2 - y1                              # Calcula a diferença da coordenada Y dos dois dedos (dedão e mindinho)
            angle = degrees(atan2(y3-y1,x3-x1))

            #cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED) # Desenha Círculo Vermelho no Ponto 01
            #cv2.circle(img, (x2, y2), 15, (0, 0, 255), cv2.FILLED) # Desenha Círculo Vermelho no Ponto 02
            #cv2.circle(img, (x3, y3), 15, (0, 0, 255), cv2.FILLED) # Desenha Círculo Vermelho no Ponto 03

            if diff > 0:                               # Entra no laço caso a diferença seja maior que 0
                wave_result = 1                        # Altera a variável de resultado atual para 1
            elif diff < 0:                             # Entra no laço caso a diferença seja menor que 0
                wave_result = -1                       # Altera a variável de resultado atual para -1
            
            if (wave_result != last_wave_res):         # Entra no laço caso o resultado atual seja diferente do anterior
                resList.insert(count, wave_result)     # Insere o resultado atual na lista
                angleList.insert(count,angle)          # Insere o ângulo do frame atual
                count += 1                             # Incrementa o contador
            last_wave_res = wave_result                # Troca o objeto de comparação (o atual vira resultado anterior)

            ## Verifica se o contador chegou em 6 e se a lista de resultados é igual a um dos dois possíveis resultados
            if (count == 6):
                counter = 0
                for item in angleList:
                    if counter == 0 or counter == 2 or counter == 4:
                        if item > 30.0:
                            sequence_angles.insert(counter,True)
                        else:
                            sequence_angles.insert(counter,False)
                    else:
                        if sequence_angles[counter-1] == True:
                            if item < 30.0:
                                sequence_angles.insert(counter,False)
                            else:
                                sequence_angles.insert(counter,True)
                    counter += 1

                if ((set(resList) == set(list01)) or (set(resList) == set(list02))) or ((set(sequence_angles) == set(angleList_1)) or (set(sequence_angles) == set(angleList_2))) and (abs(max(angleList) - min(angleList)) > 30.0):
                    result = "ACENAR" # Altera a string de resultado para "ACENAR"

            if count > 5:               # Entra no laço caso o contador seja maior que 5
                count = 0               # Zera contadores 
                resList.clear()         # Limpa lista de resultados
                angleList.clear()       # Limpa lista dos angulos
                sequence_angles.clear() # Limpa lista da sequencia de angulos detectados

        return wave_result,last_wave_res,count,resList,angleList,result # Retorna os resultados da função