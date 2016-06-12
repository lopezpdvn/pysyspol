from random import SystemRandom
from string import ascii_letters, digits

ALPHA_NUMERIC_STR = ascii_letters + digits

sys_random = SystemRandom()

def random_alphanumeric_str(n):
    return ''.join((sys_random.choice(ALPHA_NUMERIC_STR) for i in range(n)))
