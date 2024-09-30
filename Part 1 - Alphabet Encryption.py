# Create empty array
alphabets = []

# Go from 0 to 25 (aka. number of alphabets)
# This also makes alphabet's value = array's index
for i in range(0, 26):
    # Fill array with alphabets ("chr(65 onwards)" is uppercase A onwards)
    alphabets.append(chr(65 + i))


# Returns an array = [boolean, string]
def is_valid_message(key, message_plain):
    # Ensure message is a string dtype
    if not type(message_plain) == str:
        return [False, "Error: plaintext message must be a string"]

    # Ensure message contains alphabets only
    if not message_plain.isalpha():
        return [False, "Error: plaintext message must contain (UPPERCASE) alphabets only"]

    # Ensure message is entirely in uppercase
    if not message_plain.isupper():
        return [False, "Error: plaintext message must entirely be in UPPERCASE"]

    # Ensure key's char-length is >= message's char-length
    if not len(key[0 : len(message_plain)]) >= len(message_plain):
        return [False, "Error: key's character-length must be more than or equals (>=) to that of plaintext message"]

    # If message meets all conditions, then it is valid
    return [True, "Valid message"]


# Part 1a
def encrypt_message(key, plaintext_message):
    # Check if message is valid; function returns [boolean, string]
    valid_output = is_valid_message(key, plaintext_message)

    # If message is invalid, then return corresponding error message and exit function
    if valid_output[0] == False:
        return valid_output[1]

    # Create empty string
    encrypted_message = ""

    # Go from index[0] to index[message's char-length]
    for i in range(0, len(plaintext_message)):
        # Get current alphabet's value from both message and key
        alphabet_value_from_msg = alphabets.index(plaintext_message[i])
        alphabet_value_from_key = alphabets.index(key[i])

        # Sum both values, then apply mod 26
        sum = alphabet_value_from_msg + alphabet_value_from_key
        encrypted_value = sum % 26

        # Remember that alphabet's value = array's index (and vice versa)
        # Use encrypted value as index value to get encrypted alphabet
        encrypted_alphabet = alphabets[encrypted_value]
        encrypted_message += encrypted_alphabet

    print("----- ENCRYPTION START -----")
    print(f"Key (original): {key}")
    print(f"Key     (used): {key[0:len(plaintext_message)]}")
    print(f"Message (from): {plaintext_message}")
    print(f"Message   (to): {encrypted_message}")
    print("------ ENCRYPTION END ------\n")
    return encrypted_message


# Part 1b
def decrypt_message(key, cipher_message):
    # Create empty string
    decrypted_message = ""

    # Go from index[0] to index[message's char-length]
    for i in range(0, len(cipher_message)):
        # Get current alphabet's value from both message and key
        alphabet_value_from_msg = alphabets.index(cipher_message[i])
        alphabet_value_from_key = alphabets.index(key[i])

        # Take message value - key value, then apply mod 26
        deducted = alphabet_value_from_msg - alphabet_value_from_key
        decrypted_value = deducted % 26

        # Remember that alphabet's value = array's index (and vice versa)
        # Use decrypted value as index value to get decrypted alphabet
        decrypted_alphabet = alphabets[decrypted_value]
        decrypted_message += decrypted_alphabet

    print("----- DECRYPTION START -----")
    print(f"Key (original): {key}")
    print(f"Key     (used): {key[0:len(cipher_message)]}")
    print(f"Message (from): {cipher_message}")
    print(f"Message   (to): {decrypted_message}")
    print("------ DECRYPTION END ------\n")
    return decrypted_message


key = "THISISANEXAMPLEKEYINCOMPUTERSECURITYEXAM"
msg = "HELLOWORLD"

ciphertext = encrypt_message(key, msg)
decrypt_message(key, ciphertext)
