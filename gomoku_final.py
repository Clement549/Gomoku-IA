import time

def custom_main():
    chess = board_chess() # initialisation du plateau
    ai = computerplayer( chess._chess_board) #l'IA joue son 1er coups
    i=1
    
    if(computer_ == 2):
        chess._chess_board[7][7] = player_
        tic = time.perf_counter()
        score,step = ai._calc_good_postion()
        toc = time.perf_counter()
        print()
        print ("l\'IA a joué en: " + chr(score+65) + str(step+1) + ' (' + str(round(toc - tic,3)) + ' sec)')
        print()
        chess._chess_board[score][step] = computer_
    else:
        print()
        print('L\'IA place son 1er pion en H8', end="\n")
        print()

    while(i < nb_pions): # On limite le jeu à 60 tours max
        print (chess.t_ui_print())
        while(True):
            uinput  = input("Entrez une position (quitter-0): ")
            move = uinput
            #move = uinput.split(' ') # un espace entre les 2 lettres
            print()
            if uinput == "0":
                print ('Partie annulée..')
                return 0
            else:
                # On verifie que le joueur a entré une position valide
                if len(move) == 2 or len(move) == 3 and len(move[0]) == 1 and len(move[1]) == 1 :
                    row = ord(move[0].upper())-ord('A') # pos ligne
                    col = int(move[1:])-1 # pos colonne
                    if row>=0 and row< g_rows and col>=0 and col<g_cols:
                        if(chess._chess_board[row][col] == 0):
                            # Position valide
                            # On inscit cette position dans la matrice
                            chess._chess_board[row][col] = player_
                            break
                        else:
                            print ("Position incorrect, il y a déjà un pion ici", end="\n\n")
                            continue
                    else:
                        print ("Position incorrect", end="\n\n")
                        continue
                else:
                    print ("Position incorrect, veuillez réessayer", end="\n\n")
                    continue

        if(chess.judge_over(player_)): # l'humain a aligné 5 pions
            print (chess.t_ui_print())
            print ("Félicitations, vous avez gagné !")
            return 0

        tic = time.perf_counter()
        score,step = ai._calc_good_postion()
        toc = time.perf_counter()
        print ("l\'IA a joué en: " + chr(score+65) + str(step+1) + ' (' + str(round(toc - tic,3)) + ' sec)')
        print()
        chess._chess_board[score][step] = computer_

        if(chess.judge_over(computer_)): #l'IA a aligné 5 pions
            print (chess.t_ui_print())
            print ("l\'IA a prouvé sa superiorité intellectuelle sur vous.")
            return 0
        i+=1
    print (chess.t_ui_print())
    print ("Match nul: vous avez placé toutes vos pièces.")

# Valeur Scores
g_temp_a = 100000
g_temp_b = 10000
g_temp_c = 1000
g_temp_d = 100
g_temp_e = 10
g_temp_f = 1000
g_temp_g = 100
g_temp_h = 10

g_rows = 15
g_cols = 15
nb_pions = 60

