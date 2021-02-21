# coding=utf-8
# Colaboradores: Jeffrey Prado - Douglas Sabando
import os, nltk
import pandas as pd
from google_trans_new import google_trans_new as googletrans
from cenacad_sentiment import *

translator = googletrans.google_translator()
palabras_excluidas = ["SDSA", "NO", "-----", "NADA", "NADA.", "LOL", "l", "........",
                      "<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3<3",
                      "NINGUNO", "NINGUNA", "NINGUNA OBSERVACION", "NINGUN PROBLEMA", "NINGÚN COMENTARIO",
                      "NINGUN COMENTARIO", "SIN COMEN5ARIOS", "SIN NOVEDAD", "SIN NOVEDADES", "0 COMENTARIOS",
                      "SIN COMENTARIOS", "5MENTARIOS", "NADA QUE DECIR", "SIN NOVEDAD", "SIN NOVEDAD.", ":V", "YE",
                      "SIN OPINIO", "SIN OPINION", "STRJURS6KW6I6", "KHE", "S/N", "Ok", "F", "GG", "🍞", 'V":', "N/A",
                      "N.A", "NO NO NO NO", "BBBBBBBBBBBB", ".-.", ",,,,,", "BLA BLA BLA", "OOKEEY", ":|", "00",
                      "AE5UYE5UQ45UQ", "FFFFFFFFFFF", ':"(', "/*-*-/*-/*----------------------------",
                      "...............................", "............", "..................", "................",
                      "...............", "................", "--------------------", "--------------------------------",
                      ".............", ".................", "------------------------------------",
                      "aaaaaaaaaaaaaaaaaaaaa", "FYULRYOR6O88", "A35YUW46I56KIW", "syntax error"]

def print_message(message):
    """
        Se encarga de imprimir cualquier tipo de mensaje
        
            Argumentos:
                message(str) = mensaje que se encargará de imprimir
    """
    print(message)

def get_filenames():
    """
        Obtiene los paths de todos los archivos en los directorios FIEC_inf1 y FIEC_inf2 \n
        Ambos directorios se encuentran en la raíz del proyecto

            Argumentos:
                Ninguno
            
            Salida:
                (array) = lista ordenada con paths de todos los archivos en el formato (path de inf1, path de inf2)
    """
    from fnmatch import fnmatch
    from os import listdir
    from pathlib import Path

    directories = [d for d in listdir() if "FIEC" in d]
    folders = [Path(p) for p in directories]
    filenames = []
    inf_1 = []
    inf_2 = []
    for f in folders:
        if f.name == 'FIEC_inf1':
            for xlsx in f.iterdir():
                inf_1.append(xlsx)
        if f.name == 'FIEC_inf2':
            for xlsx in f.iterdir():
                inf_2.append(xlsx)
    for i,j in zip(inf_1, inf_2):
        tmp = (i, j)
        filenames.append(tmp)
    return filenames

def read_dataframes(filesList):
    """
        Lee los archivos .xlsx y acumula en una lista para trabajar con ellos
        
            Argumentos: 
                filesList (array) = arreglo que contiene los paths de archivos para abrir con pandas
            
            Salida:
                (array) = lista ordenada con dataframes en el formato (df de inf1, df de inf2)
    """
    dataframes = []
    for duo in filesList:
        df_inf1 = pd.read_excel(duo[0])
        df_inf2 = pd.read_excel(duo[1])
        tmp = (df_inf1, df_inf2)
        dataframes.append(tmp)
    return dataframes

def save_results(df, name, type='xlsx'):
    """
        Guarda archivo XLSX en el directorio resultados
        
            Argumentos:
                df (dataframe) = datagrame que se desea guardar 
                name (str) = nombre con el que se desea guardar el archivo
                type (str) = tipo de archivo, por defecto es xlsx, también admite csv
            
            Salida:
                Ninguna

    """
    year = f'{name}.xlsx'
    final_name = r'resultados\\' + year

    if type == 'xlsx':
        df.to_excel(final_name, index=False, header=True)

    if type == 'csv':
        df.to_csv(final_name, index=False, header=True)

def sanitize_txt(txt):
    """
        Limpia caracteres en los comentarios

            Argumentos:
                txt (str) = comentarios que se dese limpiar

            Salida:
                (str) = comentario limpio

    """
    txt = txt.replace("Ã¡", "á").replace("Ã©", "é").replace("Ã­", "í").replace("Ã³", "ó").replace("Ãº", "ú").replace(
        "Ã±", "ñ").replace("Ã‰", "É").replace("Ã“", "Ó").replace("Ãš", "Ú").replace("Ã‘", "Ñ")
    return txt

def translate_txt(txt, translator=translator):
    """
        Traduce el texto que se le envia
        
            Argumentos:
                txt (str) = comentario a traducir
                translator (google_translator()) = por defecto recibe la clase encargada de consumir la API de Google
            
            Salida:
                (str) = comentario traducido
    """
    txt = translator.translate(txt, lang_tgt='en')
    return txt

