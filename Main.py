import PySimpleGUI as sg
import ArbolDlexemas as Arbol
import Error
import Variable
import Function
import numpy as np

#variables globales
output = ""

joken_log = ["EQUAL","<",">","<=",">=","AND","OR","!="]

Palabras_reservadas = Arbol.AVLTree()

Joken_reserv = ["IF","WHILE","FOR","VARIABLES","END","PRINT",";","FUN","PROGRAM"]
for i in Joken_reserv:
    Palabras_reservadas.insert(i)

instrucciones = []
lexemasXinstruccion = []
#----------------------------------------------------------------------------

Joken_types = Arbol.AVLTree()
variables_program = []
functions_program = []

Joken_tipos = ["STRING","CHAR","INT","BOOL","NULL","LIST"]
for i in Joken_tipos:
    Joken_types.insert(i)

def separa_Instrucciones(codigo):
    return codigo.split('\n')

def ComposicionLexica(codigo):
    return codigo.split(' ')

def make_window():
    condicionales = ["simple","compuesto"]
    bucles = ["FOR","WHILE"]

    menu_def = [
                ['&Opciones',['Palabras reservadas',Joken_reserv,
                              'Sintaxis',['control',["condicionales",condicionales],["bucles",bucles],'funciones','operaciones'],'Semantica','tipos de datos',Joken_tipos]],
                ['&Help', '&About']]

    layout = [ [sg.Menu(menu_def,tearoff=True)] 
    ,[sg.Text('---------------------------------------------------CODE-------------------------------------------', justification='top', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=False)],
    [[sg.Button('COMPILAR'),sg.Button('EJECUTAR')],  [sg.Multiline(size=(45,15), expand_x=True, expand_y=True, k='CODE')]],
    [sg.Text('-----------------------------------------------OUTPUT----------------------------------------', justification='top', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='OUTPUT')],
      [[sg.Multiline(size=(45,10), expand_x=True, expand_y=True, k='salida',disabled=True)]]]
    layout[-1].append(sg.Sizegrip()) 
    window = sg.Window('J Retana k granados JOKEN',layout,resizable=True,return_keyboard_events=True)
    return window

def remove_Carac_Muertos(the_list, val,val2,val3):
   return [value for value in the_list if value != val and value != val2 and value !=val3]

def LimpiarCodigo(matriz):
    code_limpio = []
    for instr in matriz:

        for i in range(len(instr)):
            instr[i]=instr[i].replace('\t','')

        code_limpio.append(remove_Carac_Muertos(instr,'',' ','\t'))

    return [value for value in code_limpio if len (value) != 0]

def SintaxisBasica(mat):
    ultima_fila = len(mat)-1
    err=None
    if mat[ultima_fila][0].upper() != "END":
        err = Error.Error(ultima_fila,"Joken program must be ended whith END whithout exception","incomplete program sintax","0001")
    if len(mat[ultima_fila]) > 1 != None and mat[ultima_fila][1].upper() != "PROGRAM" or len(mat[ultima_fila]) > 2:
         err = Error.Error(ultima_fila,"END statement can only be behind pregonate PROGRAM","incorrect sintax","0002")
    if mat[0][0].upper() != "VARIABLES":
         err = Error.Error(ultima_fila,"Joken program must be started whith VARIABLES whithout exception","incomplete program sintax","0003")

    return err

def IsVarType(lexema):
    return Joken_types.FindLexema(lexema.upper())
def IsReservada(lexema):
    return Palabras_reservadas.FindLexema(lexema.upper())

def IsVariable(lex):#retorna true si el identificador de variable existe
    return any(obj.identifier == lex for obj in variables_program)

def IsFuncion(lex):#retorna true si el identificador de funcion existe
    return any(obj.identifier == lex for obj in functions_program)

def LeerVariables(instruct):
    """
    It takes a list of strings and creates a list of variables
    
    :param instruct: The instruction that is being read
    """
    if instruct[1] == '[' and instruct[-1] == ']' and  len(instruct) > 3:
        index = 2
        while index < len(instruct)-1:
            if IsVarType(instruct[index]) and not IsReservada(instruct[index+1]) and not IsVarType(instruct[index+1]):
                
                variables_program.append(Variable.Variable(instruct[index+1],instruct[index],None))
            index+=2

