# Returns [hex, decimal]
def string_to_values(message_plain, message_var_name, show_all_steps):
    print("\nStep 1: Convert M into Decimal Number")
    print("-------------------------------------")

    # Display original message
    if show_all_steps:
        print(f"{message_var_name}\t\t= {message_plain}")
    else:
        print(f"{message_var_name}\t    = {message_plain}")

    # Empty string to concatenate hex values
    concat_hex_values = ""

    # Display hex value (1 of 2)
    if show_all_steps:
        print(f"Each hex value\t= ", end="")

    # Go through every char within message
    for char in message_plain:
        # Get ASCII decimal value
        decimal_value = ord(char)
        # Convert from decimal (base 10) to hex (base 16) value
        # Remove hex value's "0x" prefix
        hex_value = hex(decimal_value)[2:]
        # Concatenate hex value
        concat_hex_values += hex_value
        # Display hex value (2 of 2)
        if show_all_steps:
            if char == message_plain[-1]:
                print(f"{hex_value}")
            else:
                print(f"{hex_value}, ", end="")

    # Message is now a large single hex value
    message_hex = concat_hex_values

    # Convert message from hex (base 16) to decimal (base 10) value
    message_decimal = int(message_hex, 16)

    # Display converted values
    if show_all_steps:
        print(f"{message_var_name} (hex)\t\t= {message_hex}")
        print(f"{message_var_name} (decimal)\t= {message_decimal}")
    else:
        print(f"{message_var_name} (hex)     = {message_hex}")
        print(f"{message_var_name} (decimal) = {message_decimal}")

    return [message_hex, message_decimal]


# Returns [N, e, phi(N)]
def get_public_key(message_plain, show_all_steps):
    print("\nStep 2: Get Public Key")
    print("----------------------")
    from sympy import randprime

    # Get N via p and q
    # Recommended for p and q each to be >= 4 times larger than message's bit size
    # The larger, the better
    bit_size = len(message_plain) * 8
    p = randprime(2 ** (bit_size - 1), 2 ** (bit_size))
    q = randprime(2 ** (bit_size - 1), 2 ** (bit_size))
    # p = 51295442427651787434046837331
    # q = 75704086548658285118882634953
    N = p * q

    # Get phi(N)
    phi_N = (p - 1) * (q - 1)

    from math import gcd

    # Get commonly used e (encryption number)
    e = 65537
    # But ensure e is indeed co-prime with phi(N)
    if show_all_steps:
        print(f"p = {p}\nq = {q}\nN = {N}")
        print(f"\nphi(N) = {phi_N}")
        print(f"\ne = {e}")
        print(f"GCD of e and phi(N)  = {gcd(e, phi_N)}")
        print(f"Test: GCD of 4 and 7 = {gcd(4, 7)}")
        print(f"Test: GCD of 4 and 8 = {gcd(4, 8)}")
        print(f"\nThus, public key (N, e)\n= ({N}, {e})")
    else:
        print(f"N      = {N}")
        print(f"phi(N) = {phi_N}")
        print(f"e      = {e}")
        print(f"GCD of e and phi(N) = {gcd(e, phi_N)}")

    return [N, e, phi_N]


# Returns encrypted decimal
def encrypt(public_key, decrypted_decimal_value, show_all_steps):
    print("\nStep 3: Encrypt")
    print("---------------")
    # Use RSA encryption formula: C = (M^e) mod N
    C = pow(decrypted_decimal_value, public_key[1], public_key[0])
    if show_all_steps:
        print(f"M (decimal) = {decrypted_decimal_value}")
        print(f"e           = {public_key[1]}")
        print(f"N           = {public_key[0]}")
        print(f"\nC (encrypted decimal) = {C}")
    else:
        print(f"C (encrypted decimal) = {C}")
    return C


# Returns plaintext message
def decrypt(public_key, encrypted_decimal_value, message_values, message_var_name, message_plain, show_all_steps):
    print("\nStep 4: Decrypt")
    print("---------------")
    from sympy import mod_inverse

    # Get d (decryption number) = mod inverse of (e mod phi(N))
    d = mod_inverse(public_key[1], public_key[2])

    # Use RSA decryption formula: C_decrypted = (C^d) mod N
    C_decrypted_decimal = pow(encrypted_decimal_value, d, public_key[0])

    # Convert C_decrypted from decimal (base 10) to hex (base 16) value
    # Remove hex value's "0x" prefix
    C_decrypted_hex = hex(C_decrypted_decimal)[2:]

    # Convert C_decrypted_hex back to original message
    # Empty array to hold hex char pairs
    C_decrypted_hex_pairs = []
    # Go through every other char within large hex value
    for i in range(0, len(C_decrypted_hex), 2):
        # Pair current char with next char
        pair = C_decrypted_hex[i : i + 2]
        # Append into array
        C_decrypted_hex_pairs.append(pair)
    # Empty string to concatenate hex chars
    C_decrypted_message = ""
    # Go through every hex pair within array
    for pair in C_decrypted_hex_pairs:
        # Convert from hex value to char value
        C_decrypted_message += bytes.fromhex(pair).decode("ascii")

    if show_all_steps:
        print(f"C = {encrypted_decimal_value}")
        print(f"d = {d}")
        print(f"N = {public_key[0]}")
        print(f"\nC (decrypted decimal) = {C_decrypted_decimal}")
        print(f"C (decrypted hex)     = {C_decrypted_hex}")
        # Compare C_decrypted with original message
        print(f"\nCheck: C (decrypted decimal) == {message_var_name} (decimal) ? {C_decrypted_decimal == message_values[1]}")
        print(f"Check: C (decrypted hex)     == {message_var_name} (hex)     ? {C_decrypted_hex == message_values[0]}")
        print(f"\nC (decrypted) = {C_decrypted_message}")
        print(f"Check: C (decrypted) == {message_var_name} ? {C_decrypted_message == message_plain}")
    else:
        print(f"C (decrypted decimal) = {C_decrypted_decimal}")
        print(f"C (decrypted hex)     = {C_decrypted_hex}")
        print(f"C (decrypted)         = {C_decrypted_message}")

    return C_decrypted_message


M = input("Type a word or phrase to encrypt and decrypt:\n")

show_all_steps = False

values = string_to_values(M, "M", show_all_steps)  # Returns [hex, decimal]
public_key = get_public_key(M, show_all_steps)  # Returns [N, e, phi(N)]
encrypted_decimal = encrypt(public_key, values[1], show_all_steps)  # Returns encrypted decimal
decrypted_message = decrypt(public_key, encrypted_decimal, values, "M", M, show_all_steps)  # Returns plaintext message
