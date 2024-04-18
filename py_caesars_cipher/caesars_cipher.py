from string import ascii_uppercase

LETTER = ascii_uppercase

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
    key1 = len(LETTER) - 1
    print(f"Please enter the key (0 to {key1}) to use")
    res = input(">>> ").upper()
    if not res.isdecimal():
        continue
    
    if 0 <= int(res) < len(LETTER):
        key2 = int(res)
        break

print(f"Enter the message to {action}")
msg = input(">>> ").upper()

translated = ""

for char in msg:
    if char in LETTER:
        num = LETTER.find(char)
        if action == "encrypt":
            num = (num + key2) % len(LETTER)
        elif action == "decrypt":
            num = (num - key2) % len(LETTER)
    
        translated += LETTER[num]
    else:
        translated += char
        
print("\n" + translated)