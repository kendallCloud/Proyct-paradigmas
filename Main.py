import PySimpleGUI as sg

#variables globales

instrucciones = []
lexemasXinstruccion = []
codigo=""

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
    [[sg.Button('COMPILAR'),sg.Button('EJECUTAR')],  [sg.Multiline('', size=(45,5), expand_x=True, expand_y=True, k='CODE')]],
    [sg.Text('-----------------------------------------------UOTPUT----------------------------------------', justification='top', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE, k='OUTPUT')],
      [[sg.Multiline(size=(45,5), expand_x=True, expand_y=True, k='salida')]]]
    layout[-1].append(sg.Sizegrip()) 
    window = sg.Window('J Retana k granados',layout,margins=(100,100),resizable=True)
    return window

def main():
    
    window = make_window()
    while True:
        event, values = window.read()
    # End program if user closes window
        if event == sg.WIN_CLOSED: 
            break
        elif event == 'COMPILAR':
            instrucciones = separa_Instrucciones(values['CODE'])
            lexemasXinstruccion = list(map(ComposicionLexica,instrucciones))
            print('instrucciones: ',instrucciones)
            print(lexemasXinstruccion)

    window.close()

if __name__ == '__main__':
    sg.theme('dark blue')
    main()