# Cette classe détermine quel sera le prochain coups de l'IA
class computerplayer:
    def __init__(self,_chess_board):    
        self.depth = 1
        self.color = 1
        self._chess_board = _chess_board
        self._move_well = (-15,-15)
        # 8 directions avec les diagonales 
        self.step = ( (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1) )

    # Détermination de la prochaine position
    def next_postions(self):
        steps = []
        for i in range(g_rows):
            for j in range(g_cols):
                if(self._chess_board[i][j] != 0):
                    continue
                flag = False 
                for k in self.step:
                    # Vérifie si la position ne sort pas de la matrice
                    if((i+k[0])>=0 and (i+k[0])<15 and(j+k[1]>=0) and (j+k[1]<15) and self._chess_board[i+k[0]][j+k[1]] != 0):
                        flag = True
                        break
                if(flag == False):
                    continue
                steps.append([i,j])
        return steps

   
    # Calcul du score
    def computer_calc(self,color,next_color):
        str_board = self.board_to_str()
        temp_a = 0
        temp_b = 0
        for i in str_board:
            if(str(next_color)*5 in i):
                return -g_temp_a;
            if(str(color)*5 in i):
                return g_temp_a

            # Algorithme des "composite patterns" avec des scores adaptatifs
            # Plutot que de définir un score en fonction du nombre et de la disposition des pions alignés
            # Le score est ici calculé en fonction des combinaisons présentes
            # (Les valeurs des constantes initiales ont été définies par tatonnement)
            # voir le rendu pour plus de details
            temp_b += 3 * g_temp_b*0.5 * i.count(str(color)*2 + '0' + str(color)*2) #11011 = XX-XX
            temp_b += 3 * g_temp_b*0.5 * i.count(str(color) + '0' + str(color) * 3) #01110 = -XXX-
            temp_a += g_temp_b * i.count('0' + str(next_color) * 4 + '0') #01110
            temp_b += 3 * g_temp_b*0.5 * i.count(str(color)*3 + '0' + str(color))#11101
            temp_b += 3 * g_temp_c*0.5 * i.count('0' + str(color) +'0'+str(color)*2+'0') #010110
            temp_b += 3 * g_temp_c*0.5 * i.count('0' + str(color)*2+'0'+str(color)+'0') #011010
            temp_b += 3 * g_temp_b * i.count('0' + str(color) * 4 + '0') #011110
            temp_b += 3 * g_temp_c * i.count('0' + str(color) * 3 + '0') #01110
            temp_a += g_temp_c * i.count('0' + str(next_color) * 3 + '0') #01110
            temp_b += 3 * g_temp_d * i.count('0' + str(color) * 2 + '0') #0110
            temp_b += 3 * g_temp_e * i.count('0' + str(color) * 1 + '0') #010
            temp_a += g_temp_d * i.count('0' + str(next_color) * 2 + '0') #0110
            temp_a += g_temp_e * i.count('0' + str(next_color) * 1 + '0')  #010
            temp_b += 13 * g_temp_f * (i.count(str(next_color) + str(color) * 4 + '0') + i.count('0' + str(color) * 4 + str(next_color)))
            temp_a += g_temp_f * (i.count(str(color) + str(next_color) * 4 + '0') + i.count('0' + str(next_color) * 4 + str(color)))
            temp_a += g_temp_g * (i.count(str(color) + str(next_color) * 3 + '0') + i.count('0' + str(next_color) * 3 + str(color)))
            temp_b += 3 * g_temp_g * (i.count(str(next_color) + str(color) * 3 + '0') + i.count('0' + str(color) * 3 + str(next_color)))
            temp_b += 3 * g_temp_h * (i.count(str(next_color) + str(color) * 2 + '0') + i.count('0' + str(color) * 2 + str(next_color)))    
            temp_a += g_temp_h * (i.count(str(color) + str(next_color) * 2 + '0') + i.count('0' + str(next_color) * 2 + str(color)))
  
        return temp_b - temp_a


    # Minimax
    def computer_search_deep(self,color,next_color,depth):
        if(depth<=0):
            score = self.computer_calc(color,next_color)
            return score
        score = self.computer_calc(color,next_color)
        if(abs(score) >= g_temp_a):
            return score
        temp_s_c = -10000
        steps = self.next_postions()
        _move_well = steps[0]
        for row,column in steps:
            self._chess_board[row][column] = color
            score = -self.computer_search_deep(next_color,color,depth-1)
            self._chess_board[row][column] = 0
            if(score > temp_s_c):
                temp_s_c = score
                _move_well = (row,column)

        if(depth == self.depth):
            self._move_well = _move_well

        return temp_s_c


    def _calc_good_postion(self):
        temp_s_c = self.computer_search_deep(1,2,self.depth)
        return self._move_well
    
    # Convertir la matrice en tableau 1D de string pour faciliter son exploitation
    def board_to_str(self):
        b_s = ''
        for row in self._chess_board:
            for column in row:
                b_s += str(column)
        str_board = []
        lg = len(b_s)
        i = 0
        while(i<g_cols*g_rows):
            str_board.append(b_s[i:i+g_cols])
            i = i+g_cols
        i = 1
        while(i<g_cols):
            str_board.append(b_s[i:lg:g_cols])
            i += 1
        i = 4
        while(i<g_cols):
            str_board.append(b_s[i:i*g_cols+1:g_cols-1])
            i += 1
        i = 1
        while(i<g_rows-4):
            str_board.append(b_s[(i+1)*g_cols-1:lg:g_cols-1])
            i += 1
        i = 0
        while(i<g_cols-4):
            str_board.append(b_s[i:(g_rows-i)*g_cols:g_cols+1])
            i += 1
        i = 1
        while(i<g_rows-4):
            str_board.append(b_s[i*g_cols:lg:g_cols+1])
            i += 1

        return str_board

# Cette classe gère l'affichage de la matrice et le nombre de pions alignés
class board_chess:
    def __init__(self):
        # Initialisation de la matrice 15*15
        self._chess_board = [[0 for i in range(g_rows)] for j in range(g_cols)]
        if(computer_ == 1): # L'IA commence à jouer en 1er
            self._chess_board[7][7] = computer_
    
    # Cette fonction affiche la matrice à chaque tour avec les differents pions
    def t_ui_print(self):
        b = 0
        if (computer_ == 1):
            tag = ['-', '0', 'X'] # joueur / IA pions
        else:
            tag = ['-', 'X', '0']
        a = '  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15\n' # header des colonnes
        row = []
        indx = 0
        while indx < len(self._chess_board): # Nom des lignes de A à N
            row = self._chess_board[indx]
            line = '  '.join([tag[n] for n in row])
            a += chr(ord('A')+b)+' '+line+'\n'
            indx += 1
            b += 1
        return a

    # Cette fonction vérifie si 5 pions sont alignés
    def judge_over(self,color):
        dirs = ((0,1),(1,-1),(1,0),(1,1)) # directions
        i = 0
        while i < g_cols: # on parcours toute la matrice pour verifier
            j = 0
            while j < g_cols:
                if(self._chess_board[i][j] != color):
                    j += 1
                    continue
                indxdir = 0
                while indxdir < len(dirs):
                    dir = dirs[indxdir]
                    flag = True
                    xrow = i
                    xcol = j
                    count = 0 # nombre de pions alligné
                    while count < 4: # tant que moins de 5 on continue 
                        xrow += dir[0]
                        xcol += dir[1]
                        if(not (xrow>=0 and xrow< 15 and xcol>=0 and xcol<15)):#
                            flag = False
                            break
                        if(self._chess_board[xrow][xcol] != color):
                            flag = False
                            break
                        count += 1
                    if(flag == True):
                        return True
                    indxdir += 1
                j += 1
            i += 1
        return False

if __name__ == "__main__":
    
    print()
    print("Qui commence ?", end="")
    uinput  = input("0 = IA | X = Joueur ")
    
    if(uinput == "0"):
        computer_ = 1
        player_ = 2
    else:
        computer_ = 2 
        player_ = 1   
    
    custom_main()