def IsCondicional(instruct):
    return instruct[0].upper() == "IF"

def IsWhile(instruct):
    return instruct[0].upper() == "WHILE"

def IsFor(instruct):
    return instruct[0].upper() == 'FOR'

def IsOperation(instruct):
    return instruct[1] == "*" or instruct[1] == "/" or instruct[1] == "+" or instruct[1] == "-"

def IsAsignacion(instruct):
    return IsVariable(instruct[0]) and instruct[1] == '='

def AsignarValue(instruct):
    identifier = instruct[0]
    igual = instruct.index("=")
    val=None
    asignado = instruct[igual+1:len(instruct)]# sub array despues del =
    print ('asignando...',*asignado)
    if asignado: #no vacia
        if len(asignado) == 1 and asignado[0].isnumeric():#asigna un numero
            val = int(asignado[0])
        elif len(asignado) > 1 and asignado[0] == '"' and asignado[-1] == '"':#asigna string
            val = ' '.join(asignado)
            print("asigna string")
        elif len(asignado) == 1 and not asignado[0].isnumeric() and asignado[0].upper() == 'TRUE' or asignado[0].upper() == 'FALSE':
            val = asignado[0].upper() == 'TRUE'
        elif len(asignado) == 1 and asignado[0].upper() == 'NULL':
            val = None
        elif len(asignado) > 1 and IsOperation(asignado):
            result = Resultado_Operacion(asignado)
            if result != None:
                val = result
            else:
                return Error.Error(-1,"error found on operation","sintax error",'jk025')

        elif asignado[0].upper() == '-' and asignado[1].isnumeric():
            val = 0 - int(asignado[1])
        elif asignado[0].upper() == '[' and asignado[-1].upper() == ']':#es lista
            joken_list = asignado[1:len(asignado)-1]
            while ',' in joken_list: joken_list.remove(',')
            nueva = []
            for x in joken_list:
                if x.isnumeric():
                    nueva.append(int(x))
                elif x.upper() == 'TRUE' or x.upper() == 'FALSE':
                    nueva.append(x.upper() == 'TRUE')
                elif x.upper() == 'NULL':
                    nueva.append(None)
                elif IsVariable(x):
                    nueva.append(GetVariable(x).valor)
                else :
                    nueva.append(x)
            val = nueva
        else:
            return Error.Error(-1,"error found on asignation","sintax error",'jk025')
        global variables_program
        for i in range(len(variables_program)):
            if variables_program[i].identifier == identifier:
                variables_program[i].valor = val
                variables_program[i].data_type = type(val)
                print("valor asignado")
        
    else:
        return Error.Error(-1,"error found on asignation","sintax error",'jk025')
        

def GetVariable(identifier):
    objeto = None
    for k in variables_program:
        if k.identifier == identifier:
            objeto = k
    return objeto


def GetFunction(identifier):
    objeto = None
    for k in functions_program:
        if k.identifier == identifier:
            objeto = k
    return objeto

def joken_print(instruct):
    global output
    for i in instruct:
        if IsVariable(i):
            variable = GetVariable(i)
            if not isinstance(variable.valor,str):
                output += str(variable.valor) + '\n'

            elif variable.valor == None:
                output += 'null' + '\n'
            
            else: 
                output += variable.valor + '\n'
        else:
            output += i + ' '
    print("joken_print...",output)

def Resultado_Operacion(operacion):
    v1 = None
    v2 = None
    sale = None
    global err
    if IsVariable(operacion[0]):
        v1 = GetVariable(operacion[0])
    elif operacion[0].isnumeric():
        v1 = Variable.Variable("",type(int),int(operacion[0]))

    if IsVariable(operacion[2]):
        v2 = GetVariable(operacion[2])
    elif operacion[2].isnumeric():
        v2 = Variable.Variable("",type(int),int(operacion[2])) 

    if isinstance(v2.valor,int) and isinstance(v1.valor,int):
        print ("realizando operacion matematica ...",operacion[0]+operacion[1]+operacion[2])
        if operacion[1] == '*':
             sale =  v1.valor * v2.valor
        elif operacion[1] == '/' and v2.valor != 0:
            sale = v1.valor / v2.valor
        elif operacion[1] == '+':
             sale =  v1.valor + v2.valor
        elif operacion[1] == '-':
             sale = v1.valor - v2.valor
    else:  
        err = Error.Error(-1,"error en la operación matematica",'sintax error','jk0079')
    print('resultado de la operacion...',sale)
    return sale
