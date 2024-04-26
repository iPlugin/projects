from string import ascii_uppercase

LETTERS = ascii_uppercase

def main():
    while True:
        print("Do you want to [1]encrypt or [2]decrypt?")
        res = input(">>> ").lower()
        if res == "1":
            action = "encrypt"
            break
        elif res == "2":
            action = "decrypt"
            break

        print("Please enter the number 1 or 2")
    
    while True:
        print("Please specify the key to use")
        print("It can be a word or any combination of letters:")
        res = input(">>> ").upper()
        if res.isalpha():
            key = res
            break
        
    print(f"Enter the message to {action}")
    msg = input(">>> ")
    if action == "encrypt":
        translated = encryptMessage(msg, key)
    elif action == "decrypt":
        translated = decryptMessage(msg, key)
    
    print(f"{action.title()}ed message:")
    print(translated)
    
    
def encryptMessage(message, key):
    return translateMessage(message, key, 'encrypt')

def decryptMessage(message, key):
    return translateMessage(message, key, 'decrypt')

def translateMessage(message, key, mode):
    translated = []
    keyIndex = 0
    key = key.upper()

    for char in message:
        num = LETTERS.find(char.upper())
        if num != -1:
            if mode == "encrypt":
                num += LETTERS.find(key[keyIndex])
            elif mode == "decrypt":
                num -= LETTERS.find(key[keyIndex])
                
            num %= len(LETTERS)
            
            if char.isupper():
                translated.append(LETTERS[num])
            elif char.islower():
                translated.append(LETTERS[num].lower())
        else:
            translated.append(char)
        
        keyIndex += 1
        if keyIndex == len(key):
            keyIndex = 0

    return "".join(translated)

    
if __name__ == "__main__":
    main()