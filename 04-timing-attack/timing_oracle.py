def timing_oracle(password_guess):
    with open('password.txt') as f:
        lines = f.readlines()

    password_correct = (lines[0])
    len_password_correct = len(password_correct)
    len_password_guess = len(password_guess)
    compare_correct = 0

    timing = len_password_correct

    for i in range(len(password_guess)):
        if(password_guess[i] == password_correct[i]):
            compare_correct = compare_correct + 1
        else: 
            timing = i
            break 
    
    success_or_not = 0

    if(timing == len_password_correct):
        if(compare_correct == (len_password_correct)):
            success_or_not = 1

    return success_or_not, timing