def tokenize_txt(txt):
    """
        Separa el texto que se le envia en tokens para aplicarle el analisis de sentimientos
        
            Argumentos:
                txt (str) = comentario que se desea tokenizar
            
            Salida:
                (array) = comentario tokenizado
    """
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(txt)
    return sentences

def add_total(id, means, key):
    """
        Retorna el valor de la clave que se desea obtener en el diccionario que contiene los totales y promedios por profesor
        
            Argumentos:
                id (str) = cédula del profesor sobre el cual se van a agregar los campos del diccionario means
                means (dict) = diccionario que contiene la polaridad, cantidad de comentarios y de 
                calificaciones positivas, neutras y negativas por profesor
                key (str) = llave para obtener el valor dentro del diccionario obtenido de means acorde al id solicitado
            
            Salida:
                (int) = valor obtenido del diccionario interno de means, puede ser: total, polaridad, comentarios o 
                calificaciones positivas, neutras y negativas
    """
    tmp = means.get(id, None)
    total = tmp.get(key, None)
    return total

def iterar(grouped):
    """
        Itera los sub sets agrupados por profesor para retornar el diccionario que contiene los valores de totales y promedios
        
            Argumentos:
                grouped (obj:DataFrameGroupBy) = agrupado por profesor
            
            Salida:
                (dict) = diccionario que contiene la polaridad, cantidad de comentarios y de 
                calificaciones positivas, neutras y negativas
    """
    means = {}
    for key, values in grouped:
        total = len(values)
        suma = values['VADER POLARITY'].sum()
        mean = suma/total
        dicc_int = means.get(key, dict())
        dicc_int['polarity mean'] = mean
        dicc_int['total'] = total
        dicc_int['comments_pos'] = len(values[values['VADER POLARITY'] > 0.0])
        dicc_int['comments_neg'] = len(values[values['VADER POLARITY'] < 0.0])
        dicc_int['comments_neu'] = len(values[values['VADER POLARITY'] == 0.0])
        dicc_int['scores_pos'] = len(values[values['PROMEDIO PROFESOR'] > values['PROMEDIO UNIDAD ENCUESTA']])
        dicc_int['scores_neg'] = len(values[values['PROMEDIO PROFESOR'] < values['PROMEDIO UNIDAD ENCUESTA']])
        dicc_int['scores_neu'] = len(values[values['PROMEDIO PROFESOR'] == values['PROMEDIO UNIDAD ENCUESTA']])
        means[key] = dicc_int
    return means

