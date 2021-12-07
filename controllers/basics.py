import random
from warnings import resetwarnings

def is_prime(number):
    counter = 2
    while counter < number-1:
        if number%counter==0:
            return False
        counter = counter + 1
    return True

def random_number():
    x = random.randint(3,20)
    result = is_prime(x)
    return locals()

def request_args():
    arg1 = float(request.args(0))
    arg2 = float(request.args(1))
    total = arg1 + arg2
    return locals()

def request_vars():
    number1 = 0
    number2 = 0
    number3 = 0
    total = 0
    if request.post_vars:
        number1 = float(request.post_vars.number1)
        number2 = float(request.post_vars.number2)
        number3 = float(request.post_vars.number3)
        total = number1 + number2 + number3
        response.flash = T("Total is: " + str(total))
    return locals()

def helloworld():
    msg = "Hello Ali from the new controller!!"
    return locals()

def index(): return dict(message="hello from basics.py")
