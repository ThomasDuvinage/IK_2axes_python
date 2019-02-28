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

##cette partie correspond au lib du calcul de trajectoires
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pylab

import plotly.plotly as py
import plotly.graph_objs as go

theta1, theta2, l1, l2, theta, alpha, a, d = dynamicsymbols('theta1 theta2 l1 l2 theta alpha a d')
#print(theta1, theta2, l1, l2, theta, alpha, a, d) 

rot = sp.Matrix([[sp.cos(theta), -sp.sin(theta)*sp.cos(alpha), sp.sin(theta)*sp.sin(alpha)],
                 [sp.sin(theta), sp.cos(theta)*sp.cos(alpha), -sp.cos(theta)*sp.sin(alpha)],
                 [0, sp.sin(alpha), sp.cos(alpha)]])

trans = sp.Matrix([a*sp.cos(theta),a*sp.sin(theta),d])

last_row = sp.Matrix([[0, 0, 0, 1]])

m = sp.Matrix.vstack(sp.Matrix.hstack(rot, trans), last_row)
#print(m)

m01 = m.subs({alpha:0, a:l1, theta:theta1, d:0})
#print(m01)

m12 = m.subs({alpha:0, a:l2, theta:theta2, d:0})
#print(m12)

m02 = (m01*m12)
#print(m02)

mbee= sp.Matrix([[m02[0,0].simplify(), m02[0,1].simplify(), sp.trigsimp(m02[0,3].simplify())],
                 [m02[1,0].simplify(), m02[1,1].simplify(), sp.trigsimp(m02[1,3].simplify())],
                 [m02[2,0].simplify(), m02[2,1].simplify(), m02[2,2].simplify()]])

#print(mbee)

px = mbee[0,2]
#print(px)

py = mbee[1,2]
#print(py)

fx = sp.lambdify([l1, l2, theta1, theta2], px, 'numpy')
fy = sp.lambdify([l1, l2, theta1, theta2], py, 'numpy')

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
    
    ask_position(50, 200, nbs_val_matrix, matrix_angle_pos,fx,fy,0.1)


