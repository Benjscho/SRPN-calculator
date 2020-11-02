from collections import deque
from random import randrange

# Initialise global stack
main_stack = deque(maxlen=23)


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

def exceptional_parse(input_to_parse):
    '''
        Define an exceptional parse function for items that aren't covered
        by the typical parse where input is split by whitespace. This parses
        input character by character to build up a split expression that
        will be parsed.

        When input is not space separated, The parse order of the version to
        emulate runs:
        1) If it's a number, push it to the stack
        2) If it's a mathematical operator, perform them in reverse input order
        3) If it's a legal special operator perform it
        4) If it's anything else print the rejection message.

        In my best emulation of this, when there is no whitespace, this program
        iterates through character by character. If it is a number it adds it
        to the temporary numbers, and if there is an operator that is also
    '''
    legal_operators = ['+', '-', '*', '/', '%', '^']

    # Initialise temporary holders for numbers, and operators.
    # and a temporary operator.
    temp_nums = []
    temp_ops = []
    temp_number = ""

    # Iterate through characters in the input
    for j in list(input_to_parse):

        # If the character is a digit, concatenate with temporary number
        if j.isdigit():
            temp_number += j
        else:
            # End of the number has been reached, so append to numbers.
            if temp_number != "":
                temp_nums.append(temp_number)
                temp_number = ""
            if j in legal_operators:
                temp_ops.append(j)
            elif j != " ":
                parse(j)

    if temp_number != "":
        temp_nums.append(temp_number)

    temp_exp = temp_nums + temp_ops[::-1]
    return temp_exp

def parse(element):
    '''
        This function iterates through the operands in each statement and
        performs the functions accordingly.
    '''
    legal_operators = ['+', '-', '*', '/', '%', '^']


    # Check if number is octal, if so, convert from octal to int and continue
    '''
        This check is slightly ugly so it requires explanation. First
        the code checks if this element is flagged as an octal. Numbers are
        flagged as octal by the prefix '0'. If a number is prefixed '0' it is
        parsed as an octal. In order to do that the element is split into a
        list, checks if that list has more than two elements, then checks if
        the first element is a 0, or if the first two elements are -0, if so
        it tries to convert the element from a string to an octal.

        The difficulty is bad octals e.g., 09, are ignored by the sprn. So
        to mimic that behaviour, if an exception is thrown by the octal, but
        it could be parsed as a regular int the parse function exits with a 1
        error.

    '''
    octal_check = list(element)
    if len(octal_check) > 1:
        octal_bools = [\
            (octal_check[0] == '0'),\
            (octal_check[0] == '-' and octal_check[1] == '0')]

        if (octal_bools[0] or octal_bools[1]):
            try:
                element = int(element, 8)
            except:
                try:
                    int(element)
                    return 1
                except:
                    pass

    # If value is an integer push to the stack, otherwise pass
    try:
        val: int = int(element)
        push_to_stack(val)
        return 0
    except ValueError:
        pass


    # If value is in the legal operators check if there are sufficient
    # values on the stack then pop those and apply operand function
    if element in legal_operators:
        # Replace '^' with '**'. This is so powers are parsed properly
        # additionally ensure that the top of the stack is positive to show
        # an error if a negative power is called.
        if '^' in element:
            element = element.replace("^","**")
            try:
                assert main_stack[-1] >= 1
            except:
                print("Negative power.")
                return 0
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
        if len(main_stack) == 0:
            print(-2147483648)
            return 0
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
        it will return 0.

        If it gets to the end and the parser cannot parse the element it is
        likely that there is no whitespace and it is a complicated expression.
        That element is then passed to the exceptional parser which returns an
        array of elements split based on conditions that mimic the behaviour of
        the srpn.

        The comment flag is interpreted outside of the parse function due to
        behaviour found when inputs such as '#2' or '#2' are input.
    '''
    comment_flag = False
    print("You can now start interacting with the SRPN calculator")
    while True:

        input_to_parse = input()
        split_input = input_to_parse.split()
        for element in split_input:

            # If comment symbol received switch comment flag and skip input until
            # the next comment symbol is received. Stop processing for '#' element.
            if element == '#':
                comment_flag = not comment_flag
                continue
            if comment_flag == True:
                break

            # Call the parse statement on the element and get the return value.
            # If the return value is 1 it means the expression needs to be
            # split by the exceptional parser, before being run through parse
            # again.
            result = parse(element)
            if result == 1:
                secondary_input = exceptional_parse(element)
                for element in secondary_input:
                    parse(element)


# Finally call the main function to run the program and start the calculator
if __name__ == "__main__":
    main()

