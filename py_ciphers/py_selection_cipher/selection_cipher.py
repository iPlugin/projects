import random
from string import ascii_uppercase

LETTERS = ascii_uppercase

def main():
    while True:
        print("Do you want to [1]encrypt or [2]decrypt?")
        res = input(">>> ").lower()
        if res in {"1", "encrypt"}:
            action = "encrypt"
            break
        elif res in {"2", "decrypt"}:
            action = "decrypt"
            break

        print("Please enter either '1' or 'encrypt' for encryption, or '2' or 'decrypt' for decryption.")
        
    while True:
        print("Please specify the key to use")
        if action == "encrypt":
            print("Or enter RANDOM to have one generated for you")
        key = input(">>> ").upper()
        if key == "RANDOM":
            key = generateRandomKey()
            print(f"The key is |{key}| KEEP THIS SECRET!")
            break
        elif checkKey(key):
            break
    
    print(f"Enter the message to {action}")
    msg = input(">>> ")
    
    if action == "encrypt":
        translated = encryptMessage(msg, key)
    elif action == "decrypt":
        translated = decryptMessage(msg, key)
        
    print(f"The {action}ed message is:")
    print(translated)
    
def checkKey(key):
    if sorted(key) != sorted(LETTERS):
        print("There is an error in the key or symbol set")
        return False
    return True

def encryptMessage(message, key):
    return translateMessage(message, key, 'encrypt')

def decryptMessage(message, key):
    return translateMessage(message, key, 'decrypt')

def translateMessage(message, key, action):
    translated = ""
    charsA = LETTERS
    charsB = key
    if action == "decrypt":
        charsA, charsB = charsB, charsA
    
    for char in message:
        if char.upper() in charsA:
            symIndex = charsA.find(char.upper())
            if char.isupper():
                translated += charsB[symIndex].upper()
            else:
                translated += charsB[symIndex].lower()
        else:
            translated += char

    return translated

def generateRandomKey():
    key = list(LETTERS)
    random.shuffle(key)
    return "".join(key)

if __name__ == "__main__":
    main()