############################Affichage de l'ensemble des positions que peut prendre le robot 
def affichage_possitions():
    work_space_x = []
    work_space_y = []

    with open('matrices_generale.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            work_space_x.append(row[0])
            work_space_y.append(row[1])

    plt.scatter(work_space_x,work_space_y,s=5)
    plt.title('Toutes les positions que la pointe peut prendre')
    plt.xlabel('work_space_x')
    plt.ylabel('work_space_y')
    plt.show()


##############################  Calcul de trajectoire
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#Apres cela nous allons demander la taille de chaque objet et leur positon 
#Nous allons creer deux tableaux un pour les dimensions et l'autre pour les positions 
# taille_array = [[30,30,10],[60,60,20],[20,40,20]]
# position_array = [[20,20,0],[30,30,0],[10,30,0]]

def calul_trajectoire(GX,GY):
    #Dans un premier temps nous allons demander le nombre d'obstacle 
    nb_obstacle = int(input("How many obstacles are there ? "))
    #nb_obstacle = 3

    #Apres cela nous allons demander la taille de chaque objet et leur positon 
    #Nous allons creer deux tableaux un pour les dimensions et l'autre pour les positions 
    taille_array = []
    position_array = []

    #Si vous voulez faire pour n obstacle decommenter ce bloc 
    for n in range(0,nb_obstacle):
        longueur = int(input("Longueur de l'obstacle n",str(n)," ? "))
        largeur  = int(input("Largeur de l'obstacle n",str(n)," ? "))
        #hauteur  = int(input("Hauteur de l'obstacle n",str(n)," ? "))
        #on insert les valeurs dans l'array taille
        taille_array.append([longueur,largeur])

        #on fait de meme avec les positions 
        p_x  = int(input("Position en x de l'obstacle n",str(n)," ? "))
        p_y  = int(input("Position en y de l'obstacle n",str(n)," ? "))
        #p_z  = int(input("Position en z de l'obstacle n",str(n)," ? "))
        position_array.append([p_x,p_y])
    

    #array pour les points de passage du robot 
    points = []
    #securite correspond a la marge de passage entre l'objet et la pointe 
    securite = 3

    #cette boucle permet l'affichage de tous les obstacles
    for k in range(0,nb_obstacle):
        c = 'r'
        m = 's'
        ax.scatter(position_array[k][0], position_array[k][1], position_array[k][2] , zdir='z', s=[taille_array[k][0],taille_array[k][1]], c=c, depthshade=True,marker=m)
        #nous allons desormais generer les points de passage du robot 
        #pour cela nous allons allons garder le meme x mais modifier la position en y 
        #en alternant quand l'obstacle est un pair ou impair (%2 -> modulo 2)
        #if(k % 2 == 0):
        points.append((position_array[k][0],position_array[k][1]+((taille_array[k][1])/2) + securite))
        # else:
        #     points.append((position_array[k][0],position_array[k][1]-((taille_array[k][1])/2) - securite))

    #dans les deux lignes qui suivent on isole les possitions en x et en y 
    passage_x = [0]
    passage_y = [0]
    for o in range(0,nb_obstacle):
        passage_x.append(points[o][0])
        passage_y.append(points[o][1])

    passage_x.append(GX)
    passage_y.append(GY)

    #si la trajectoire n'est pas asssez precise il faut que vous augmentiez le degres de fit
    fit_degres = nb_obstacle

    # on calcul l'equation 
    z = np.polyfit(passage_x, passage_y, fit_degres)
    f = np.poly1d(z)

    print('la fonction est =')
    print(f)

    #precison_trajctoire
    precision_trajectoire = 50

    #nous allons definir l'ensemble de variation de toutes les valeurs en x et en y
    point_x_new = np.linspace(passage_x[0], GX, precision_trajectoire)
    point_y_new = f(point_x_new)

    plt.plot(point_x_new,point_y_new,'o')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    ax.set_xlim(0, 100)
    ax.set_ylim(100, 0)
    ax.set_zlim(0, 100)

    plt.show()
    
def lecture_csv_T1(GX, GY , seuil , fx ,fy):
    matrix_reponse_t1 = []
    matrix_reponse_t2 = []

    with open('matrices_generale.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            if(GX-seuil <= row[0] <= GX+seuil and  GY-seuil <= row[1] <= GY+seuil):     
                matrix_reponse_t1.append(row[2])
                matrix_reponse_t2.append(row[3])

    if(len(matrix_reponse_t1) == 1 and len(matrix_reponse_t2) == 1):
        T1_moyen = matrix_reponse_t1[0]
        T2_moyen = matrix_reponse_t2[0]
        #print(T1_moyen)

        return T1_moyen

    elif(len(matrix_reponse_t1) > 1 and len(matrix_reponse_t2) == 1):
        T1_moyen = mean(matrix_reponse_t1)
        T2_moyen = matrix_reponse_t2[0]
        #print(T1_moyen)

        return T1_moyen

    elif(len(matrix_reponse_t1) == 1 and len(matrix_reponse_t2) > 1):
        T1_moyen = matrix_reponse_t1[0]
        T2_moyen = mean(matrix_reponse_t2)
        #print(T1_moyen)

        return T1_moyen
    
    elif(len(matrix_reponse_t1) > 1 and len(matrix_reponse_t2) > 1):
        T1_moyen = mean(matrix_reponse_t1)
        T2_moyen = mean(matrix_reponse_t2)
        #print(T1_moyen)

        return T1_moyen
    
    elif(len(matrix_reponse_t1) ==  0 or len(matrix_reponse_t2) == 0):
        print("Le robot ne peut pas avoir la position souhaitee")
        return('IMPOSSIBLE')
    
    """ print("possition en x =",fx(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))
    print("possition en y =",fy(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))
    
    ecart_x = ((GX - fx(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))/GX)*100
    ecart_y = ((GY - fy(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))/GY)*100
    
    print("Ecart en x = ", ecart_x)
    print("Ecart en y = ", ecart_y) """

def lecture_csv_T2(GX, GY , seuil , fx ,fy):
    matrix_reponse_t1 = []
    matrix_reponse_t2 = []

    with open('matrices_generale.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for row in csv_reader:
            if(GX-seuil <= row[0] <= GX+seuil and  GY-seuil <= row[1] <= GY+seuil):     
                matrix_reponse_t1.append(row[2])
                matrix_reponse_t2.append(row[3])

    if(len(matrix_reponse_t1) == 1 and len(matrix_reponse_t2) == 1):
        T1_moyen = matrix_reponse_t1[0]
        T2_moyen = matrix_reponse_t2[0]
        #print(T2_moyen)

        return(T2_moyen)

    elif(len(matrix_reponse_t1) > 1 and len(matrix_reponse_t2) == 1):
        T1_moyen = mean(matrix_reponse_t1)
        T2_moyen = matrix_reponse_t2[0]
        #print(T2_moyen)

        return(T2_moyen)

    elif(len(matrix_reponse_t1) == 1 and len(matrix_reponse_t2) > 1):
        T1_moyen = matrix_reponse_t1[0]
        T2_moyen = mean(matrix_reponse_t2)
        #print(T2_moyen)

        return(T2_moyen)
    
    elif(len(matrix_reponse_t1) > 1 and len(matrix_reponse_t2) > 1):
        T1_moyen = mean(matrix_reponse_t1)
        T2_moyen = mean(matrix_reponse_t2)
        #print(T2_moyen)

        return(T2_moyen)
    
    elif(len(matrix_reponse_t1) ==  0 or len(matrix_reponse_t2) == 0):
        print("Le robot ne peut pas avoir la position souhaitee")
        return("IMPOSSIBLE")
    
    """ print("possition en x =",fx(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))
    print("possition en y =",fy(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))
    
    ecart_x = ((GX - fx(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))/GX)*100
    ecart_y = ((GY - fy(120.0, 130.0, mean(matrix_reponse_t1), mean(matrix_reponse_t2)))/GY)*100
    
    print("Ecart en x = ", ecart_x)
    print("Ecart en y = ", ecart_y) """

    
#all_positions(theta1s, theta2s, fx, fy)

#lecture_csv(50, 200 , 0.1, fx ,fy)