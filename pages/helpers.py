import random
import string

def random_code_generator(string_size=5):
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=string_size)
    )
