
#TODO : automate 
def calculate_string_effort(p, politque, n_special ,n_digit,n_specials):
    output=[]
    k=0
    
    for policy in politiques:
        components = policy.split()
        
        #UPDATE l
        #UPDATE k
        
        output.append((policy, L))
    
    return output


def estimate_effort(string_list, digit_list, special_list):
    n_string = len(string_list)
    n_digit = len(digit_list)
    n_special = len(special_list)
    politiques = ['string digit', 
                  'string', 'digit', 
                  'digit string', 
                  'string digit string', 
                  'digit string digit', 
                  'string special string', 
                  'string special digit', 
                  'string special', 
                  'string digit special']

    output = []
    
    # STRINGS
    for p in range(1, n_string + 1):
        L = []
        k = 0
        L.append(p * n_digit + k)
        k += n_string * n_digit
        L.append(p + k)
        k += n_string
        # digits only
        L.append(-100) # ONLY FOR FORMAT
        k += n_digit
        L.append(n_digit * p + k)
        k += n_digit * n_string
        L.append(p * n_digit * n_string * 2 + k)
        k += n_string * n_digit * n_string * 2
        L.append(n_digit * p * n_digit + k)
        k += n_digit * n_string * n_digit
        L.append(p * n_special * n_string * 2 + k)
        k += n_string * n_special * n_string * 2
        L.append(p * n_special * n_digit + k)
        k += n_string * n_special * n_digit
        L.append(p * n_special + k)
        k += n_string * n_special
        L.append(p * n_digit * n_special + k)

        # Add efforts to output
        output.append((string_list[p - 1], L))

    # DIGITS
    for p in range(1, n_digit + 1):
        L = []
        k = 0
        L.append(n_string * p + k)
        k += n_string * n_digit
        # strings only
        L.append(-100) # ONLY FOR FORMAT
        k += n_string
        L.append(p + k)
        k += n_digit
        L.append(p * n_string + k)
        k += n_digit * n_string
        L.append(n_string * p * n_string + k)
        k += n_string * n_digit * n_string
        L.append(p * n_string * n_digit * 2 + k)
        k += n_digit * n_string * n_digit * 2
        # string and special only
        L.append(-100) # ONLY FOR FORMAT
        k += n_string * n_special * n_string
        L.append(n_string * n_special * p + k)
        k += n_string * n_special * n_digit
        # string and special only
        L.append(-100) # ONLY FOR FORMAT
        k += n_string * n_special
        L.append(n_string * p * n_special + k)

        # Add efforts to output
        output.append((digit_list[p - 1], L))

    return output
