import numpy as np
d2r = np.deg2rad

from math import cos,sin,sqrt

import csv 

import matplotlib
import matplotlib.pyplot as plt


#Dans la fonction si dessous nous allons lire deux tableaux en meme temps (point_passage et le gcode) pour cela nous faire une projection pour le premier bras dans l'espace 
#puis avec les points de passage nous pourrons relier les deux bouts restants 
# IMPORTANT cette technique ne foncitonne que pour un bras ayant deux bras....

def points_liaisons(longueur_bras1):#cette fonction permet de generer la possition de chaque liaisons dans l'espace
    array_position_liaisons = [[],[]]

    with open('G_CODE_ROBOT.gcode') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for CODE in csv_reader:
            array_position_liaisons[0].append([longueur_bras1 * cos(CODE[0]),longueur_bras1 * sin(CODE[0])])

    with open('points_passage.csv') as csv_file:
        csv_points = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        for points in csv_points:
            array_position_liaisons[1].append([points[0],points[1]])

    #print(array_possition_liaisons)

    def affichage_deplacement(array_position_liaisons):
        fig, ax = plt.subplots()

        for n in range(0,len(array_position_liaisons[0])-1):
            ax.plot(array_position_liaisons[1][n][0],array_position_liaisons[1][n][1],'ro-')
            ax.plot(array_position_liaisons[0][n][0],array_position_liaisons[0][n][1],'bo-')

            print('longueur bras 1 = ',sqrt(pow(array_position_liaisons[0][n][0],2) + pow(array_position_liaisons[0][n][1],2) ))
            print('longueur bras 2 = ',sqrt(pow((array_position_liaisons[1][n][0] - array_position_liaisons[0][n][0]),2) + pow((array_position_liaisons[1][n][1] - array_position_liaisons[0][n][1]),2) ))

        ax.set(xlabel='x', ylabel='y',
            title='Positions liaisons')
        ax.grid()

        plt.show()

    affichage_deplacement(array_position_liaisons)


points_liaisons(120)

