import re

temp_count = 0

def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"

def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

def to_postfix(expression):
    stack = []
    output = []

    tokens = re.findall(r'\d+|[a-zA-Z]+|[+\-*/=()]', expression)

    for token in tokens:
        if token.isalnum():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()
        else:
            while stack and precedence(stack[-1]) >= precedence(token):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return output


def generate_code(postfix):
    stack = []
    code = []

    for token in postfix:
        if token.isalnum():
            stack.append(token)
        else:
            right = stack.pop()
            left = stack.pop()

            # Constant folding
            if left.isdigit() and right.isdigit():
                if token == '+':
                    result = int(left) + int(right)
                elif token == '-':
                    result = int(left) - int(right)
                elif token == '*':
                    result = int(left) * int(right)
                elif token == '/':
                    result = int(left) // int(right)

                stack.append(str(result))
            else:
                temp = new_temp()
                code.append(f"{temp} = {left} {token} {right}")
                stack.append(temp)

    return code, stack[-1]


def compile_expr(expr):
    global temp_count
    temp_count = 0

    if '=' not in expr:
        print("Invalid format. Use: a = 5 + 3")
        return []

    var, expression = expr.split('=')
    var = var.strip()

    postfix = to_postfix(expression)
    code, result = generate_code(postfix)

    code.append(f"{var} = {result}")
    return code


if __name__ == "__main__":
    print("Mini Compiler Started")
    print("Type expressions like: a = 5 + 3 * 2")
    print("Supports parentheses and constant folding")
    print("Type 'exit' to quit\n")

    while True:
        expr = input("Enter expression: ")

        if expr.lower() == "exit":
            print("Exiting compiler...")
            break

        try:
            result = compile_expr(expr)

            if result:
                print("\nGenerated 3-Address Code:")
                for line in result:
                    print(line)
                print("-" * 30)

        except Exception:
            print("Invalid expression. Try again.")