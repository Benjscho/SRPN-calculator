from collections import deque

# Initialise global stack
main_stack = deque(maxlen=23)

def parse(arguments):
    '''
        This function iterates through the operands in each statement and
        performs the functions accordingly.
    '''
    legal_operators = ['+', '-', '*', '/', '%', '^']
    special_operators = ['=','#','d','r']
    for i in arguments:
        try:
            # If value is an integer push to the stack
            val: int = int(i)
            if len(main_stack) < main_stack.maxlen:
                main_stack.append(val)
            else:
                print("Stack overflow.")
        except ValueError:
            pass

        if i in legal_operators:
            if len(main_stack) > 1:
                val1 = main_stack.pop()
                val2 = main_stack.pop()
                operands(val1, val2, i)
            else:
                print("Stack underflow.")
        if i == '=':
            try:
                print(main_stack[-1])
            except:
                print("Stack empty.")
        if i == 'd':
            for i in main_stack:
                print(i)


def operands(val1, val2, operator):
    if operator == '^':
        result = pow(val2, val1)
        if result > 2147483647:
            result = 2147483647
        elif result < -2147483648:
            result = -2147483648
        main_stack.append(result)
    else:
        expression = str(val2) + operator + str(val1)
        try:
            result = int(eval(expression))
            if result > 2147483647:
                result = 2147483647
            elif result < -2147483648:
                result = -2147483648
            main_stack.append(result)
        except ZeroDivisionError:
            print("Divide by 0.")
            main_stack.append(val2)
            main_stack.append(val1)


def main():
    print("You can now start interacting with the SRPN calculator")
    while True:
        input_to_parse = input()
        process = input_to_parse.split()
        parse(process)

main()
