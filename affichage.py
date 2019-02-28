#####################
##  Le but de ce code est de generer les equations de tajectoire que le robot doit effectuer 
##  pour ce rendre en un point le plus rapidement possible 
#####################

from sympy.abc import x
from sympy.utilities.lambdify import lambdify, implemented_function
from sympy import Function

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import pylab

import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go

import csv

import time 

from math import *

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



def trajectoire_et_obstacles():
    #Apres cela nous allons demander la taille de chaque objet et leur positon 
    #Nous allons creer deux tableaux un pour les dimensions et l'autre pour les positions 
    # taille_array = [[30,30,10],[60,60,20],[20,40,20]]
    # position_array = [[20,20,0],[30,30,0],[10,30,0]]

    #Dans un premier temps nous allons demander le nombre d'obstacle 
    nb_obstacle = int(input("How many obstacles are there ? "))
    #nb_obstacle = 3

    def calul_trajectoire(GX,GY,nb_obstacle):

        #array pour les points de passage du robot 
        points = []
        #securite correspond a la marge de passage entre l'objet et la pointe 
        securite = 3

        iteration = 0#permet de compter le nombre de ligne

        #on defini les arrays de passage
        passage_x = []
        passage_y = []
        passage_z = []

        with open('tableau-obstacle.csv') as obstacles_file:
            csv_reader = csv.reader(obstacles_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            for osbstacles_row in csv_reader:
    
                if(iteration == 0):#la premiere ligne du fichier csv correpond a la position initiale du robot 
                    passage_x = [osbstacles_row[3]]
                    passage_y = [osbstacles_row[4]]
                    #la ligne suivante n'est pas encore utilisee 
                    #passage_z = [osbstacles_row[5]]
                    iteration += 1

                else:
                    c = 'r'#cette ligne correspond a la couleur
                    m = 's'#cette ligne correspond a la taille de l'obstacle

                    #la premiere ligne permet d'aficher les points dans le repere 
                    #dans cette ligne il faut voir pour prendre en compte la hauteur de l'obstacle dans le s=....
                    ax.scatter(osbstacles_row[3], osbstacles_row[4], osbstacles_row[5] , zdir='z', s=[osbstacles_row[0],osbstacles_row[1]], c=c, depthshade=True,marker=m)
                    #points correspond aux points que le robot va emprunter
                    #cela permet de faire une interpolation 
                    points.append([osbstacles_row[3],osbstacles_row[4]+((osbstacles_row[2])/2) + securite,osbstacles_row[5]])

        for o in range(0,nb_obstacle):
            #dans les deux lignes qui suivent on isole les possitions en x et en y 
            passage_x.append(points[o][0])
            passage_y.append(points[o][1])

        passage_x.append(GX)
        passage_y.append(GY)

        #si la trajectoire n'est pas asssez precise il faut que vous augmentiez le degres de fit
        if(nb_obstacle == 0):
            fit_degres = 1
        else:
            fit_degres = nb_obstacle

        # on calcul l'equation 
        z = np.polyfit(passage_x, passage_y, fit_degres)
        f = np.poly1d(z)

        print('la fonction est =')
        print(f)

        #nous allons definir l'ensemble de variation de toutes les valeurs en x et en y
        point_x_new = np.linspace(passage_x[0], GX, 100)
        point_y_new = f(point_x_new)

        with open('points_passage.csv', mode='w') as passage_file:
                passage_writer = csv.writer(passage_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                
                for nb_passage in range(0,len(point_x_new)):
                    passage_writer.writerow([point_x_new[nb_passage],point_y_new[nb_passage]])


        #ici nous enregistrons un fichier csv avec toutes les positions que va prendre le robot
        with open('trajectory-points.csv', mode='w') as points_file:
                points_writer = csv.writer(points_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

                for j in range(0, len(point_x_new)):
                    points_writer.writerow([point_x_new[j],point_y_new[j]])
        
        #on affiche sur le repere les differents points
        plt.plot(point_x_new,point_y_new,'o')

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        if(GX < GY):
            ax.set_xlim(0, GY)
            ax.set_ylim(GY, 0)
            ax.set_zlim(0, GY)
        else:
            ax.set_xlim(0, GX)
            ax.set_ylim(GX, 0)
            ax.set_zlim(0, GX)

        plt.show()

    def enregistrement_csv(nb_obstacle):
        #dans un premier temps nous allons faire une demande de creation d'obstacle...
        demande_changement = int(input("Do you want to create or change csv file about obstacles ? (0/1) "))

        #si validation alors on creer le fichier
        if(demande_changement == 1):
            print('Le fichier csv existe deja vous allez reecrire dessus.')
            print('ATTENTION !! TOUTES LES VALEURS VONT ETRE SUPRIMEES...')
            print('ctrl-c to quit')
            time.sleep(10)#on attend pendant 30 secondes
            print('Creation du fichier csv..............')
                

            with open('tableau-obstacle.csv', mode='w') as obstacles_file:
                obstacle_writer = csv.writer(obstacles_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

                #nous allons demander la possition du robot au debut du mouvement
                debut_x = float(input("Position en x au debut = "))
                debut_y = float(input("Position en y au debut = "))
                debut_z = float(input("Position en z au debut = "))

                obstacle_writer.writerow([0,0,0,debut_x,debut_y,debut_z])

                #Si vous voulez faire pour n obstacle decommenter ce bloc 
                for n in range(0,nb_obstacle):
                    longueur = float(input("Longueur de l'obstacle n"+str(n)+" ? "))
                    largeur  = float(input("Largeur de l'obstacle n"+str(n)+" ? "))
                    #hauteur  = int(input("Hauteur de l'obstacle n",str(n)," ? "))
                    hauteur = 0 #pour prendre en compte la hauteur nous devons trouver un systeme pour l'affichage dans le repere des obstacles

                    #on fait de meme avec les positions 
                    p_x  = float(input("Position en x de l'obstacle n"+str(n)+" ? "))
                    p_y  = float(input("Position en y de l'obstacle n"+str(n)+" ? "))
                    #p_z  = float(input("Position en z de l'obstacle n",str(n)," ? "))
                    p_z = 0 #cette ligne devra etre commentee pour une demande dans un repere xyz

                    #on insere desormais dans le tableau csv
                    obstacle_writer.writerow([longueur,largeur,hauteur,p_x,p_y,p_z])

        else:#si la personne ne veut pas creer d'obstacles alors on passe
            pass


############### La fonction qui suit permet de faire les caluls de trajectoire pour une fonction donnee 
def creation_funtion():
    fonction = str(input("Enter the function you want = "))
    f = implemented_function('f', lambda x: eval(fonction))
    lam_f = lambdify(x, f(x))

    min_value = input("Debut de l'interval = ")
    max_value = input("Fin de l'interval = ")

    #dans la partie qui va suivre, nous allons faire les calculs de la trajectoire

    with open('points_passage.csv', mode='w') as passage_file:
            passage_writer = csv.writer(passage_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            for X in range(min_value,max_value+1):
                passage_writer.writerow([X,lam_f(X)])


trajectoire_et_obstacles()
creation_funtion()
#enregistrement_csv(nb_obstacle)
#calul_trajectoire(50,200,nb_obstacle)