def Resultado_Condicion(cond_array):
    v1 = None
    v2 = None
    if IsVariable(cond_array[0]):
        v1 = GetVariable(cond_array[0])
    elif cond_array[0].isnumeric():
        v1 = Variable.Variable("",type(int),int(cond_array[0]))
    elif cond_array[0].upper() == "TRUE":
        v1 = Variable.Variable("",type(bool),True)
    elif cond_array[0].upper() == "FALSE":
        v1 = Variable.Variable("",type(bool),False)

    if IsVariable(cond_array[2]):
        v2 = GetVariable(cond_array[2])
    elif cond_array[2].isnumeric():
        v2 = Variable.Variable("",type(int),int(cond_array[2]))    

    if isinstance(v2.valor,int) and isinstance(v1.valor,int):#si es entero
        if cond_array[1] == '<':
            return  v1.valor < v2.valor
        elif cond_array[1] == '>':
            return  v1.valor > v2.valor
        elif cond_array[1] == '>=':
            return  v1.valor >= v2.valor
        elif cond_array[1] == '<=':
            return  v1.valor <= v2.valor
        elif cond_array[1].upper() == 'EQUAL':
            return  v1.valor == v2.valor
        elif cond_array[1] == '!=':
            return  v1.valor != v2.valor
    elif isinstance(v2.valor,bool) and isinstance(v2.valor,bool):
        if cond_array[1].upper() == 'EQUAL':
            return  v1.valor == v2.valor
        elif cond_array[1] == '!=':
            return  v1.valor != v2.valor
    elif isinstance(v2.valor,type(None)) and isinstance(v1.valor,type(None)): 
        return True
""""
def Findoperator_logico(instruct):
    i = 0
    for i in instruct:
        if i in joken_log and i:
            i+=1
"""

def finDfunction(index):
    i = index
    print ("index {} len {}",index,len(lexemasXinstruccion)-1)
    for i, elem in enumerate(lexemasXinstruccion):
        print (lexemasXinstruccion[i][0])
        if elem[0] == ';':
            return i
    return -1

def Ejecutar_func(iden,args):
    global variables_program
    fn = GetFunction(iden)
    if fn != None and len(fn.args) == len(args):
        for f, a in zip(fn.args,args):
            if a.isnumeric():
             variables_program.append(Variable.Variable(f,int,int(a)))
            else:
             variables_program.append(Variable.Variable(f,type(a),a))
    
        i = 0
        for j in fn.codigo:
            err = AnalizarInstruccion(j,i)
            if err != None:
                return err
                break
            i+=1

