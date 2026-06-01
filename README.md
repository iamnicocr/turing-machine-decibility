# Principios de sistemas computacionales 2026-1
# CA3 - Toolkit Turing Machine Simulator

Proyecto en Python para simular una maquina de turing con trazos paso a paso.
Realizado por Nicolas Carrillo R.

## Archivos del .zip
- `main.py`: menu principal.
- `funcs.py`: carga de TM, simulacion paso a paso, trace y utilidades.
- `tm_1.txt`: decider para `{0^n1^n | n >= 0}`.
- `tm_2.txt`: decider para `{w#w | w in {0,1}*}`.
- `tm_3.txt`: TM que deja `1^(n+1)` en cinta.
- `tests.txt`: casos de prueba planteados.
- `informe.docx`: informe editable.

## Cómo correr
En la carpeta del proyecto, click derecho -> Powershell/Open in terminal. 
Digite el siguiente comando y el proyecto se ejecutara en su totalidad:
```bash
python main.py
```

## Uso
1. Cargar una TM desde archivo.
2. Ver la TM cargada.
3. Correr una entrada con `max_steps`.
4. Correr una entrada con trace.

Para la cadena vacia usar `eps`.

## Formato del archivo TM
El formato aceptado por el programa sigue y se asimila al enunciado:

```txt
states: q0 q1 qaccept qreject
input_alphabet: 0 1
tape_alphabet: 0 1 _
start: q0
accept: qaccept
reject: qreject
transitions:
q0 0 -> q1 X R
q1 1 -> qaccept 1 R
```
## Nota
Para la carga del archivo, basta con digitar el nombre del archivo despues de digitar la opcion en el menu, es decir, si quiero ejecutar `tm_w_hash_w.txt` basta con digitar 1 en el menu principal y luego el mismo archivo `tm_w_hash_w.txt`, el programa lo leera correctamente.