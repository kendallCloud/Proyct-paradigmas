import PySimpleGUI as sg
import ArbolDlexemas as Arbol
import Error


#variables globales

Palabras_reservadas = Arbol.AVLTree()

Joken_reserv = ["IF","ELSE","WHILE","FOR","STRING","FLOAT","INT","BOOL","VARIABLES","END","BEGIN"]
for i in Joken_reserv:
    Palabras_reservadas.insert(i)

instrucciones = []
lexemasXinstruccion = []

def separa_Instrucciones(codigo):
    return codigo.split('\n')

def ComposicionLexica(codigo):
    return codigo.split(' ')

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
      [[sg.Multiline(size=(45,10), expand_x=True, expand_y=True, k='salida')]]]
    layout[-1].append(sg.Sizegrip()) 
    window = sg.Window('J Retana k granados',layout,margins=(75,100),resizable=True)
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
    print("utima_fila ",ultima_fila)
    err=None
    if mat[ultima_fila][0].upper() != "END":
        err = Error.Error(ultima_fila,"Joken program must be ended whith END whithout exception","imcomplete program sintax","0001")
    return err


def main():
    
    window = make_window()
    while True:
        event, values = window.read()
    # End program if user closes window
        if event == sg.WIN_CLOSED: 
            break
        elif event == 'COMPILAR':
            instrucciones = separa_Instrucciones(values['CODE'])
            lexemasXinstruccion = list(map(ComposicionLexica,instrucciones))#separa cada instrucción en un array de lexemas
            lexemasXinstruccion = LimpiarCodigo(lexemasXinstruccion)# elimina espacios en blanco o muertos
            err = SintaxisBasica(lexemasXinstruccion)
            if SintaxisBasica(lexemasXinstruccion) != None:
                print ("hay errores")
                window['salida'].Update(err,text_color='red')
            else:
                window['salida'].Update('Compiled succesfully!',text_color='green')

            for i in lexemasXinstruccion:
                print("\n",i)

    window.close()

if __name__ == '__main__':
    sg.theme('SystemDefault')
    main()