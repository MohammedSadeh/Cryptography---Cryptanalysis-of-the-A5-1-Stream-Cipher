# 🔐 A5/1 Cryptanalysis Project

## 📌 Overview
This project implements a **cryptanalytic attack on the A5/1 stream cipher**, which is used in GSM networks to secure voice and data transmissions.  
The task involves recovering the unknown initial state of one of the Linear Feedback Shift Registers (LFSRs) and using it to decrypt the intercepted ciphertext.

## 🎯 Objectives
- Recover the **22-bit initial state** of LFSR **Y** using a known plaintext attack.
- Generate the full keystream to decrypt the ciphertext.
- Output the recovered plaintext message and the recovered state.

## ⚙️ Features
- Reads initial LFSR states and intercepted ciphertext from files.
- Uses known plaintext to deduce the missing LFSR state.
- Recovers and saves the plaintext message.
- Provides progress indicators (`tqdm`) while testing possible states.

## 🛠️ Technologies Used
- **Python 3**
- Libraries: `tqdm`

# 📂 Project Structure
    ├── Task Document             # the task  rquirements
    ├── Task Report               # Final Report for this task, including the results
    ├── task1.py                  # Main cryptanalysis implementation
    ├── initial_states.txt        # Given states of LFSRs X and Z
    ├── known_plaintext.txt       # Known part of plaintext
    ├── ciphertext.bin            # Intercepted ciphertext
    ├── recovered_y_state.txt     # Output: recovered LFSR Y state
    ├── recovered_plaintext.txt   # Output: full plaintext message
    └── README.md                 # Project documentation

