from collections import deque

# Initialise global stack
main_stack = deque(maxlen=23)

def parse(arguments):
    '''
        This function iterates through the operands in each statement and
        performs the functions accordingly.
    '''
    legal_operators = ['+', '-', '*', '^', '/', '%']
    special_operators = ['=','#','d','r']
    for i in arguments:
        try:
            # If value is an integer push to the stack
            val = int(i)
            if len(main_stack) < main_stack.maxlen:
                main_stack.append(val)
            else:
                print("Stack overflow.")
        except ValueError:
            pass

        if i in legal_operators:
            operands(i)
        if i == '=':
            print(main_stack[-1])
        if i == 'd':
            for i in main_stack:
                print(i)


def operands(operator):
    val1 = main_stack.pop()
    val2 = main_stack.pop()
    expression = str(val2) + operator + str(val1)
    main_stack.append(eval(expression))



def main():
    print("You can now start interacting with the SRPN calculator")
    while True:
        input_to_parse = input()
        process = input_to_parse.split()
        parse(process)

main()
