#Luhn algorithm

card_no = input("Enter your credit card number: ")
card = card_no.replace(" ","") #to remove spaces

# this condition checks that the card should consist of 16 numbers and only digits.
if len(card) >= 16 and card.isdigit():

    # to print the original card number by converting it into masked card.
    check_digit = card[-1]
    mask_card = card[:-1] + "X"
    print(mask_card)

    # reverse the card number by using reverse slicing
    reverse_card = card[::-1]
    print("Reversed card number:", reverse_card)

    # to calculate and print double digits so later this will be use for the sum of double digits.
    double_digits = []
    for i in range(1, len(reverse_card)):  
        digit = int(reverse_card[i])
        if i % 2 == 1:
            double_digit = digit * 2
            if double_digit > 9:
                double_digit -= 9
            double_digits.append(double_digit)
        else:
            double_digits.append(digit)
    print("Doubled digits:", double_digits)

    # to find the total sum of the card that consist of the sum of double digits and the index number of the reverse card
    total_sum = sum(double_digits) + int(reverse_card[0])
    print("Total sum:", total_sum)

    # this condition is used if the total sum is divisible by 10 or not in order to check the card validation.
    if total_sum % 10 == 0:
        print("The credit card number is valid!")
    else:
        print("The credit card number is invalid!")
else:
    print("Invalid input! Please enter a valid credit card number that consist of only 16 digits.")