def AnalizarInstruccion(instruct,linea):
    global lexemasXinstruccion
    global variables_program
    print('analizando linea ',linea)
    if(IsCondicional(instruct)):
        if instruct[1] == "[" and instruct[-1] == ']':
            print('if correcto')
            comas = instruct.count(',')
            if comas == 1:#condicional simple
                salida = instruct[2:instruct.index(',')]# del inicio a la primera coma es la salida si se cumple la condicion
                condicion = instruct[instruct.index(',')+1:len(instruct)-1]
                print ('condicion de if...',*condicion)
                print ('salida de if...',*salida)
                verdad = Resultado_Condicion(condicion)
                print ('resultado condicion ',verdad) 
                if verdad :
                    return AnalizarInstruccion(salida,linea)
                return None
            elif comas == 2:# compuesto

                ultima_coma = (len(instruct) - 1 - instruct[::-1].index(','))
                primer_coma = instruct.index(',')
                salida_true = instruct[2:primer_coma]# del inicio a la primera coma es la salida si se cumple la condicion
                salida_false = instruct[ultima_coma+1:len(instruct) -1]
                salida = None
                condicion = instruct[primer_coma+1:ultima_coma]
                print ('condicion de if...',*condicion)
                print ('salida de true...',*salida_true)
                print ('salida de false...',*salida_false)
                verdad = Resultado_Condicion(condicion)
                print ('resultado condicion ',verdad) 
                if verdad :
                    salida = salida_true
                else :
                    salida = salida_false

                if salida != None:
                    AnalizarInstruccion(salida,linea)
                    return None
                return Error.Error(linea,"could'nt get output on if condition","No output",'jk0010')
            else:
                return Error.Error(linea,"error found on if condition","sintax error",'jk005')
        else:
            return Error.Error(linea,"error found on if condition","sintax error",'jk005')
    elif IsAsignacion(instruct):
        if AsignarValue(instruct) != None:
            return Error.Error(linea,"error found on asignation","sintax error",'jk015')

        print("Variables desp de asignar",*variables_program)    
        
        return None
    elif instruct[0].upper() == 'PRINT':
            if len(instruct) > 1 and instruct[1] == '(' and instruct[-1] == ')':     
                joken_print(instruct[2:len(instruct)-1])
            else:
                return Error.Error(linea,"error found on print function","sintax error",'jk005')
    elif IsWhile(instruct):# while [ do, condition ]
        error = None
        if instruct[1] == "[" and instruct[-1] == ']':
                do_this = instruct[2:instruct.index(',')]# del inicio a la primera coma es la salida si se cumple la condicion
                condicion = instruct[instruct.index(',')+1:len(instruct)-1]

                if ';' in do_this:
                    do_this = ' '.join(do_this)
                    do_this = do_this.split(';')
                    aux=[]
                    for d in do_this:
                        a = d.split(' ')
                        a[:] = (value for value in a if value != '')
                        aux.append(a)
                    do_this = aux
                    print ('do this while ',do_this)

                    while ' ' in do_this: do_this.remove('')

                    while Resultado_Condicion(condicion):
                        for l in do_this:
                            error = AnalizarInstruccion(l,linea)
                            if error != None: break

                print ('ejecuta mientras...',*condicion)
                print ('a ejecutar en cada iteracion ',*do_this) 
                while Resultado_Condicion(condicion):
                    error = AnalizarInstruccion(do_this,linea)
                    if error != None: break
        else:
                error = Error.Error(linea,"error found on while loop","sintax error",'jk005')

        return error 
    elif IsFor(instruct):# for [ do ; declare iterador ,condition, increase]
        print ('entra al for')
        if instruct[1] == "[" and instruct[-1] == "]":
                ultima_coma = (len(instruct) - 1 - instruct[::-1].index(','))
                primer_coma = instruct.index(',')
                puntoYcoma = instruct.index(';')
                do_this = instruct[2:puntoYcoma]
                var_itera = instruct[puntoYcoma+1:primer_coma]# del inicio a la primera coma es la declaracion del iterador
                modif_iter = instruct[ultima_coma+1:len(instruct) -1]
                condicion = instruct[primer_coma+1:ultima_coma]
                print ('do_this | ', do_this, 'condicion',condicion, '| modif_iter ', modif_iter ,'|var_itera ',var_itera)

                if not IsReservada(var_itera[0]) and not IsVariable(var_itera[0]) and not IsFuncion(var_itera[0]):
                    variables_program.append(Variable.Variable(var_itera[0],int,None))                
                    if IsAsignacion(var_itera):
                        if AsignarValue(var_itera) != None:
                            return Error.Error(linea,"error found on asignation","sintax error",'jk015')

                    error = None
                while Resultado_Condicion(condicion):
                    print ('ejecutando ',do_this)
                    error = AnalizarInstruccion(do_this,linea)
                    if AsignarValue(modif_iter) != None:
                            return Error.Error(linea,"error found on asignation","sintax error",'jk015')
                    if error != None: break          

                print ('for terminado')

        else:
            error = Error.Error(linea,'expected correct [ ] in for','incomplete sintax','jk0018')

        return error          
    elif instruct[0].upper() == 'FUN':#DECLARA FUNCION
        print ("es funcion")
        if instruct[2] == '[' and instruct[-1] == ']' and not IsVariable(instruct[1]) and not IsReservada(instruct[1]):
            global functions_program
            global err
            cierra = finDfunction(linea)
            params = instruct[3:len(instruct)-1]
            obj_params = []
            
            for i in params:
                obj_params.append(Variable.Variable(i,'',''))
            print('parametros ',*params)

            if cierra == -1:
                return Error.Error(linea,'function not closed whith the corresponding ;','impcomplete sintax','j0017')
            else:
                cod_function = lexemasXinstruccion[linea+1:cierra]
                print ('codigo dentro de la función ',cod_function)
                del lexemasXinstruccion[linea+1:cierra]
                print ('codigo en la funcion :',*cod_function)
                functions_program.append(Function.Function(instruct[1],instruct[3:len(instruct)-1],cod_function,None))
                print (*functions_program)
        else:
            error = Error.Error(linea,'expected correct [ ] in while','incomplete sintax','jk0018')
    elif IsFuncion(instruct[0]) and len(instruct) > 1 and instruct[1] == '(' and instruct[-1] == ')':
        print ('llamando función ',instruct[0])
        Ejecutar_func(instruct[0],instruct[2:len(instruct)-1])

