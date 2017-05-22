

import matplotlib.patches as mpatches


    momentosPromedios=[]

    plt.figure()
    momento=[lesion[1][1] for lesion in momentos]
    momentosPromedios.append(np.mean(momento))
    plt.plot(np.log(momento),".")
    plt.title("Momento 2: Promedio: "+str(np.mean(momento)))
    plt.savefig("momento2.png")


    plt.figure()
    momento=[lesion[1][0] for lesion in momentos]
    momentosPromedios.append(np.mean(momento))
    plt.plot(np.log(momento),".")
    plt.title("Momento 1: Promedio: "+str(np.mean(momento)))
    plt.savefig("momento1.png")

    plt.figure()
    momento=[lesion[1][2] for lesion in momentos]
    momentosPromedios.append(np.mean(momento))
    plt.plot(np.log(momento),".")
    plt.title("Momento 3: Promedio: "+str(np.mean(momento)))
    plt.savefig("momento3.png")


    plt.figure()
    momento=[lesion[1][3] for lesion in momentos]
    momentosPromedios.append(np.mean(momento))
    plt.plot(np.log(momento),".")
    plt.title("Momento 4: Promedio: "+str(np.mean(momento)))
    plt.savefig("momento4.png")

    plt.figure()
    momento=[lesion[1][4] for lesion in momentos]
    momentosPromedios.append(np.mean(momento))
    plt.plot(np.log(momento),".")
    plt.title("Momento 5: Promedio: "+str(np.mean(momento)))
    plt.savefig("momento5.png")

    plt.figure()
    momento=[lesion[1][5] for lesion in momentos]
    momentosPromedios.append(np.mean(momento))
    plt.plot(np.log(momento),".")
    plt.title("Momento 6: Promedio: "+str(np.mean(momento)))
    plt.savefig("momento6.png")

    plt.figure()
    momento=[lesion[1][6] for lesion in momentos]
    momentosPromedios.append(np.mean(momento))
    plt.plot(np.log(momento),".")
    plt.title("Momento 7: Promedio: "+str(np.mean(momento)))
    plt.savefig("momento7.png")
        #hay que enmascarar la imagen  con la segmentada
        #hay que crear histogramas para cada momento geometrico

    colores=["blue","green","red","cyan","magenta","yellow","black"]
    plt.figure()
    for i in xrange(7):
        momento=[lesion[1][i] for lesion in momentos]
        plt.plot(np.log(momento),".",color=colores[i])
    blue = mpatches.Patch(color='blue', label="M1")
    green = mpatches.Patch(color='green', label='M2')
    red = mpatches.Patch(color='red', label='M3')
    cyan = mpatches.Patch(color='cyan', label='M4')
    magenta = mpatches.Patch(color='magenta', label='M5')
    yellow = mpatches.Patch(color='yellow', label='M6')
    black = mpatches.Patch(color='black', label='M7')
    plt.legend(handles=[blue,green,red,cyan,magenta,yellow,black])
    plt.title("Todos los momentos")
    plt.savefig("momento8.png")

    plt.figure()
    plt.plot(range(1,len(momentosPromedios)+1),momentosPromedios,color="red")
    plt.plot(range(1,len(momentosPromedios)+1),momentosPromedios,"o",color="blue")
    plt.grid()
    plt.title("Promedio de momentos")
    plt.savefig("VectorPromedio.png")


    """
