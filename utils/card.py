import random
from my_account.models import Card

def generate_card_number():
    number = [random.randint(0, 9) for _ in range(15)]
    check_digit = get_check_digit(number)
    return ''.join(map(str, number)) + str(check_digit)

def get_check_digit(number):
    # Luhn algorithm to calculate check digit
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    # Ensure 'number' is treated as a single integer, not a list of integers
    number_str = ''.join(map(str, number))
    digits = digits_of(number_str)
    
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    
    for d in even_digits:
        total += sum(digits_of(d * 2))
    
    return (10 - (total % 10)) % 10

def generate_unique_card_number():
    while True:
        card_number = generate_card_number()
        if not Card.objects.filter(card_number=card_number).exists():
            return card_number