def main():
    global lexemasXinstruccion
    window = make_window()
    while True:
        event, values = window.read()
        print (event)
    #End program if user closes window
        if event == sg.WIN_CLOSED: 
            break
        elif (event == 'COMPILAR' or event == 'c:67') and values['CODE'] != "":
            global output
            output = ""
            global variables_program
            variables_program.clear()

            instrucciones = separa_Instrucciones(values['CODE'])
            lexemasXinstruccion = list(map(ComposicionLexica,instrucciones))#separa cada instrucción en un array de lexemas
            lexemasXinstruccion = LimpiarCodigo(lexemasXinstruccion)# elimina espacios en blanco o muertos
            err = SintaxisBasica(lexemasXinstruccion)
            if err != None:
                print ("hay errores")
                window['salida'].Update(err,text_color='red')
            else:
                LeerVariables(lexemasXinstruccion[0])
                print(*variables_program)
                if not variables_program:
                    err = Error.Error(1,"Error inside [ ] in variables","Incomplete sintax","0004")
                    window['salida'].Update(err,text_color='red')
                else:
                    i = 0
                    for j in lexemasXinstruccion:
                        print(j,"\n")
                        err = AnalizarInstruccion(j,i)
                        if err != None:
                            window['salida'].Update(err,text_color='red')
                            break
                        i+=1

                    if err == None:
                        window['salida'].Update('Compiled succesfully!\n',text_color='lime green')    
        elif event == 'EJECUTAR' or event == 'e:69':
            print ("output...",output)
            window['salida'].Update(output)
        elif event == 'L:76' or event == 'l:76':
            window['CODE'].Update('')
        elif event == 'j:74' or event == 'J:74':
            plantilla = "variables [ tipo_dato dato ]\nCODE....\nEND PROGRAM"
            window['CODE'].Update(plantilla)
        elif event == 'About':
            window.disappear()
            sg.popup('About JOKEN', 'Version beta',
                    'Proyecto final del curso paradigmas de programación 2022\nProfesor: Josias Chavez\nAlumnos:Kendall Marino Granados Barrantes y Josué Retana Cespedes',  grab_anywhere=True)
            window.reappear()
        elif event in Joken_reserv:
            window['CODE'].Update(values['CODE']+event)
        elif event == 'funciones':
            window['CODE'].Update(values['CODE']+"\nfun identifier [ params ]\n;")
        elif event == 'simple' or event == 'compuesto':
            cod = "if "
            if event == 'compuesto':
                cod +=  "[ if_true , condition , else ]"
            else:
                cod +=  "[ if_true , condition ]"
            window['CODE'].Update(values['CODE']+cod)
        elif event == 'FOR':
            window['CODE'].Update(values['CODE']+"\nFOR [ ejecuta ; inicializa_iterador , condition , modifica_iterador ]")
        elif event == 'WHILE':
            window['CODE'].Update(values['CODE']+"\nWHILE [ ejecuta , condition ]")
        elif event.upper() in Joken_tipos:
            window['CODE'].Update(values['CODE']+event)
    window.close()
if __name__ == '__main__':
    sg.theme('Dark')
    main()