def make_resumes(filesList):
    """
        Genera cada archivo resumen del par de dataframes, es decir crea el archivo por año y semestre \n
        Recibe pareja del 2015_1S -> (2015_1S INF1, 2015_1S INF2) \n
        Intersecta ambos dataframes eliminando las filas que no contengan comentarios \n
        Crea dataframe 2015_1S que contiene ya toda la información resumida
        
            Argumentos:
                filesList (array) = lista que contiene parejas de paths de archivos (path de INF1, path de INF2)
            
            Salida:
                Ninguna
    """
    dataframes = read_dataframes(filesList)
    for index in range(len(dataframes)):
        nombre = filesList[index][0].name.split('.')[0][-7:]
        if '2015' in nombre or '2016' in nombre: continue
        print_message(f"Iniciando proceso de dataframes del {nombre}")

        pair = dataframes[index]

        df1 = pair[0]
        df1 = df1.drop(columns=['UNIDAD', 'EVALUADOS FUERA PERIODO', 'PREGUNTAS', 'DESVIACIÓN ESTÁNDAR'])

        df2 = pair[1]
        comments = df2['COMENTARIO REALIZADO']
        comment_cond_1 = comments.notnull()
        comment_cond_2 = ~comments.str.upper().isin(palabras_excluidas)
        comment_cond_3 = comments.str.len() > 10
        df2_filtered = df2[comment_cond_1 & comment_cond_2 & comment_cond_3].drop(columns=['UNIDAD'])
        
        df_result = pd.merge(df1, df2_filtered, how='left',
                     left_on=['CODIGO MATERIA', 'NOMBRE MATERIA', 'PARALELO', 'AÑO', 'TÉRMINO'],
                     right_on=['CODIGO MATERIA', 'NOMBRE MATERIA', 'PARALELO', 'AÑO', 'TÉRMINO'])


        df_result_comments = df_result['COMENTARIO REALIZADO']
        df_result = df_result[df_result_comments.notnull()].drop_duplicates()

        print_message(f"Dataframes del {nombre} filtrados")

        df_result['COMENTARIO LIMPIO'] = df_result.apply(lambda row: sanitize_txt(row['COMENTARIO REALIZADO']), axis=1)

        print_message(f"Comentarios del {nombre} limpios")

        df_result['COMENTARIO TRADUCIDO'] = df_result.apply(lambda row: translate_txt(row['COMENTARIO LIMPIO']), axis=1)

        print_message(f"Comentarios del {nombre} traducidos")
        
        df_result['COMENTARIO TOKENIZED'] = df_result.apply(lambda row: tokenize_txt(row['COMENTARIO TRADUCIDO']), axis=1)

        print_message(f"Iniciando análisis de sentimientos")
        
        # TextBlob no soporta demasiadas requests de analisis
        # df_result['TEXTBLOB POLARITY'] = df_result.apply(lambda row: analyze_txt_textblob(row['COMENTARIO TRADUCIDO']), axis=1)
        
        df_result['VADER POLARITY'] = df_result.apply(lambda row: analyze_txt_vader(row['COMENTARIO TOKENIZED']), axis=1)

        print_message(f"Análisis de sentimientos terminado")

        grouped = df_result.groupby('NUMERO IDENTIFICACIÓN')
        means = iterar(grouped)

        print_message(f"Generando resumen")

        df_result['NEGATIVE SCORE'] = df_result.apply(lambda row: add_total(row['NUMERO IDENTIFICACIÓN'], means, 'scores_neg'), axis=1)
        df_result['NEUTRAL SCORE'] = df_result.apply(lambda row: add_total(row['NUMERO IDENTIFICACIÓN'], means, 'scores_neu'), axis=1)
        df_result['POSITIVE SCORE'] = df_result.apply(lambda row: add_total(row['NUMERO IDENTIFICACIÓN'], means, 'scores_pos'), axis=1)

        df_result['TOTAL'] = df_result.apply(lambda row: add_total(row['NUMERO IDENTIFICACIÓN'], means, 'total'), axis=1)

        df_result['NEGATIVE COMMENTS'] = df_result.apply(lambda row: add_total(row['NUMERO IDENTIFICACIÓN'], means, 'comments_neg'), axis=1)
        df_result['NEUTRAL COMMENTS'] = df_result.apply(lambda row: add_total(row['NUMERO IDENTIFICACIÓN'], means, 'comments_neu'), axis=1)
        df_result['POSITIVE COMMENTS'] = df_result.apply(lambda row: add_total(row['NUMERO IDENTIFICACIÓN'], means, 'comments_pos'), axis=1)

        df_result['VADER POLARITY MEAN'] = df_result.apply(lambda row: add_total(row['NUMERO IDENTIFICACIÓN'], means, 'polarity mean'), axis=1)

        print_message(f"Guardando resumen completo")

        save_results(df=df_result, name=nombre+" resumen", type='xlsx')

        df_final = df_result[['CODIGO MATERIA', 'NOMBRE MATERIA', 'NUMERO IDENTIFICACIÓN', 'PROMEDIO PROFESOR', 'NEGATIVE SCORE', 
                    'NEUTRAL SCORE', 'POSITIVE SCORE', 'TOTAL', 'NEGATIVE COMMENTS','NEUTRAL COMMENTS', 'POSITIVE COMMENTS', 
                    'VADER POLARITY MEAN']].drop_duplicates()

        print_message(f"Guardando resumen numerico")

        save_results(df=df_final, name=nombre, type='xlsx')

        print_message(f"Resumenes {nombre} guardados con éxito")

def make_graph(grouped):
    """
        Generar graficos
        Guarda los graficos
        
            Argumentos:
                grouped (obj:DataFrameGroupBy) = agrupado por profesor 
                del dataframe que es resultado final
            
            Salida:
                Ninguna
    """
    import matplotlib.pyplot as plt
    for id in grouped.groups:
        tmp = grouped.get_group(id)
        total = len(tmp)

        pos_score = tmp['PROMEDIO PROFESOR'] > 86.27
        neu_score = tmp['PROMEDIO PROFESOR'] == 86.27
        neg_score = tmp['PROMEDIO PROFESOR'] < 86.27

        pos_polar = tmp['VADER POLARITY MEAN'] > 0.0
        neu_polar = tmp['VADER POLARITY MEAN'] == 0.0
        neg_polar = tmp['VADER POLARITY MEAN'] < 0.0

        score_pos_polarity_pos = len(tmp[pos_score & pos_polar])
        score_pos_polarity_neg = len(tmp[pos_score & neg_polar])
        score_neg_polarity_pos = len(tmp[neg_score & pos_polar])
        score_neg_polarity_neg = len(tmp[neg_score & neg_polar])

        values = [score_pos_polarity_pos, score_pos_polarity_neg, score_neg_polarity_pos, score_neg_polarity_neg]
        labels = ["Calificación positiva\nPolaridad positiva", "Calificación positiva\nPolaridad negativa", 
                "Calificación negativa\nPolaridad positiva", "Calificación negativa\nPolaridad negativa"]
        plt.pie(values, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title("Distribución de Calificación vs Polaridad " + id)
        plt.savefig("graficos/" + id + ".jpg")
        # plt.cla() #clean axes
        plt.clf() #clean figures
        plt.close() #close actual

if os.path.exists("resultados/"):
    if not os.listdir("resultados/") :
        files = get_filenames()
        make_resumes(files)

if os.path.exists("graficos/"):
    if not os.listdir("graficos/") :
        result = pd.read_excel(r'resultados\final_result.xlsx', engine='openpyxl')
        grouped = result.groupby('NUMERO IDENTIFICACIÓN')
        make_graph(grouped)
