from sys import argv


ARRAY_LENGTH=30000
ARRAY=[0]*ARRAY_LENGTH
POINTER=0
LOOPS=[]
CONSOLE_INPUT=""
SKIPPING=False
IN_LOOP_CODE=[]
DEBUG=False
def eval_bf(code:str)->None:
    global ARRAY_LENGTH
    global ARRAY
    global POINTER
    global LOOPS
    global CONSOLE_INPUT
    global SKIPPING
    global DEBUG
    IN_LOOP_CODE=[]
    for character in code:
            if DEBUG:
                print(f"CHARACTER: {character}, SKIPPING: {SKIPPING}, POINTER: {POINTER}, LOOPS: {LOOPS}, INLOOPCODE: {IN_LOOP_CODE}")
                print(ARRAY[:10])
            if character=="[":
                if ARRAY[POINTER]==0:
                    SKIPPING=True
                else:
                    LOOPS.append(POINTER)
                    IN_LOOP_CODE.append("[")
            elif character=="]":
                if SKIPPING:
                    SKIPPING=False
                    continue
                elif ARRAY[POINTER]==0:
                    LOOPS.pop(-1)
                    IN_LOOP_CODE.pop(-1)
                    continue
                else:
                    POINTER=LOOPS[-1]
                    IN_LOOP_CODE[-1]=IN_LOOP_CODE[-1]+character
                    eval_bf(IN_LOOP_CODE[-1])
                    LOOPS.pop(-1)
                    IN_LOOP_CODE.pop(-1)
            elif SKIPPING:
                continue
            elif character=='>':
                if len(LOOPS)!=0:
                    IN_LOOP_CODE[-1]=IN_LOOP_CODE[-1]+character
                POINTER=POINTER+1
            elif character=='<':
                if len(LOOPS)!=0:
                    IN_LOOP_CODE[-1]=IN_LOOP_CODE[-1]+character
                if POINTER == 0:
                    pass
                POINTER=POINTER-1
            elif character=='+':
                if len(LOOPS)!=0:
                    IN_LOOP_CODE[-1]=IN_LOOP_CODE[-1]+character
                if ARRAY[POINTER] == 255:
                    ARRAY[POINTER]=0
                ARRAY[POINTER]=ARRAY[POINTER]+1
            elif character=='-':
                if len(LOOPS)!=0:
                    IN_LOOP_CODE[-1]=IN_LOOP_CODE[-1]+character
                if ARRAY[POINTER] == 0:
                    pass
                ARRAY[POINTER]=ARRAY[POINTER]-1
            elif character==',':
                if len(LOOPS)!=0:
                    IN_LOOP_CODE[-1]=IN_LOOP_CODE[-1]+character
                if len(CONSOLE_INPUT)==0:
                    CONSOLE_INPUT = input()
                    ARRAY[POINTER]=ord(CONSOLE_INPUT[0])
                    CONSOLE_INPUT=CONSOLE_INPUT[1:]
                else:
                    ARRAY[POINTER]=ord(CONSOLE_INPUT[0])
                    CONSOLE_INPUT=CONSOLE_INPUT[1:]
            elif character=='.':
                if len(LOOPS)!=0:
                    IN_LOOP_CODE[-1]=IN_LOOP_CODE[-1]+character
                print(chr(ARRAY[POINTER]),end="")
            else:
                pass
if __name__=="__main__":
    if len(argv)==1:
        while True:
            code = input("Please input brainfuck code:",)
            if code in ["q","quit"]:
                break
            eval_bf(code)
    else:
        with open(argv[1],'r') as f:
            file = f.read()
        eval_bf(file)
        