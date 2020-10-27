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

def exceptional_parse(i):
    '''
        Define an exceptional parse function for items that aren't covered
        by the typical parse where input is split by whitespace. This parses
        input character by character.
    '''
    temp_exp = []
    temp_num = ""
    for j in list(i):
        if j.isdigit():
            temp_num += j
        else:
            if temp_num != "":
                temp_exp.append(temp_num)
                temp_num = ""
            try:
                temp_result = int(eval(''.join(temp_exp)))
                temp_exp = []
                temp_exp.append(str(temp_result))
            except:
                pass
            if j != " ":
                temp_exp.append(j)
    if temp_num != "":
        temp_exp.append(temp_num)
    try:
        temp_result = int(eval(''.join(temp_exp)))
        temp_exp = []
        temp_exp.append(str(temp_result))
    except:
        pass
    return temp_exp

def parse(element):
    '''
        This function iterates through the operands in each statement and
        performs the functions accordingly.
    '''
    legal_operators = ['+', '-', '*', '/', '%', '**']
    global comment_flag

    # If comment symbol received switch comment flag and skip input until
    # the next comment symbol is received.
    if element == '#':
        comment_flag = not comment_flag
        return 0
    if comment_flag == True:
        return 0

    # Replace '^' with '**'. This is so powers are parsed properly
    if '^' in element:
        element = element.replace("^","**")

    # If value is an integer push to the stack, otherwise pass
    try:
        val: int = int(element)
        push_to_stack(val)
        return 0
    except ValueError:
        pass

    # If value is an expression push result to the stack, else pass
    try:
        val: int = eval(element)
        push_to_stack(val)
        return 0
    except:
        pass

    # If value is in the legal operators check if there are sufficient
    # values on the stack then pop those and apply operand function
    if element in legal_operators:
        if len(main_stack) > 1:
            val1 = main_stack.pop()
            val2 = main_stack.pop()
            operands(val1, val2, element)
        else:
            print("Stack underflow.")
        return 0

    # Parse '=' to print the last number from the stack without removing it.
    elif element == '=':
        try:
            print(main_stack[-1])
        except:
            print("Stack empty.")
        return 0

    # Parse 'd' to print the stack in order.
    elif element == 'd':
        for element in main_stack:
            print(element)
        return 0

    # Parse 'r' to push random number on stack. Potentially update this
    # so it gets the same numbers as from rand() in c++ that the old sprn
    # appears to have.
    elif element == 'r':
        r = randrange(2147483647)
        push_to_stack(r)
        return 0

    # If it's an illegal character print that
    elif len(element) == 1:
        print("Unrecognised operator or operand \"" + element + "\".")
        return 0

    # If none of the above could parse the element, return an error flag.
    else:
        return 1

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


def main():
    '''
        The main function starts the calculator then while it is running
        accepts input. The input is split by whitespaces, the parser then
        attempts to parse each element. If the parser can parse that element
        it will return 0. If it gets to the end and the parser cannot parse
        the element it is likely that there is no whitespace and it is a
        complicated expression. That element is then passed to the exceptional
        parser which returns an array of elements split based on conditions
        that mimic the behaviour of the srpn.
    '''
    print("You can now start interacting with the SRPN calculator")
    while True:

        input_to_parse = input()
        split_input = input_to_parse.split()
        for element in split_input:

            result = parse(element)
            if result == 1:
                secondary_input = exceptional_parse(element)
                for element in secondary_input:
                    parse(element)


main()

