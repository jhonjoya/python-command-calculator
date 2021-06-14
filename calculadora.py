import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # Si el equipo corre Windows usa comando 'cls'
        command = 'cls'
    os.system(command)

class Operaciones:
    def __init__(self): #Declaración para crear un objeto que va a almacenar las líneas de operaciones
        self.operadores=[]
    
    def agregarOperador(self,operacion,resultado): #Método para agregar una lista de comandos al objeto creado
        self.operadores.append(operacion+' = '+str(resultado))
    
    def mostrarResultado(self): #se encarga de mantener ordenado la línea de comandos, mostrandos los anteriores
        cont=0
        for i in self.operadores:
            print(f'command_line[{cont}]:',i)
            cont+=1
    
    def tamanoObjeto(self): #permite obtener el número de objetos almacenados para visualizar en la entrada de cada línea
        return len(self.operadores)
            
def encontrarPosiciones(cadenaEntrada): #Función que se encarga de extraer los operadores presentes en la cadena
    posDef=[]
    operadores=['^','/','*','+','-']
    for operador in operadores:
        cadena1 = cadenaEntrada
        pos1=0
        pos2=0
        pos=[]
        while(cadena1.find(operador) > -1):
            pos1 = cadena1.find(operador)
            pos2+=pos1
            if operador=='-' and pos2 !=0: #Algoritmo que extrae el operador '-' (menos) pero conserva el número si es negativo
                try:
                    num=float(cadenaEntrada[pos2-1])
                    pos.append(pos2)
                except:
                    pass
            elif operador!='-':
                pos.append(pos2)
            pos1+=1
            cadena1=cadena1[pos1:] #Permite recortar la cadena para extraer posición de operadores ordenadamente
            pos2+=1
        posDef.append(pos)
    return posDef

def extraerNumeros(cadenaEntrada): #Función que permite extraer una lista de los números contenidos en la cadena, decimales, enteros, positivos y negativos
    valido=True
    listaNumeros=[]
    """El siguiente arbol de operaciones fracciona la cadena de caracteres con números y operaciones
    para obtener los números disponibles para operación, realizando la división en cadenas según el
    operador, comenzando con la potencia(^), después la división(/), sigue con la multiplicación (*),
    continua con la suma(+) y finalizando con la resta(-)"""
    listaEntrada=cadenaEntrada.split('^')
    for l0 in listaEntrada:
        try:
            listaNumeros.append(float(l0))
        except:
            l0=l0.split('/')
            for l1 in l0:
                try:
                    listaNumeros.append(float(l1))
                except:
                    l1=l1.split('*')
                    for l2 in l1:
                        try:
                            listaNumeros.append(float(l2))
                        except:
                            l2=l2.split('+')
                            for l3 in l2:
                                try:
                                    listaNumeros.append(float(l3))
                                except:
                                    l3=l3.split('-')
                                    for l4 in l3:
                                        try:
                                            listaNumeros.append(float(l4))
                                        except:
                                            valido = False
    if valido:
        return listaNumeros, valido
    else:
        return [], valido

def reconstruirLista(numeros, operadores): #Crea una lista con cada operador y número presente en la cadena
    longitud=0
    operandosDesordenados={}
    count=0
    for listaOperador in operadores:
        longitud+=len(listaOperador)
        if count==0: oper='^'
        elif count==1: oper='/'
        elif count ==2: oper='*'
        elif count ==3: oper='+'
        elif count ==4: oper='-'
        for item in listaOperador:
            operandosDesordenados[item]=oper #Crea un diccionario con los operadores y su posicion desordenada
        count+=1
    longitud+=len(numeros)
    operandosOrden=list(operandosDesordenados.keys())
    nuevOrden=[i for i in range(longitud) if i%2!=0] #Crea una lista para ordenar los operadores a ubicar
    operandosOrden.sort() #Ordena la lista de operadores
    count=0
    listaNumeros=numeros
    """Se insertan los operadores en los espacios entre números"""
    for elemento in operandosOrden:
        listaNumeros.insert(nuevOrden[count], operandosDesordenados[elemento])
        count+=1
    return listaNumeros

def calcular(listaElementos):
    """Emplea una función que realiza operaciones matemática para operar los dos números que están a la izquierda
    y derecha del operador, priorizando siempre la potencia, la división, la multiplicación, la resta y la suma
    """
    iteracion=listaElementos
    while len(iteracion) > 1:
        count=0
        for elemento in iteracion:
            if iteracion[count] == '^':
                nuevoValor=iteracion[count-1]**iteracion[count+1]
                eliminar=count-1
                for i in range(3):
                    del iteracion[eliminar]
                iteracion.insert(eliminar, nuevoValor)
            count+=1
        count=0
        for elemento in iteracion:
            if iteracion[count] == '/':
                nuevoValor=iteracion[count-1]/iteracion[count+1]
                eliminar=count-1
                for i in range(3):
                    del iteracion[eliminar]
                iteracion.insert(eliminar, nuevoValor)
            count+=1
        count=0
        for elemento in iteracion:
            if iteracion[count] == '*':
                nuevoValor=iteracion[count-1]*iteracion[count+1]
                eliminar=count-1
                for i in range(3):
                    del iteracion[eliminar]
                iteracion.insert(eliminar, nuevoValor)
            count+=1
        count=0
        for elemento in iteracion:
            if iteracion[count] == '-':
                nuevoValor=iteracion[count-1]-iteracion[count+1]
                eliminar=count-1
                for i in range(3):
                    del iteracion[eliminar]
                iteracion.insert(eliminar, nuevoValor)
            count+=1
        count=0
        for elemento in iteracion:
            if iteracion[count] == '+':
                nuevoValor=iteracion[count-1]+iteracion[count+1]
                eliminar=count-1
                for i in range(3):
                    del iteracion[eliminar]
                iteracion.insert(eliminar, nuevoValor)
            count+=1
    return iteracion

def run():
    continuar='Y'
    listaResultados=Operaciones()
    while continuar=='Y' or continuar=='y':
        clearConsole()
        listaResultados.mostrarResultado()
        entrada="command_line[{0}]: ".format(listaResultados.tamanoObjeto())
        cadena=input(entrada)
        separacion, validar=extraerNumeros(cadena)
        if validar:
            posi=encontrarPosiciones(cadena)
            listaCompleta=reconstruirLista(separacion,posi)
            try:
                total=calcular(listaCompleta)
                if total[0] == int(total[0]): #Simplifica la vista del resultado eliminado decimales innecesarios
                    totalF = int(total[0])
                else:
                    totalF=round(total[0],4)
                listaResultados.agregarOperador(cadena, totalF)
                clearConsole()
                listaResultados.mostrarResultado()
            except ZeroDivisionError:
                print("Error en división por Cero")
            except OverflowError:
                print("Número tiende a infinito")
        else:
            print("valores Inválidos")
        continuar=input("¿Desea continuar(y)?")
    clearConsole()
    listaResultados.mostrarResultado()
    print("Gracias por utilizar la calculadora básica de jhonjoya@gmail.com")

if __name__=='__main__':
    run()