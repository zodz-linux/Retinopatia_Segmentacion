def MomentosGeometricos(imagen,file_xml,size=60):
    print "\t\t*Funcion: Momentos Geometricos ..."
    img= cv2.imread(outPath+imagen) # Cargar Imagen
    img=img[:,:,1] # Tomar la Capa Verde
    GroundTruth=XML2Table(file_xml)
    counter=0
    size=size/2
    attributes=[]
    for lesion in GroundTruth:
        centerX,centerY=lesion[4][0],lesion[4][1] #tomamos como centro el punto representativo
        subimage=img[(centerX-size):(centerX+size),(centerY-size):(centerY+size)]
        temporal=[[centerX,centerY]]
        if subimage.shape == (0, 40) : continue
        if subimage.shape == (40, 0) : continue
        aux=cv2.HuMoments(cv2.moments(subimage))
        temporal.append(aux)
        cv2.imwrite(outPathLesion+file_xml[-25:-4]+"_Lesion_"+str(counter)+".png",subimage)
        counter+=1
        attributes.append(temporal)
    print "Numero de  lesiones: ",counter
    return  attributes

