#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 18:00:52 2018

@author: thomasduvinage
"""

from statistics import mean

import sympy as sp

from sympy.physics.vector import init_vprinting
init_vprinting(use_latex='mathjax', pretty_print=False)

from sympy.physics.mechanics import dynamicsymbols

import matplotlib.pyplot as plt  


import numpy as np
d2r = np.deg2rad 

import csv

import sys

def ask_parameters():
    liaisons = int(input("Number of liaisons in your system = "))
    print("POUR LES PARAMETRES QUI VONT SUIVRE VEUILLEZ REMPLIR AVEC 1(OUI) ou 0(NON)")
    for n in range(1, liaisons+1):
        print("Degrés de libertés pour la liaison " + str(n))

        Rx = int(input("Rotation en x = "))
        Ry = int(input("Rotation en y = "))
        Rz = int(input("Rotation en z = "))
        Tx = int(input("Translation en x = "))
        Ty = int(input("Translation en y = "))
        Tz = int(input("Translation en z = "))

        R_matrix = [Rx, Ry, Rz]
        T_matrix = [Tx,Ty,Tz]

        if n == 1:
            matrix_degres_liberte = [R_matrix,T_matrix]

        else:
            matrix_degres_liberte.append(R_matrix)
            matrix_degres_liberte.append(T_matrix)

    print("Matrix degrees of liberty", matrix_degres_liberte)

    print("You all ready need to give the size of each arm(s)")

    longueur_matrix = []

    for k in range(1, liaisons + 1):
        longueur = int(input("Longueur du bras " + str(k) + " = "))

        longueur_matrix.append(longueur)

    print(longueur_matrix)

    return liaisons, longueur_matrix, matrix_degres_liberte

def variable_generation(matrix_degres_liberte,longueur_matrix, liaisons):#Dans cette partie il reste a prendre en compte les translations
    #nous allons lire la matrice de degrees de liberte 
    #for degres in range(0,)
    variabledict = {}#on creer un dictionnaire pour pouvoir gerer le nomd des varibles en dynamique 
    for degres in range (0,liaisons+1):
        for check in  range(0,2):#je met 2 car il y a 3 possibilite pour chaque liaison
            if(matrix_degres_liberte[degres][check] == 1):
                #pour la rotation
                if (check == 0 and degres%2 == 0):
                    variabledict["phi"+ str(degres)] = dynamicsymbols("phi"+ str(degres))
                if (check == 1 and degres%2 == 0 ):
                    variabledict["alpha"+ str(degres)] = dynamicsymbols("aplha"+ str(degres))
                if (check == 2 and degres%2 == 0):
                    variabledict["theta"+ str(degres)] = dynamicsymbols("theta"+ str(degres))

                #pour la translation
                if (check == 0 and degres%2 != 0):
                    variabledict["Tx"+ str(degres)] = dynamicsymbols("Tx"+ str(degres))
                if (check == 1 and degres%2 != 0 ):
                    variabledict["Ty"+ str(degres)] = dynamicsymbols("Ty"+ str(degres))
                if (check == 2 and degres%2 != 0):
                    variabledict["Tz"+ str(degres)] = dynamicsymbols("Tz"+ str(degres))


        variabledict["l"+str(degres)] = longueur_matrix[0]

    variabledict["a"] = dynamicsymbols("a")
    variabledict["d"] = dynamicsymbols("d")
    variabledict["theta"]=dynamicsymbols("theta")
    variabledict["alpha"]=dynamicsymbols("alpha")

    print(variabledict)

    #theta1, theta2, l1, l2, theta, alpha, a, d = dynamicsymbols('theta1 theta2 l1 l2 theta alpha a d')
    #print(theta1, theta2, l1, l2, theta, alpha, a, d) 

#les entrees ne seront pas a changer dans le code final, il faudra juste appeller la fonction 
def caculus_matrix(liaisons, longueur_matrix, matrix_degres_liberte, variabledict):    
    def rot_matrix_z(longueur_matrix):
        rot = sp.Matrix([[sp.cos(variabledict["theta"]), -sp.sin(variabledict["theta"])*sp.cos(variabledict["alpha"]), sp.sin(variabledict["theta"])*sp.sin(variabledict["alpha"])],
                 [sp.sin(variabledict["theta"]), sp.cos(variabledict["theta"])*sp.cos(variabledict["alpha"]), -sp.cos(variabledict["theta"])*sp.sin(variabledict["alpha"])],
                 [0, sp.sin(variabledict["alpha"]), sp.cos(variabledict["alpha"])]])

        trans = sp.Matrix([variabledict["a"]*sp.cos(variabledict["theta"]),variabledict["a"]*sp.sin(variabledict["theta"]),variabledict["d"]])

        last_row = sp.Matrix([[0, 0, 0, 1]])

        m = sp.Matrix.vstack(sp.Matrix.hstack(rot, trans), last_row)
        #print(m)
        matrice_z = []
        for rotY in range(0,liaisons-1):
            for degres in range (0,liaisons+1):
                for check in  range(0,2):#je met 2 car il y a 3 possibilite pour chaque liaison
                    if(matrix_degres_liberte[degres][check] == 1):
                        if (check == 2 and degres%2 == 0):
                            m = m.subs({ variabledict["alpha"]:0, variabledict["a"]:longueur_matrix[rotY],  variabledict["theta"]:variabledict["theta"+ str(degres)], d:0})
                            matrice_z.append(m)

        m02 = np.prod(matrice_z)
        #print(m02)

        mbee= sp.Matrix([[m02[0,0].simplify(), m02[0,1].simplify(), sp.trigsimp(m02[0,3].simplify())],
                        [m02[1,0].simplify(), m02[1,1].simplify(), sp.trigsimp(m02[1,3].simplify())],
                        [m02[2,0].simplify(), m02[2,1].simplify(), m02[2,2].simplify()]])

        #print(mbee)

        px = mbee[0,2]
        #print(px)

        py = mbee[1,2]
        #print(py)

    fx = sp.lambdify((l1, l2, theta1, theta2), px, 'numpy')
    fy = sp.lambdify((l1, l2, theta1, theta2), py, 'numpy')

    theta1s = np.linspace(d2r(0), d2r(90), num=1000) # desired range of motion for joint 1
    theta2s = np.linspace(d2r(-90), d2r(90), num=1000) # desired range of motion for joint 2




#la fonction qui suit va chercher dans le tableau de valeur si les demandes en X et Y correspondent à une 
def ask_position(GX, GY, nbs_val_matrix, matrix_angle_pos,  fx, fy, seuil):
    matrix_reponse_t1 = []
    matrix_reponse_t2 = []
    for k in range(0 , nbs_val_matrix-1):
        if(GX-seuil <= matrix_angle_pos[k][0] <= GX+seuil and  GY-seuil <= matrix_angle_pos[k][1] <= GY+seuil):
            #print("l'angle theta1 est de : " , matrix_angle_pos[k][2])
            #print("l'angle theta2 est de : ", matrix_angle_pos[k][3])
            
            matrix_reponse_t1.append(matrix_angle_pos[k][2])
            matrix_reponse_t2.append(matrix_angle_pos[k][3])
            
    print("Theta1 moyen: ",mean(matrix_reponse_t1))
    print("Theta2 moyen: ",mean(matrix_reponse_t2))
    
    print("possition en x =",fx(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))
    print("possition en y =",fy(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))
    
    ecart_x = ((GX - fx(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))/GX)*100
    ecart_y = ((GY - fy(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))/GY)*100
    
    print("Ecart en x = ", ecart_x)
    print("Ecart en y = ", ecart_y)
            
#la fonction suivante permet de definir l'ensemble des positions que peut avoir le robot 
def all_positions(theta1s, theta2s, fx, fy):
    work_space_x = []
    work_space_y = []
    
    matrix_angle_pos = []
    
    if(len(theta1s) == len(theta2s)):
        #on creer un tableau csv 
        #cela va nous permettre de ne pas recaler à chaque fois 
        with open('matrices_generale.csv', mode='w') as matrice_file:
            matrice_writer = csv.writer(matrice_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, len(theta1s)-1):
                for n in range(0, len(theta2s)-1):
                    work_space_x.append(round(fx(120.0, 130.0, theta1s[i], theta2s[n]),1))
                    work_space_y.append(round(fy(120.0, 130.0, theta1s[i], theta2s[n]),1))
                    matrix_angle_pos.append([round(fx(120.0, 130.0, theta1s[i], theta2s[n]),1),round(fy(120.0, 130.0, theta1s[i], theta2s[n]),1), theta1s[i],theta2s[n]])
                    
                    #on enregistre l'equivalent de matrix_angle_pos dans le tableau csv
                    matrice_writer.writerow([round(fx(120.0, 130.0, theta1s[i], theta2s[n]),1),round(fy(120.0, 130.0, theta1s[i], theta2s[n]),1), theta1s[i],theta2s[n]])
    
##Les lignes suivantes permettent d'afficher l'ensemble des matrices 
#    print("WORK_SPACE_X")
#    print(work_space_x)
#    print("WORK_SPACE_Y")
#    print(work_space_y)
#    
#    print("MATRIX_ANGLE_POS")
#    print(matrix_angle_pos)
    
#    #nbs_val_matrix correspond au nombre de ligne dans la matrice 
    nbs_val_matrix = len(matrix_angle_pos)
#    print(nbs_val_matrix)
    
    plt.scatter(work_space_x,work_space_y,s=5)
    plt.title('Toutes les positions que la pointe peut prendre')
    plt.xlabel('work_space_x')
    plt.ylabel('work_space_y')
    plt.show()
    
    ask_position(50, 200, nbs_val_matrix, matrix_angle_pos,fx,fy,0.1)
    
def lecture_csv(GX, GY , seuil , fx ,fy):
    matrix_reponse_t1 = []
    matrix_reponse_t2 = []
    with open('matrices_generale.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

        for row in csv_reader:
            if(GX-seuil <= row[0] <= GX+seuil and  GY-seuil <= row[1] <= GY+seuil):
                
                matrix_reponse_t1.append(row[2])
                matrix_reponse_t2.append(row[3])
            
    print("Theta1 moyen: ",mean(matrix_reponse_t1))
    print("Theta2 moyen: ",mean(matrix_reponse_t2))
    
    print("possition en x =",fx(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))
    print("possition en y =",fy(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))
    
    ecart_x = ((GX - fx(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))/GX)*100
    ecart_y = ((GY - fy(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))/GY)*100
    
    print("Ecart en x = ", ecart_x,"%")
    print("Ecart en y = ", ecart_y,"%")
    
    