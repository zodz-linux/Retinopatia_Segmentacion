import multiprocessing

def Create4Process(xfiles,function):
    pros=[]
    for xfile in xfiles:
        pros.append(multiprocessing.Process(target=function,args=(xfile,)))
    for p in pros:
        p.start()
    for p in pros:
        p.join()
    pass
