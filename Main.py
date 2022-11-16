import PySimpleGUI as sg
import ArbolDlexemas as Arbol
import Error
import keyboard

#variables globales
output = ""

joken_log = ["EQUAL","<",">","<=",">=","AND","OR","!="]

Palabras_reservadas = Arbol.AVLTree()

Joken_reserv = ["IF","ELSE","WHILE","FOR","VARIABLES","END","PRINT"]
for i in Joken_reserv:
    Palabras_reservadas.insert(i)

instrucciones = []
lexemasXinstruccion = []
#----------------------------------------------------------------------------
class Variable:
  def __init__(self, identifier,data_type,valor):
        self.data_type = data_type
        self.valor = valor
        self.identifier = identifier
  def __str__(self):
    return f"{self.identifier}//{self.data_type}//{self.valor}"

Joken_types = Arbol.AVLTree()
variables_program = []

Joken_tipos = ["STRING","FLOAT","INT","BOOL","NULL","ARRAY","LIST"]
for i in Joken_tipos:
    Joken_types.insert(i)

def separa_Instrucciones(codigo):
    return codigo.split('\n')

def ComposicionLexica(codigo):
    return codigo.split(' ')

def redo(event, text):
    try:    # if nothing to redo will cause "_tkinter.TclError: nothing to redo"
        text.edit_redo()
    except:
        pass

def make_window():
    menu_def = [['&Nuevo', []],
                ['&opciones', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Salir', ['---', 'Command &1', 'Command &2',
                              '---', 'Command &3', 'Command &4']]]
    right_click_menu_def = [[], ['Edit Me', 'Versions', 'Nothing','More Nothing','Exit']]
    graph_right_click_menu_def = [[], ['Erase','Draw Line', 'Draw',['Circle', 'Rectangle', 'Image'], 'Exit']]

    layout = [ [sg.Menu(menu_def, key='-MENU-', font='Courier 15', tearoff=True)] 
    ,[sg.Text('---------------------------------------------------CODE-------------------------------------------', justification='top', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='-TEXT HEADING-', enable_events=False)],
    [[sg.Button('COMPILAR'),sg.Button('EJECUTAR')],  [sg.Multiline(size=(45,15), expand_x=True, expand_y=True, k='CODE')]],
    [sg.Text('-----------------------------------------------OUTPUT----------------------------------------', justification='top', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='OUTPUT')],
      [[sg.Multiline(size=(45,10), expand_x=True, expand_y=True, k='salida',disabled=True)]]]
    layout[-1].append(sg.Sizegrip()) 
    window = sg.Window('J Retana k granados JOKEN',layout,margins=(85,100),resizable=True,return_keyboard_events=True)
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

def LeerVariables(instruct):
    if instruct[1] == '[' and instruct[-1] == ']' and  len(instruct) > 3:
        index = 2
        while index < len(instruct)-1:
            if IsVarType(instruct[index]) and not IsReservada(instruct[index+1]) and not IsVarType(instruct[index+1]):
                variables_program.append(Variable(instruct[index+1],instruct[index],None))
            index+=2

def IsCondicional(instruct):
    return instruct[0] == "IF" or instruct[0] == "if" or instruct[0] == "If" or instruct[0] == "iF"

def AsignarValue(identifier,valor):
    global variables_program
    for i in range(len(variables_program)):
        if variables_program[i].identifier == identifier:
            variables_program[i].valor = valor
            variables_program[i].data_type = type(valor)
            print("valor asignado")

def IsAsignacion(instruct):
    return IsVariable(instruct[0]) and instruct[1] == '='

def GetVariable(identifier):
    objeto = None
    for k in variables_program:
        if k.identifier == identifier:
            objeto = k
    return objeto

def joken_print(instruct):
    global output
    for i in instruct:
        if IsVariable(i):
            variable = GetVariable(i)
            output += variable.valor + '\n'
        else:
            output += i + ' '
    print("joken_print...",output)

