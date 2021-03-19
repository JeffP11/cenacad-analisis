# coding=utf-8
# Colaboradores: Jeffrey Prado - Douglas Sabando

title = "Análisis de Sentimientos de comentarios en el Censo Académico"
libs = "Librerías TextBlob - VADER"
authors = "Jeffrey Prado - Douglas Sabando"
txt_1 = "a. Por término"
txt_2 = "b. Completo"
txt_3 = "c. Volver"
txt_4 = "Inserte selección: "
txt_5 = f"""
    1. Análisis de todos los profesores
    2. Análisis por profesor
    3. Salir
{txt_4}"""
txt_6 = f"""
    {txt_1}
    {txt_2}
    {txt_3}
{txt_4}"""

def head():
    print(title.center(150, ' '))
    print(libs.center(150, ' '))
    print(authors.center(150, ' '))

def menu():
    opt_1 = ''

    while opt_1 != '3':
        opt_1 = str(input(txt_5))

        if opt_1 == '1':
            opt_2 = ''
            while opt_2 != 'c':
                opt_2 = str(input(txt_6))
                if opt_2 == 'a':
                    print('todos los profesores, por termino')
                if opt_2 == 'b':  
                    print('todos los profesores, completo')

        if opt_1 == '2':
            opt_2 = ''
            while opt_2 != 'c':
                opt_2 = str(input(txt_6))
                if opt_2 == 'a':
                    print('un profesor, por termino')
                if opt_2 == 'b':  
                    print('un profesor, completo')

    print('\nGracias!')

if __name__ == "__main__":
    head()
    menu()