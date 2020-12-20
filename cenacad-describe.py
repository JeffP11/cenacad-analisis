import sys

# Obtiene los paths de todos los archivos en los directorios FIEC_inf1 y FIEC_inf3
def getFilenames():
    from fnmatch import fnmatch
    from os import listdir
    from pathlib import Path

    directories = [d for d in listdir() if "FIEC" in d]
    folders = [Path(p) for p in directories]
    filenames = []
    for f in folders:
        for xlsx in f.iterdir():
            filenames.append(xlsx)
    return filenames

# Lee los archivos .xlsx y acumula en una lista para trabajar con ellos
def readDataframes(filesList):
    import pandas as pd
    return [pd.read_excel(f) for f in filesList]

# TO DO generar graficos
def makeGraph(data):
    from pandas import matplotlib as mtp
    return 0

# Redirecciona el standard otuput a archivos en el directorio resultados
def saveResults(flag, name=None, stdout=None):
    if flag and name:
        sys.stdout = open(f"{name}.txt", "w")
    else:
        sys.stdout.close()
        sys.stdout = original_stdout

if __name__ == "__main__":

    files = getFilenames()
    dataframes = readDataframes(files)

    # Guarda el default config del standard otuput 
    original_stdout = sys.stdout

    # Genera cada archivo resumen del dataframes
    for i in range(len(dataframes)):
        nombre = "resultados/" + str(files[i].name)
        saveResults(flag=True, name=nombre)
        print(dataframes[i].describe())
    
    # Redireccionar el standard output de vuelta a la consola
    saveResults(flag=False,stdout=original_stdout)