def Resultado_Condicion(cond_array):
    v1 = None
    v2 = None
    if IsVariable(cond_array[0]):
        v1 = GetVariable(cond_array[0])
    elif cond_array[0].isnumeric():
        v1 = Variable("",type(int),int(cond_array[0]))
    elif cond_array[0].upper() == "TRUE":
        v1 = Variable("",type(bool),True)
    elif cond_array[0].upper() == "FALSE":
        v1 = Variable("",type(bool),False)

    if IsVariable(cond_array[2]):
        v2 = GetVariable(cond_array[2])
    elif cond_array[2].isnumeric():
        v2 = Variable("",type(int),int(cond_array[2]))    

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
    elif isinstance(v2.valor,None) and isinstance(v1.valor,None): 
        return True
""""
def Findoperator_logico(instruct):
    i = 0
    for i in instruct:
        if i in joken_log and i:
            i+=1
"""    
def AnalizarInstruccion(instruct,j):
    print('analizando linea ',j)
    if(IsCondicional(instruct)):
        if instruct[1] == "[" and instruct[-1] == ']':
            print('if correcto')
            comas = instruct.count(',')
            if comas == 1:#condicional simple
                salida = instruct[2:instruct.index(',')]# del inicio a la primera coma es la salida si se cumple la condicion
                condicion = instruct[instruct.index(',')+1:len(instruct)-1]
                verdad = Resultado_Condicion(condicion)
                print ('resultado ',verdad) 
                if verdad :
                    if salida[0] == 'print':
                        print ('es print')
                        if salida[1] != '(' or salida[-1] != ')':
                            return Error.Error(j,"error found on if condition","sintax error",'jk005')
                        joken_print(salida[2:len(salida)-1])

                return None
            elif comas == 2:# compuesto
                return None
            else:
                return Error.Error(j,"error found on if condition","sintax error",'jk005')
        else:
            return Error.Error(j,"error found on if condition","sintax error",'jk005')
    elif IsAsignacion(instruct):
        igual = instruct.index("=")
        val=None
        asignado = instruct[igual+1:len(instruct)]
        print ('asignando...',*asignado)
        if len(asignado) == 1 and asignado[0].isnumeric():#asigna un numero
            val = int(asignado[0])
        elif len(asignado) > 1 and asignado[0] == '"' and asignado[-1] == '"':#asigna string
            val = ' '.join(asignado)
            print("asigna string")
        elif len(asignado) == 1 and not asignado[0].isnumeric() and asignado[0].upper() == 'TRUE' or asignado[0].upper() == 'FALSE':
            val = asignado[0].upper() == 'TRUE'
        elif len(asignado) == 1 and asignado[0].upper() == 'NULL':
            val = None

        AsignarValue(instruct[0],val)

        print("Variables desp de asignar",*variables_program)    
        
        return None
    elif len(instruct) > 1 and instruct[1] == '(' or instruct[-1] == ')' and instruct[0] == 'print':
            joken_print(instruct[2:len(instruct)-1])
            #return Error.Error(j,"error found on print condition","sintax error",'jk005')

def main():
    
    window = make_window()
    while True:
        event, values = window.read()
        print(event)
    #End program if user closes window
        if event == sg.WIN_CLOSED: 
            break
        elif event == 'COMPILAR' or event == '\r' and values['CODE'] != "":
            #variables_program.clear()
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
                        err = AnalizarInstruccion(j,i)
                        if err != None:
                            window['salida'].Update(err,text_color='red')
                            break
                        i+=1

                    if err == None:
                        window['salida'].Update('Compiled succesfully!\n',text_color='green')    
                       #print("\n",j)
        elif event == 'EJECUTAR':
            print ("output...",output)
            window['salida'].Update(output)
        elif event == 'L:76' or event == 'l:76':
            window['CODE'].Update('')
        elif event == 'j:74' or event == 'J:74':
            plantilla = "variables [ tipo_dato dato ]\nCODIGO....\nEND PROGRAM"
            window['CODE'].Update(plantilla) 

    window.close()

if __name__ == '__main__':
    sg.theme('SystemDefault')
    main()