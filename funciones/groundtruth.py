import xml.etree.ElementTree as ET
import os

def XML2Table(xml_data):
    tree = ET.parse(xml_data)#Leer  arbol xml
    tmp1,tmp2=[],[] #listas temporales
    for node  in tree.iter("marking"): #Vamos  iterar sobre todos los  marcadores
        lesionLocal=["",[],[],[],[],"",""]#Para cada marcador vamos a buscar los elementos
        for  subchild01 in node.getchildren():
            #Iterando en la primera Capa
            if subchild01.tag == "polygonregion" or subchild01.tag == "circleregion":
                lesionLocal[0]=str(subchild01.tag) #agregamos el tipo de lesion
                coordsPoly=[] #crear lista para  coordenadas de poligono
                #Iterando en  la segunda Capa para polygonregion
                for subchild02 in subchild01:
                    if subchild01.tag == "polygonregion" and subchild02.tag == "coords2d":
                        #obtenemos  coordenadas iterando para poligono
                        coordsPoly.append(([int(i) for i in ((subchild02.text).split(","))])[:])
                    #Iterando en  la segunda Capa para circleregion
                    if subchild01.tag == "circleregion" :
                        if subchild02.tag == "radius":
                            #Agregamos el radio
                            lesionLocal[2]= int(subchild02.text)
                        if subchild02.tag == "centroid":
                            #agregamos las coordenadas del centro
                            lesionLocal[1]=([ int(i) for i in (subchild02[0].text).split(",")])[:]
                if subchild01.tag == "polygonregion":
                    #Agregamos las coordenadas del  poligo a  la observacion local
                    lesionLocal[3]=coordsPoly[:]
            if subchild01.tag == "representativepoint" :#Agregamos el punto representativo
                lesionLocal[4]=([int(i) for i in  (subchild01[0].text).split(",")  ])[:]
            if subchild01.tag == "confidencelevel" : #Agregamos  el  nivel de confianza
                lesionLocal[5]=(subchild01.text)
            if subchild01.tag == "markingtype" :  #Agregamos  el tipo de marcador
                lesionLocal[6]=(subchild01.text)
        if lesionLocal[6] == 'Red_small_dots':
            tmp1.append(lesionLocal)
        if lesionLocal[6] == 'Haemorrhages':
            tmp2.append(lesionLocal)
    ImageObservation=tmp1[:]+tmp2[:]
    return ImageObservation

def TablaDeLesiones(file):
    f_in_list=[f for f in os.listdir("GroundTruth") if ".xml" in f]
    f_in_list.sort()
    table=[]
    for xml_file in f_in_list:
        table+=XML2Table(xml_file)[:]
    return table
