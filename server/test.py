import string
digs = string.digits + string.ascii_letters
print(digs)

def decimal_to_base15(number):
    if number == 0:
        return "0"
    digits = []
    while number > 0:
        number, remainder = divmod(number, 15)
        digits.append(str(remainder))
    digits.reverse()
    return "".join(digits)

print(decimal_to_base15(12345))