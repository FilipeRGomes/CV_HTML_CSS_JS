
class FollowHandControl():
    
    def control(lmlist,last_center_coords,last_fist_coords):

        offset_x = 150
        offset_y = 100
        result = ""

        if len(lmlist) != 0:
            x1, y1 = lmlist[4][1], lmlist[4][2] # Coordenadas do polegar
            x2, y2 = lmlist[20][1], lmlist[20][2] # Coordenadas do mindinho
            x3, y3 = lmlist[0][1],lmlist[0][2] # Coordenadas do punho 

            center_x = (x1+x2)/2
            center_y = (y1+y2)/2

            if last_center_coords[0] != -1.0 and last_center_coords[1] != -1.0:
                if center_x <= last_center_coords[0]-offset_x and x3 <= last_fist_coords[0] - offset_x:
                    result += "DIREITA"
                elif center_x >= last_center_coords[0]+offset_x and x3 >= last_fist_coords[0] + offset_x:
                    if result != "":
                        result += " ESQUERDA"
                    else:
                        result += "ESQUERDA"
                
                if center_y <= last_center_coords[1]-offset_y and y3 <= last_fist_coords[1] - offset_y:
                    if result != "":
                        result += " CIMA"
                    else:
                        result += "CIMA" 
                elif center_y >= last_center_coords[1]+offset_y and y3 >= last_fist_coords[1] + offset_y:
                    if result != "":
                        result += " BAIXO"
                    else:
                        result += "BAIXO"
            
            last_center_coords = (center_x,center_y)
            last_fist_coords = (x3,y3)

        return result,last_center_coords,last_fist_coords