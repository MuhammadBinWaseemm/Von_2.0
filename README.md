# Von_2.0

The Von 2.0 Simulator is a Python-based emulator for a 16-bit stored-program computer designed as an enhanced version of the Basic Computer from Morris Mano’s Computer System Architecture. Developed for the CE222-E course (Computer Organization and Assembly Language) at Ghulam Ishaq Khan Institute of Engineering Sciences and Technology, it implements the Von 2.0 Instruction Set Architecture (ISA) with advanced features like cryptographic instructions, prioritized interrupts, and optimized I/O handling.

# Features

- Rich ISA: Supports memory-reference (e.g., ADD, SUB, XOR, REC, RDC), register-reference (e.g., CLA, SIN, SON), and I/O instructions (e.g., INP, OUT, IIN, IOT).

- Cryptographic Operations: REC (Reverse Encrypt) and RDC (Reverse Decrypt) for lightweight security using XOR, bit-reversal, and shifts.

- Prioritized Interrupts: Nested interrupt system with PGI flag to prioritize input over output, using shadow registers (SHRI, SHRO).

- GUI Interface: Built with tkinter and customtkinter, offering code editing, assembly, step-by-step execution, and real-time visualization of registers, memory, and flags.

- Optimized I/O: Memory-mapped I/O and microcoded IIN/IOT instructions to reduce CPU stalls.
  
- Educational Focus: Designed to teach low-level processor architecture, instruction execution, and microoperations.

# Prerequisites

Python: Version 3.8 or higher

# Dependencies:

- tkinter (usually included with Python)

- customtkinter (install via pip install customtkinter)

# Installation

- Clone the repository:

git clone https://github.com/your-username/von2-simulator.git
cd von2-simulator

(i have uploaded the whole virtual environment but just in case , if you want to setup your own environment)
- Install dependencies:

pip install customtkinter
Ensure tkinter is available (included with standard Python installations on most systems).

# Usage

1. Run the simulator:

python Simulator.py

2. The GUI will launch with the following components:

- Code Editor: Write assembly code (e.g., LDA 100, REC 100, HLT).

- Registers/Flags Display: Shows real-time values of 14 registers and 8 flip-flops.

- Memory Display: Shows memory contents in address-opcode-value format.

- Control Buttons:

  - Assemble: Parse and load the program.

  - Step: Execute one instruction at a time.

  - Run: Execute the entire program.

  - Set FGI/FGO: Toggle input/output flags.

  - Clear Code: Reset the code editor.

  - Input/Key Fields: Set 8-bit INPR (binary) and 16-bit K register (binary) values.

  - Dropdown Menu: Load example programs (Encryption/Decryption, XOR+Memory Handling, Optimized I/O).

3. Example workflow:

- Select "Encryption/Decryption" from the dropdown to load sample code.

- Set a 16-bit binary key (e.g., 1010101010101010) in the KEY field.

- Click Assemble to parse the code.

- Click Step to execute instructions one-by-one or Run to execute fully.

- Observe register, memory, and flag updates in real-time.

# Project Structure

- backendsimulator.py: Core simulator logic, handling CPU operations, memory, and instruction execution.

- Simulator.py: GUI frontend, managing user interaction and state visualization.

- COAL PROJECT REPORT.docx: Detailed project documentation, including ISA, microoperations, and design rationale.

Example Code

DATA 5 4   ; Store 4 at address 5
DATA 6 2   ; Store 2 at address 6
LDA 5
ADD 6
STA 7
HLT

# Troubleshooting

- GUI Issues: Ensure customtkinter is installed and Python’s Tkinter backend is functional.

- Invalid Input: INPR requires 8-bit binary, and K requires 16-bit binary. Invalid inputs will trigger error messages.

- VM Performance: If running in a virtual machine, ensure sufficient resources to avoid slowdowns (reinstall VM if needed, as noted in lab issues).

# Contributing

Contributions are welcome! To contribute:

- Fork the repository.

- Create a feature branch (git checkout -b feature-name).

- Commit changes (git commit -m "Add feature").

- Push to the branch (git push origin feature-name).

- Open a pull request.

# Authors

- Muhammad Bin Waseem 

- Muhammad Daniyal 

- Mahad Aqeel 

# Acknowledgments

- Morris Mano’s Computer System Architecture for foundational concepts.

- William Stallings’ Computer Organization and Architecture for ISA design principles.

- Faculty of Computer Science, GIKI, for guidance and support.
