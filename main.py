from funcs import loadTm, run, runTrace, showTrace, tmTxt, leeInp, leeMaxSteps


def showMenu():
    print('\n=== Simulador de Maquina de Turing ===')
    print('1. Cargar TM desde archivo')
    print('2. Ver TM cargada')
    print('3. Correr TM')
    print('4. Correr TM con trace')
    print('5. Salir')


def main():
    tmAct = None
    pathAct = ''
    while True:
        showMenu()
        opc = input('Opcion: ').strip()
        if opc == '1':
            pathTm = input('Ruta del archivo TM: ').strip()
            try:
                tmAct = loadTm(pathTm)
                pathAct = pathTm
                print('TM cargada bien desde', pathTm)
            except Exception as err:
                print('Error cargando TM:', err)
        elif opc == '2':
            if tmAct is None:
                print('Primero cargue una TM.')
                continue
            print('Archivo:', pathAct)
            print(tmTxt(tmAct))
        elif opc == '3':
            if tmAct is None:
                print('Primero cargue una TM.')
                continue
            inp = leeInp()
            maxSteps = leeMaxSteps()
            res = run(tmAct, inp, maxSteps)
            print('Resultado:', res)
        elif opc == '4':
            if tmAct is None:
                print('Primero cargue una TM.')
                continue
            inp = leeInp()
            maxSteps = leeMaxSteps()
            res, trace, tapeFin = runTrace(tmAct, inp, maxSteps)
            showTrace(trace)
            print('Resultado:', res)
            print('Tape final:', tapeFin)
        elif opc == '5':
            print('Saliendo.')
            break
        else:
            print('Opcion invalida.')


if __name__ == '__main__':
    main()
