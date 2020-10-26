from collections import deque
import re
from random import randrange

# Initialise global stack and comment flag
main_stack = deque(maxlen=23)
comment_flag: bool = False


def overflow_check(value):
    '''
        This function provides a standin to check whether the value is within
        the int limits in the original sprn
    '''
    if value > 2147483647:
        value = 2147483647
    elif value < -2147483648:
        value = -2147483648
    return value

def push_to_stack(val):
    '''
        Checks if the stack is less than the max stack length, and if so
        pushes the value to the stack after checking for overflows.
    '''
    if len(main_stack) < main_stack.maxlen:
        main_stack.append(overflow_check(val))
    else:
        print("Stack overflow.")

def parse(arguments):
    '''
        This function iterates through the operands in each statement and
        performs the functions accordingly.
    '''
    legal_operators = ['+', '-', '*', '/', '%', '^']
    special_operators = ['=','#','d','r']
    global comment_flag
    for i in arguments:
        # If comment symbol received switch comment flag and skip input until
        # the next comment symbol is received.
        if i == '#':
            comment_flag = not comment_flag

        if comment_flag == True:
            break

        try:
            # If value is an integer push to the stack
            val: int = int(i)
            push_to_stack(val)
        except ValueError:
            pass

        try:
            val: int = eval(i)
            push_to_stack(val)
        except:
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
        if i == 'r':
            r = randrange(2147483647)
            push_to_stack(r)


def operands(val1, val2, operator):
    '''
        This function takes two values popped from the stack, and seeks to
        perform the function indicated by the operator on them. It then pushes
        the result of that operation back onto the stack.
    '''
    # Exceptional case for power operator to call pow function.
    if operator == '^':
        result = pow(val2, val1)
        push_to_stack(result)
    else:
        expression = str(val2) + operator + str(val1)
        try:
            result = int(eval(expression))
            push_to_stack(result)
        except ZeroDivisionError:
            print("Divide by 0.")
            main_stack.append(val2)
            main_stack.append(val1)

def split_by_regex(parse_string):
        # regex to parse mathematical expressions taken from
        # https://stackoverflow.com/questions/3373885/splitting-a-simple-maths-expression-with-regex#3377362
        # and edited to meet needs in this instance.
    regex = "(?<=op)|(?=op)".replace("op", "[-+*^/%]")

    process = re.split(regex, parse_string)

    return process

def main():
    print("You can now start interacting with the SRPN calculator")
    while True:
        input_to_parse = input()
        '''
        try:
            process = eval(input_to_parse)
        except:
            process = split_by_regex(input_to_parse)
        print(process)
        '''
        process = input_to_parse.split()
        parse(process)


main()

