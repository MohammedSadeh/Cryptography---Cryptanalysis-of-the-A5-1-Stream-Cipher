from tqdm import tqdm

# --- File Input ---
initial_states_path = input("Enter path to initial_states.txt: ").strip()
known_plaintext_path = input("Enter path to known_plaintext.txt: ").strip()
ciphertext_path = input("Enter path to ciphertext.bin: ").strip()


with open(known_plaintext_path, 'r', encoding='utf-8') as f:
    plaintext = f.read()


#Convert each character to binary representation (8-bit)
plaintext_binary = ''.join(format(ord(char), '08b') for char in plaintext)

#Read the input file ciphertext.bin
with open(ciphertext_path, 'r') as c:
    ciphertext_binary = c.read()

#The plaintext is 152 bits and we have the ciphertext, so we can find the first 152 stream keys S0 - S151
known_plaintext_length = len(plaintext_binary)

#stream key
S = []
for i in range(known_plaintext_length):
    S.append(int(plaintext_binary[i]) ^ int(ciphertext_binary[i]))

#Read the initial states for X and Z
with open(initial_states_path, "r") as file:
    lines = file.readlines()

x1 = lines[0].strip()
X = []
for i in range (19):
    X.append(x1[i])
z1 = lines[1].strip()
Z = []
for i in range (23):
    Z.append(z1[i])

#the task now is to find initail states for Y
#2^22 possible initial states, try them all!

Y = []
for i in range (22):
    Y.append(0)

#functions
def shift(X,length, value):
    i = length - 1
    while i > 0:
        X[i] = X[i-1]
        i-=1
    X[0] = value

    return X

def majority(X,Y,Z):
    if(int(X[8]) == 1 and int(Y[10]) == 1):
        return 1
    
    elif(int(X[8]) == 1 and int(Z[10]) == 1):
        return 1
    
    elif(int(Y[10]) == 1 and int(Z[10]) == 1):
        return 1
    
    return 0

possible_Values_Of_Y = []


for i in tqdm(range(2**22)):
    Xtemp = X.copy()
    Ztemp = Z.copy()
    flag = 0
    Ytemp = Y.copy()


    for j in range(known_plaintext_length):
        maj = majority(Xtemp, Ytemp , Ztemp)
        #check X,Y,Z for shift
        if(int(Xtemp[8]) == maj):
            value = (int(Xtemp[13]) ^ int(Xtemp[16])) ^ (int(Xtemp[17]) ^ int(Xtemp[18]))
            shift(Xtemp,len(Xtemp),value)
        if(int(Ytemp[10]) == maj):
            value = int(Ytemp[20]) ^ int(Ytemp[21])
            shift(Ytemp,len(Ytemp),value)
        if(int(Ztemp[10]) == maj):
            value = (int(Ztemp[7]) ^ int(Ztemp[20]) ^ int(Ztemp[21]) ^ int(Ztemp[22]))
            shift(Ztemp,len(Ztemp),value)

        stream = int(Xtemp[18]) ^ int(Ytemp[21]) ^ int(Ztemp[22])
        if stream == S[j]:
            if j == known_plaintext_length - 1:
                flag = 1

        else:
            flag = 0
            binary_str = format(i, '022b') 
            Y = [int(bit) for bit in binary_str]
            break
    
    if flag == 1:
        possible_Values_Of_Y.append(Y)
        binary_str = format(i, '022b') 
        Y = [int(bit) for bit in binary_str]


original_text = ''
for k in range(len(possible_Values_Of_Y)):
    Y = possible_Values_Of_Y[k]

    # Save recovered Y state to file
    with open('recovered_y_state.txt', 'w') as f:
        f.write(''.join(str(bit) for bit in Y))

    for i in range(len(ciphertext_binary)):
        maj = majority(X, Y , Z)
        #check X,Y,Z for shift
        if(int(X[8]) == maj):
            value = (int(X[13]) ^ int(X[16])) ^ (int(X[17]) ^ int(X[18]))
            shift(X,len(X),value)
        if(int(Y[10]) == maj):
            value = int(Y[20]) ^ int(Y[21])
            shift(Y,len(Y),value)
        if(int(Z[10]) == maj):
            value = (int(Z[7]) ^ int(Z[20]) ^ int(Z[21]) ^ int(Z[22]))
            shift(Z,len(Z),value)

        stream = int(X[18]) ^ int(Y[21]) ^ int(Z[22])

        original_text += str(int(ciphertext_binary[i]) ^ stream)

    original_text_ascii = ''.join(chr(int(original_text[i:i+8], 2)) for i in range(0, len(original_text), 8))

    # Save to file
    with open('recovered_plaintext.txt', 'w', encoding='utf-8') as f:
        f.write(original_text_ascii)


#print(original_text_ascii)


