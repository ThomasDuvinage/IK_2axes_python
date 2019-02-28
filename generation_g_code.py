#on import ce code pour la fonction de lecture_csv
from denavit_et_trajctoire import *

import csv

def gcode_generation(seuil):
    with open('points_passage.csv') as passage_file:#je vais lire le fichier de points de passage en csv 
            passage_reader = csv.reader(passage_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            with open('G_CODE_ROBOT.gcode', mode='w') as gc_file:#je creer le g-code tout en lisant le passage de points
                gc_writer = csv.writer(gc_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            
                for passage_row in passage_reader:
                    #lecture_csv(passage_row[0],passage_row[1] , 1, fx ,fy)
                    if(lecture_csv_T1(passage_row[0], passage_row[1] , seuil, fx ,fy) == "IMPOSSIBLE" or lecture_csv_T2(passage_row[0], passage_row[1] , seuil, fx ,fy) == "IMPOSSIBLE"):
                        gc_writer.writerow(["IMPOSSIBLE","IMPOSSIBLE"])
                    else:
                        gc_writer.writerow([lecture_csv_T1(passage_row[0], passage_row[1] , seuil, fx ,fy),lecture_csv_T2(passage_row[0], passage_row[1] , seuil , fx ,fy)])
                        print(passage_row[0], passage_row[1]) 

gcode_generation(5)