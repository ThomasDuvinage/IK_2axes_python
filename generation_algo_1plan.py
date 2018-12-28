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

print("THIS PROGRAM ONLY GIVE YOU THE ANSWER FOR A PLANAR ROBOT")

liaisons = int(input("How many liaisons do you have ? "))

def generation_var(liaisons):
    arm_lenght = []
    dictvariables = {}
    function_table = []
    angle_table = []
    for lenght in range(0, liaisons):
        size = float(input("What the length of the "+str(lenght)+" arm ? "))
        arm_lenght.append(size)
        dictvariables["theta"+str(lenght)] = dynamicsymbols("theta"+str(lenght))
        dictvariables["l"+str(lenght)] = size
        function_table.append(dictvariables["theta"+str(lenght)])
        function_table.append(dictvariables["l"+str(lenght)])
        angle_table.append(dictvariables["theta"+str(lenght)])
        print("ANGLE_TABLE= ",angle_table)
    
    dictvariables["a"] = dynamicsymbols("a")
    dictvariables["d"] = dynamicsymbols("d")
    dictvariables["theta"] = dynamicsymbols("theta")
    dictvariables["alpha"] = dynamicsymbols("alpha")

    print(dictvariables)

    generation_matrix(dictvariables,liaisons, angle_table)
    angle_limits(liaisons,dictvariables,angle_table)

def generation_matrix(dictvariables,liaisons, angle_table):
    rot = sp.Matrix([[sp.cos(dictvariables["theta"]), -sp.sin(dictvariables["theta"])*sp.cos(dictvariables["alpha"]), sp.sin(dictvariables["theta"])*sp.sin(dictvariables["alpha"])],
                    [sp.sin(dictvariables["theta"]), sp.cos(dictvariables["theta"])*sp.cos(dictvariables["alpha"]), -sp.cos(dictvariables["theta"])*sp.sin(dictvariables["alpha"])],
                    [0, sp.sin(dictvariables["alpha"]), sp.cos(dictvariables["alpha"])]])

    trans = sp.Matrix([dictvariables["a"]*sp.cos(dictvariables["theta"]),dictvariables["a"]*sp.sin(dictvariables["theta"]),dictvariables["d"]])

    last_row = sp.Matrix([[0, 0, 0, 1]])

    m = sp.Matrix.vstack(sp.Matrix.hstack(rot, trans), last_row)
    #print(m)

    matrix_table = []
    for matrix in range(0, liaisons):
        matrix_table.append(m.subs({dictvariables["alpha"]:0, dictvariables["a"]:dictvariables["l"+str(matrix)], dictvariables["theta"]:dictvariables["theta"+str(matrix)], dictvariables["d"]:0}))
        print(matrix_table)

    m02 = 1
    for k in range(0,len(matrix_table)):
        m02 = m02 * matrix_table[k]
    
    print(m02)

    mbee= sp.Matrix([[m02[0,0].simplify(), m02[0,1].simplify(), sp.trigsimp(m02[0,3].simplify())],
                    [m02[1,0].simplify(), m02[1,1].simplify(), sp.trigsimp(m02[1,3].simplify())],
                    [m02[2,0].simplify(), m02[2,1].simplify(), m02[2,2].simplify()]])

    #print(mbee)

    px = mbee[0,2] #les deux lignes qui suivent permettent d'afficher les equations qui regissent le systeme en x et en y
    print("PX= ",px)

    py = mbee[1,2] 
    print("PY= ",py)

    fx = sp.lambdify(angle_table, px, 'numpy')
    fy = sp.lambdify(angle_table, py, 'numpy')

def angle_limits(liaisons,dictvariables,angle_table):
    limits = []#this array contains of the angle possibilites with angle limits
    n = 10 #if you want to increase the precision of your robot you will need to change this variable
    for angle in range(0, liaisons):
        limit_max = float(input("angle limit max = "))
        limit_min = float(input("angle limit min = "))
        limits.append(np.linspace(d2r(limit_min), d2r(limit_max), num=n))
        dictvariables["theta"+str(angle)] = np.linspace(d2r(limit_min), d2r(limit_max), num=n)
        angle_table[angle] = dictvariables["theta"+str(angle)]
    
    # print("limits_array= ", limits)
    # print("ANGLE_TABLE= ",angle_table)
    # print("dict= ",dictvariables)


#This function permit to generate all the robot possitions
def all_positions(limits,liaisons,dictvariables, px, py,n, fx, fy,angle_table):
    matrix_angle_pos = [[],[]]
    
    #we create a csv table / if it all ready exist in your folder it will write on it 
    #That alowed us to not recalculate all the possitons eah time 

    for k in range(liaisons,0):
        for i in range(0,n):
            angle_table[liaisons] = limits[liaisons][i]
        


    with open('matrices_generale.csv', mode='w') as matrice_file:
        matrice_writer = csv.writer(matrice_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    work_space_x.append(round(fx(120.0, 130.0, limits[o][i], theta2s[n]),1))
                    work_space_y.append(round(fy(120.0, 130.0, theta1s[i], theta2s[n]),1))
                    matrix_angle_pos.append([round(fx(120.0, 130.0, theta1s[i], theta2s[n]),1),round(fy(120.0, 130.0, theta1s[i], theta2s[n]),1), theta1s[i],theta2s[n]])
                        
                    #on enregistre l'equivalent de matrix_angle_pos dans le tableau csv
                    matrice_writer.writerow([round(fx(120.0, 130.0, theta1s[i], theta2s[n]),1),round(fy(120.0, 130.0, theta1s[i], theta2s[n]),1), theta1s[i],theta2s[n]])

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
    
    # plt.scatter(work_space_x,work_space_y,s=5)
    # plt.title('Toutes les positions que la pointe peut prendre')
    # plt.xlabel('work_space_x')
    # plt.ylabel('work_space_y')
    # plt.show()
    
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
    
    
#all_positions(theta1s, theta2s, fx, fy)

#lecture_csv(50, 200 , 0.1, fx ,fy)

generation_var(liaisons)