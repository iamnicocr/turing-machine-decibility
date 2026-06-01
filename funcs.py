BLK = '_'
def loadTm(pathTm):
    with open(pathTm, 'r', encoding='utf-8') as fileTm:
        lines = [line.strip() for line in fileTm if line.strip() != '']
    tm = {
        'states': [],
        'inAlpha': [],
        'tapeAlpha': [],
        'start': '',
        'accept': '',
        'reject': '',
        'delta': {}
    }
    enTrans = False
    for line in lines:
        if line == 'transitions:':
            enTrans = True
            continue
        if not enTrans:
            if line.startswith('states:'):
                tm['states'] = line.split(':', 1)[1].strip().split()
            elif line.startswith('input_alphabet:'):
                tm['inAlpha'] = line.split(':', 1)[1].strip().split()
            elif line.startswith('tape_alphabet:'):
                tm['tapeAlpha'] = line.split(':', 1)[1].strip().split()
            elif line.startswith('start:'):
                tm['start'] = line.split(':', 1)[1].strip()
            elif line.startswith('accept:'):
                tm['accept'] = line.split(':', 1)[1].strip()
            elif line.startswith('reject:'):
                tm['reject'] = line.split(':', 1)[1].strip()
        else:
            partes = line.split()
            if len(partes) != 6 or partes[2] != '->':
                raise ValueError('Transicion invalida: ' + line)
            stAct = partes[0]
            symAct = partes[1]
            stNew = partes[3]
            symNew = partes[4]
            mov = partes[5]
            if mov not in ['L', 'R', 'S']:
                raise ValueError('Movimiento invalido: ' + mov)
            if stAct not in tm['delta']:
                tm['delta'][stAct] = {}
            tm['delta'][stAct][symAct] = (stNew, symNew, mov)
    reqs = ['states', 'inAlpha', 'tapeAlpha', 'start', 'accept', 'reject']
    for key in reqs:
        if tm[key] == [] or tm[key] == '':
            raise ValueError('Falta campo en TM: ' + key)
    return tm

def initTape(inp):
    tape = list(inp) if inp != '' else [BLK]
    return tape

def getSym(tape, head):
    if head < 0 or head >= len(tape):
        return BLK
    return tape[head]

def setSym(tape, head, sym):
    if head < 0:
        falt = abs(head)
        tape[:0] = [BLK] * falt
        head = 0
    if head >= len(tape):
        tape.extend([BLK] * (head - len(tape) + 1))
    tape[head] = sym
    return head

def trimTape(tape, head):
    while len(tape) > 1 and tape[-1] == BLK and head < len(tape) - 1:
        tape.pop()
    return tape, head

def tapeTxt(tape):
    return ''.join(tape)

def confTxt(tape, head, stAct):
    tapeTxtAct = ''.join(tape)
    if head < 0:
        pref = BLK * abs(head)
        tapeTxtAct = pref + tapeTxtAct
        head = 0
    if head >= len(tapeTxtAct):
        tapeTxtAct = tapeTxtAct + (BLK * (head - len(tapeTxtAct) + 1))
    return tapeTxtAct[:head] + stAct + tapeTxtAct[head:]

def headMark(tape, head, stAct):
    tapeTxtAct = ''.join(tape)
    if head < 0:
        tapeTxtAct = (BLK * abs(head)) + tapeTxtAct
        head = 0
    if head >= len(tapeTxtAct):
        tapeTxtAct = tapeTxtAct + (BLK * (head - len(tapeTxtAct) + 1))
    return ' ' * (head + len(stAct)) + '^'

def stepTm(tm, tape, head, stAct):
    if stAct == tm['accept']:
        return tape, head, stAct, 'ACCEPT', 'halt_accept'
    if stAct == tm['reject']:
        return tape, head, stAct, 'REJECT', 'halt_reject'
    symAct = getSym(tape, head)
    if stAct not in tm['delta'] or symAct not in tm['delta'][stAct]:
        return tape, head, tm['reject'], 'REJECT', 'undefined'
    stNew, symNew, mov = tm['delta'][stAct][symAct]
    head = setSym(tape, head, symNew)
    if mov == 'R':
        head += 1
    elif mov == 'L':
        head -= 1
    tape, head = trimTape(tape, head)
    if stNew == tm['accept']:
        return tape, head, stNew, 'ACCEPT', f'{stAct} {symAct} -> {stNew} {symNew} {mov}'
    if stNew == tm['reject']:
        return tape, head, stNew, 'REJECT', f'{stAct} {symAct} -> {stNew} {symNew} {mov}'
    return tape, head, stNew, 'RUN', f'{stAct} {symAct} -> {stNew} {symNew} {mov}'

def run(tm, inp, max_steps):
    tape = initTape(inp)
    head = 0
    stAct = tm['start']
    steps = 0
    while steps <= max_steps:
        tape, head, stAct, stat, _ = stepTm(tm, tape, head, stAct)
        if stat in ['ACCEPT', 'REJECT']:
            return stat
        steps += 1
    return 'TIMEOUT'

def runTrace(tm, inp, max_steps):
    tape = initTape(inp)
    head = 0
    stAct = tm['start']
    trace = []
    trace.append({
        'step': 0,
        'conf': confTxt(tape, head, stAct),
        'tape': tapeTxt(tape),
        'head': headMark(tape, head, stAct),
        'rule': 'start'
    })
    step = 0
    while step < max_steps:
        tape, head, stAct, stat, rule = stepTm(tm, tape, head, stAct)
        step += 1
        trace.append({
            'step': step,
            'conf': confTxt(tape, head, stAct),
            'tape': tapeTxt(tape),
            'head': headMark(tape, head, stAct),
            'rule': rule
        })
        if stat in ['ACCEPT', 'REJECT']:
            return stat, trace, tapeTxt(tape)
    return 'TIMEOUT', trace, tapeTxt(tape)

def showTrace(trace):
    for row in trace:
        print(f"Paso {row['step']}: {row['conf']}")
        print(row['tape'])
        print(row['head'])
        print('Regla:', row['rule'])
        print()

def tmTxt(tm):
    out = []
    out.append('states: ' + ' '.join(tm['states']))
    out.append('input_alphabet: ' + ' '.join(tm['inAlpha']))
    out.append('tape_alphabet: ' + ' '.join(tm['tapeAlpha']))
    out.append('start: ' + tm['start'])
    out.append('accept: ' + tm['accept'])
    out.append('reject: ' + tm['reject'])
    out.append('transitions:')
    for stAct in tm['delta']:
        for symAct in tm['delta'][stAct]:
            stNew, symNew, mov = tm['delta'][stAct][symAct]
            out.append(f'{stAct} {symAct} -> {stNew} {symNew} {mov}')
    return '\n'.join(out)

def leeInp():
    inp = input('Input (use eps cuando vacia): ').strip()
    if inp.lower() == 'eps':
        return ''
    return inp

def leeMaxSteps():
    txt = input('max_steps: ').strip()
    if txt == '':
        return 200
    return int(txt)
