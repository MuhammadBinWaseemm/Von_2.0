import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import customtkinter as ctk
from typing import Dict, List, Optional
from backendsimulator import Simulator
import re
# Set appearance mode and theme

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
#
# Register class
class Register:
    sim=Simulator()
    def __init__(self, name: str, bits: int ):
        self.name = name
        self.value = 0
        self.bits = bits
    def set(self, value: int):
        self.value = value & ((1 << self.bits) - 1)
    def _initflag_(self,name : str , bits=1):
        self.name = name
        self.value = 0
        self.bits = bits
    def get(self) -> int:
        return self.value

# Instruction class
class Instruction:
    def __init__(self, opcode: str, operand: Optional[int] = None):
        self.opcode = opcode.upper()
        self.operand = operand

    @staticmethod
    def parse(line: str) -> Optional['Instruction']:
        line = re.split(r'[;#//]', line)[0].strip()
        if not line:
            return None
        parts = line.split()
        if not parts:
            return None
        opcode = parts[0].upper()
        operand = None
        if len(parts) > 1:
            try:
                if parts[1].startswith('0x'):
                    operand = int(parts[1], 16)
                else:
                    operand = int(parts[1])
            except ValueError:
                return None
        return Instruction(opcode, operand)

# self.simulator Class
class Assemblysimulator:
    sim=Simulator()
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Von 2.0 Simulator")
        self.window.geometry("1200x800")
        self.registers: Dict[str, Register] = {
            'DR': Register('DR',16),
            'AC': Register('AC',16),
            'TR': Register('TR',16),
            'IR': Register('IR',16),
            'K': Register('K',16),
            'AR': Register('AR',11),
            'PC': Register('PC',11),
            'SHRI': Register('SHRI',11),
            'SHRO': Register('SHRO',11),
            'SHI': Register('SHI',11),
            'SHO': Register('SHO',11),
            'SC' : Register('SC',3),
            'INPR': Register('INPR',8),
            'OUTR': Register('OUTR',8),
            'IEN': Register('IEN', 1),  # Interrupt Enable
            'FGI': Register('FGI', 1),  # Input Flag
            'FGO': Register('FGO', 1),  # Output Flag
            'R':   Register('R', 1),    # I/O Interrupt
            'I':   Register('I', 1),    # Indirect Address
            'PGI': Register('PGI', 1),  # Program Interrupt
            'E':   Register('E', 1),    # Overflow
            'S':   Register('S', 1)     # Stop
        }

        

        # Memory
        self.memory = ['000 0000 000000000000000'] * 256

        # Program
        self.program: List[Optional[Instruction]] = []
        self.current_line = 0
        self.running = False
        self.setup_ui()
        
    def setup_ui(self):
        self.cycle_count = 0  
        left_frame = ctk.CTkFrame(self.window)
        left_frame.pack(side="left", padx=10, pady=10)

        right_frame = ctk.CTkFrame(self.window)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)

        code_label = ctk.CTkLabel(left_frame, text="Assembly Code", font=("Roboto", 20))
        code_label.pack(pady=5)

        self.code_editor = scrolledtext.ScrolledText(
            left_frame, width=55, height=18,
            bg='#1a1a1a', fg='#00ff00', insertbackground='#00ff00', font=("Courier", 20)
        )
        ## change here
        self.code_editor.pack(padx=10, pady=5)

        button_frame = ctk.CTkFrame(left_frame)
        button_frame.pack(fill="x", padx=10, pady=5)
        button_frame.grid_columnconfigure(0, weight=0)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        button_frame.grid_columnconfigure(3, weight=0)

        
        self.Assemble_button = ctk.CTkButton(
            button_frame,
            text="Assemble",
            command=self.assembleprogram,
            fg_color="#00aa00",
            hover_color="#008800",
            width=170,
        )
    
        
        self.step_button = ctk.CTkButton(
            button_frame,
            text="Step",
            command=self.step_program,
            fg_color="#0088ff",
            hover_color="#0066cc",
            width=170,
        )
        
        
        self.Run_button = ctk.CTkButton(
            button_frame,
            text="Run",
            command=self.run_program,
            fg_color="#ff4400",
            hover_color="#cc3300",
            width=170,
        )
        self.Assemble_button.grid(row=0, column=0, padx=5, pady=5)
        self.step_button.grid(row=0, column=1, padx=5, pady=5)
        self.Run_button.grid(row=0, column=2, padx=5, pady=5)


        # === Second Row: Centered FGI and FGO (empty columns on side) ===
        self.set_fgi_button = ctk.CTkButton(
            button_frame, 
            text="Set FGI", 
            command=self.set_fgi,
            fg_color="#ffaa00", 
            hover_color="#cc8800", 
            width=170
        )
        self.set_fgi_button.grid(row=1, column=0, padx=5, pady=5, sticky="e")  # Right-align
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear Code",
            command=lambda: self.code_editor.delete(1.0, tk.END),
            fg_color="#aa0000",
            hover_color="#880000",
            width=170
        )
        self.clear_button.grid(row=1, column=1, padx=5, pady=5)
        
        self.set_fgo_button = ctk.CTkButton(
            button_frame, 
            text="Set FGO", 
            command=self.set_fgo,
            fg_color="#ffaa00", 
            hover_color="#cc8800", 
            width=170
        )
        self.set_fgo_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")  # Left-align

                # === Third Row: Set INPUT (label and entry) ===
        button_frame = ctk.CTkFrame(left_frame)
        button_frame.pack(fill="x", padx=10, pady=5)

        # ADD this immediately after button_frame
        button_frame.grid_columnconfigure(0, weight=0)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        button_frame.grid_columnconfigure(3, weight=0)

        # Third Row
        self.input_label = ctk.CTkLabel(button_frame, text="Set INPUT", font=("Roboto", 14))
        self.input_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.in_var = ctk.StringVar()
        self.input_entry = ctk.CTkEntry(button_frame, width=150, font=("Courier", 16), justify="center",textvariable=self.in_var)
        self.input_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
       






        self.cycles_label = ctk.CTkLabel(
            button_frame, 
            text="Cycles:", 
            font=("Roboto", 14)
        )
        self.cycles_label.grid(row=2, column=4, sticky="e", padx=5, pady=5)

        # Entry (read-only display)
        self.cycles_entry = ctk.CTkEntry(
            button_frame,
            width=50,
            font=("Courier", 16),
            justify="center"
        )
        self.cycles_entry.grid(row=2, column=5, sticky="w", padx=5, pady=5)
        self.update_cycle_display()  # Initialize display



        # Fourth Row
        # Create "Set KEY" label
    
        
        
        
        
        
        
        self.key_label = ctk.CTkLabel(button_frame, text="Set KEY", font=("Roboto", 14))
        self.key_label.grid(row=2, column=2, sticky="e", padx=5, pady=5)
        self.key_var = ctk.StringVar()
        self.key_entry = ctk.CTkEntry(button_frame, width=180, font=("Courier", 16), justify="center",textvariable=self.key_var)
        self.key_entry.grid(row=2, column=3, sticky="w", padx=5, pady=5)
       
        # 1. Create the display frame (single-line height)
        display_frame = ctk.CTkFrame(left_frame, height=30)  # Minimal height
        display_frame.pack(fill="x", padx=10, pady=(0,5))  # Tight spacing

        # 2. Single-line label (no word wrap)
        self.display_line = ctk.CTkLabel(
            display_frame,
            text="START",  # Default text
            font=("Consolas", 14),  # Monospace font
            fg_color="#222222",
            corner_radius=4,
            anchor="w",  # Left-align text
            height=24,  # Tight fit
            wraplength=0  # Disable word wrapping
        )
        self.display_line.pack(fill="x", padx=3, pady=0)  # Minimal padding

        # 3. Update function (for single-line messages)
        #ok
        
        ##
        self.dropdown = ctk.CTkComboBox(
            button_frame,
            values=["Encryption/Decryption","XOR+Memory Handling", "Optimized Input/Output"],  # Your options
            font=("Courier", 16),
            width=100,  # Make it long
            justify="center",  # Center text inside
            state="readonly",
            command=self.load_example_code
        )
        self.dropdown.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        self.dropdown.set("-Select Option-")
        
        # Registers code , frame , grid

        registers_frame = ctk.CTkFrame(right_frame)
        registers_frame.pack(fill="y", padx=10, pady=5)
        registers_label = ctk.CTkLabel(registers_frame, text="Registers", font=("Roboto", 16))
        registers_label.grid(row=0, column=0, columnspan=3, pady=5)

        self.register_labels: Dict[str, ctk.CTkLabel] = {}

        # ====== Main Registers Display ======
        row = 1
        col = 0
        main_registers = list(self.registers.items())[:14]  # First 14 registers

        # First ensure we have all registers we expect to display
        print(f"Total registers to display: {len(main_registers)}")  # Debug print
        for reg_name, register in main_registers:

            
            label = ctk.CTkLabel(
                registers_frame,
                text=f"{reg_name}:{'0' * register.bits}",
                font=("Courier", 15),
                fg_color="#222222",
                corner_radius=8,
                width=100, 
                height=30
            )
            label.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            self.register_labels[reg_name] = label
            
            # Move to next column, and next row if needed
            col += 1
            if col >= 3:
                col = 0
                row += 1

        # Configure column weights for centering
        for i in range(3):
            registers_frame.grid_columnconfigure(i, weight=1)

        # ====== Flags Display ======
        flags_frame = ctk.CTkFrame(right_frame)
        flags_frame.pack(fill="x", padx=10, pady=5)

        # Flags title - centered
        flags_label = ctk.CTkLabel(
            flags_frame, 
            text="Flags", 
            font=("Roboto", 16, "bold"),
            anchor="center",
        )
        flags_label.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))

        # Define all flag registers in the exact order we want them to appear
        flag_order = ['IEN', 'FGI', 'FGO', 'R', 'I', 'PGI', 'E', 'S']
        flag_registers = [(name, self.registers[name]) for name in flag_order]

        # Add dummy flag to make 9 cells if needed
        if len(flag_registers) < 9:
            flag_registers.append((" ", None))  # Dummy empty slot

      

        # Display flags in 3-column layout
        row = 1
        col = 0
        for reg_name, register in flag_registers:
            if(reg_name == " "):
                break
            if register is not None:
                label = ctk.CTkLabel(
                    flags_frame,
                    text=f"{reg_name}:{'0' * register.bits}",
                    font=("Courier", 15),
                    fg_color="#333333",
                    corner_radius=8,
                    width=100, height=30
                )
                self.register_labels[reg_name] = label
            else:
                label = ctk.CTkLabel(
                    flags_frame,
                    text="",
                    font=("Courier", 15),
                    fg_color="#333333",
                    corner_radius=8,
                    width=100, height=30
                )

            label.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')

            col += 1
            if col == 3:
                col = 0
                row += 1

        # Configure column weights for centering
        for i in range(3):
            flags_frame.grid_columnconfigure(i, weight=1)

       # flags end here self.cycle_countz

        memory_frame = ctk.CTkFrame(right_frame)
        memory_frame.pack(fill="both", expand=True, padx=10, pady=5)

        memory_label = ctk.CTkLabel(memory_frame, text="Memory", font=("Roboto", 16))
        memory_label.pack(pady=5)

        self.memory_display = scrolledtext.ScrolledText(
            memory_frame, width=40, height=30,
            bg='#1a1a1a', fg='#00ffff', font=("Courier", 20)
        )
        self.memory_display.pack(padx=10, pady=5, fill="both", expand=True)
        self.memory_display.delete('1.0', 'end')  # clear first
        self.memory_display.insert('end', "      \n\n")  # center title

        for i,op,address, in self.sim.memory_data:
            line = f"            {i} {op} {address} \n"
            self.memory_display.insert('end', line)

        self.memory_display.configure(state='disabled')  # make it read-only
        self.schedule_memory_updates()  # Start automatic updates
        


    def update_registers_display(self):
        for reg_name, register in self.registers.items():
            bit_length = register.bits  # Assuming each register has a 'bits' attribute
            binary_value = bin(register.get())[2:].zfill(bit_length)  # Convert to binary with leading zeros
            self.register_labels[reg_name].configure(text=f"{reg_name}: {binary_value}")
        self.update_cycle_display()
        self.update_key()
            
            
    def update_memory_display(self):
        self.memory_display.configure(state='normal')
        self.memory_display.delete('1.0', 'end')
        self.memory_display.insert('end', "      \n\n")  # center title
        
        for i, op, address in self.sim.memory_data:
            line = f"            {i} {op} {address} \n"
            self.memory_display.insert('end', line)
        
        self.memory_display.configure(state='disabled')



    def parse_program(self):
        self.program = []
        code = self.code_editor.get(1.0, tk.END).split('\n')
        for line in code:
            if not line.strip():
                continue
            if line.upper().startswith('DATA'):
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        address = int(parts[1])
                        value = int(parts[2])
                        self.memory[address] = value
                    except ValueError:
                        continue
            else:
                instruction = Instruction.parse(line)
                if instruction:
                    self.program.append(instruction)

    def fetch_decode_execute(self) -> bool:
        if not (0 <= self.registers['PC'].get() < len(self.program)):
            return False
        

        instruction = self.program[self.registers['PC'].get()]
        if not instruction:

            return False

        opcode, operand = instruction.opcode, instruction.operand
        ac = self.registers['AC']
        dr = self.registers['DR']
        ir = self.registers['IR']
        tr = self.registers['TR']
        ar = self.registers['AR']
        k = self.registers['K']
        sc = self.registers['SC']
        inpr = self.registers['INPR']
        outr = self.registers['OUTR']
        ien = self.registers['IEN']
        fgi = self.registers['FGI']
        fgo = self.registers['FGO']
        r = self.registers['R']
        i = self.registers['I']
        pgi = self.registers['PGI']
        e = self.registers['E']
        s = self.registers['S']
        pc= self.registers['PC']
        shri = self.registers['SHRI']
        shro = self.registers['SHRO']
        # Decode instruction
        second_row = self.sim.memory_data[pc.get()]  # Gets the 2nd row (index 1)
        address = second_row[0]  # First column (e.g., "001")
        op = second_row[1]       # Second column (e.g., "0000")
        value = second_row[2]    # Third column (e.g., "0000 0000 0000 0000")
        op = ['0'] * 4  # Initialize op as a list of 4 characters
        # Get the current memory data

        

        
        if opcode == 'AND':    # D0
            
            if operand is not None:
                ac.set(ac.get() & self.memory[operand])
                dr.set(self.memory[operand])
            self.cycle_count += 6
            ir.set((0 << 11 )| operand % (2**11)) # Assuming IR is 16 bits
            ar.set(operand % 2**16)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
            
            
        elif opcode == 'ADD':  # D1
            if operand is not None:
                dr.set(self.memory[operand])
                temp = ac.get() + self.memory[operand]
                if temp >= 2**16:  # Handle overflow
                    self.registers['E'].set(1)
                else:
                    self.registers['E'].set(0)
                ac.set(temp % (2**16))
                self.cycle_count += 6
                ir.set((1 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
                ar.set(operand % 2**16)
                ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
                ir_list = list(ir_bits)
                ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
                ir_hex_list = list(ir_hex)
                # Now define value as a list of 16 characters
                value = ['0'] * 16
                # Fill value
                value[0:16]=ir_list
                op[0:4] = ir_hex_list
                value[0] = str(i.get())  # i.get() is int — convert to string
                # If needed, convert value back to string
                value_str = ''.join(value)
                formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
                opp=''.join(op)  # Convert list back to string
                self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        elif opcode == 'LDA':  # D2
            if operand is not None:
                ac.set(self.memory[operand])
            self.cycle_count+= 6
            ir.set((2 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
            ar.set(operand % 2**16)
            dr.set(self.memory[operand])
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
            
            
        
        elif opcode == 'STA':  # D3
            if operand is not None:
                self.memory[operand] = ac.get()
            self.cycle_count += 5
            ir.set((3 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
            ar.set(operand % 2**16)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
            
        
        elif opcode == 'BUN':  # D4
            if operand is not None:
                ir.set((4 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
                ar.set(operand % 2**16)
                ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
                ir_list = list(ir_bits)
                ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
                ir_hex_list = list(ir_hex)
                # Now define value as a list of 16 characters
                value = ['0'] * 16
                # Fill value
                value[0:16]=ir_list
                op[0:4] = ir_hex_list
                value[0] = str(i.get())  # i.get() is int — convert to string
                # If needed, convert value back to string
                value_str = ''.join(value)
                formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
                opp=''.join(op)  # Convert list back to string
                self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
                self.registers['PC'].set(operand)
                self.cycle_count += 5
            
        
        elif opcode == 'BSA':  # D5
            if operand is not None:
                self.cycle_count += 6
                ir.set((5 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
                ar.set(operand % 2**16)
                ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
                ir_list = list(ir_bits)
                ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
                ir_hex_list = list(ir_hex)
                # Now define value as a list of 16 characters
                value = ['0'] * 16
                # Fill value
                value[0:16]=ir_list
                op[0:4] = ir_hex_list
                value[0] = str(i.get())  # i.get() is int — convert to string
                # If needed, convert value back to string
                value_str = ''.join(value)
                formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
                opp=''.join(op)  # Convert list back to string
                self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
                self.memory[operand] = self.registers['PC'].get()
                self.registers['PC'].set(operand + 1)
            
        
        elif opcode == 'ISZ':  # D6
            if operand is not None:
                self.memory[operand] += 1
                dr.set(self.memory[operand])
                ir.set((6 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
                ar.set(operand % 2**16)
                ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
                ir_list = list(ir_bits)
                ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
                ir_hex_list = list(ir_hex)
                # Now define value as a list of 16 characters
                value = ['0'] * 16
                # Fill value
                value[0:16]=ir_list
                op[0:4] = ir_hex_list
                value[0] = str(i.get())  # i.get() is int — convert to string
                # If needed, convert value back to string
                value_str = ''.join(value)
                formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
                opp=''.join(op)  # Convert list back to string
                self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
                if self.memory[operand] == 0:
                    self.registers['PC'].set(self.registers['PC'].get() + 1)
                self.cycle_count += 7
           
        
        elif opcode == 'SUB':  # D7
            if operand is not None:
                ac.set(ac.get() - self.memory[operand])
            ir.set((7 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 6
            ar.set(operand % 2**16)
            dr.set(self.memory[operand])
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        elif opcode == 'REC':  # D8
            if operand is not None:
                dr.set(self.memory[operand])
                temp = dr.get() ^ k.get()
                temp = ((temp << 1) & 0xFFFF)
                reversed_bits = int('{:016b}'.format(temp)[::-1], 2)
                self.memory[operand] = reversed_bits
                dr.set(self.memory[operand])
                self.cycle_count += 8
                ir.set((8 << 11) | (operand % (2**11)))
            ar.set(operand % 2**16)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        elif opcode == 'DSZ':  # D9
            if operand is not None:
                self.memory[operand] -= 1
                dr.set(self.memory[operand])
                if self.memory[operand] == 0:
                    self.registers['PC'].set(self.registers['PC'].get() + 1)
            ir.set((9 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 7
            ar.set(operand % 2**16)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        elif opcode == 'XOR':  # D10
            if operand is not None:
                ac.set(ac.get() ^ self.memory[operand])
            ir.set((10 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 6
            ar.set(operand % 2**16)
            dr.set(self.memory[operand])
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        elif opcode == 'SWP':  # D11
            if operand is not None:
                temp = ac.get()
                ac.set(self.memory[operand])
                self.memory[operand] = temp
            ir.set( (11 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 7
            ar.set(operand % 2**16)
            dr.set(self.memory[operand])
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        elif opcode == 'CLM':  # D12
            if operand is not None:
                self.memory[operand] = 0
                ac.set(0)
            ir.set((12 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 6
            ar.set(operand % 2**16)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        elif opcode == 'RDC':  # D13
            if operand is not None:
                dr.set(self.memory[operand])
                reversed_bits = int('{:016b}'.format(dr.get())[::-1], 2)
                shifted = (reversed_bits >> 1) & 0x7FFF
                temp = shifted ^ k.get()
                ac.set(temp)
                self.cycle_count += 7
                
                
            ir.set((13 << 11 )| operand % (2**11))  # Assuming IR is 16 bits
            ar.set(operand % 2**16)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        # Register Reference Instructions (rB0-rB10)
        elif opcode == 'CLA':  # rB10
            ac.set(0)
            ir.set((14 << 11 )| 1024 % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 4
            ar.set(1024)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        elif opcode == 'CLE':  # rB9
            e.set(0)
            ir.set((14 << 11 )| 512 % (2**11)) # Assuming IR is 16 bits
            self.cycle_count += 4
            ar.set(1024>>1)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        elif opcode == 'CMA':  # rB8
            ac.set(~ac.get())
            ir.set((14 << 11 )| 256 % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 4
            ar.set(1024>>2)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'CME':  # rB7
            self.registers['E'].set(1 if self.registers['E'].get() == 0 else 0)
            ir.set((14 << 11 )| 128 % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 4
            ar.set(1024>>3)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        elif opcode == 'CIR':  # rB6
            # Circular shift right AC and E
          
            ir.set((14 << 11 )| 64 % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 4
            ar.set(1024>>4)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'CIL':  # rB5
            # Circular shift left AC and E
  
            ir.set((14 << 11 )| 32 % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 4
            ar.set(1024>>5)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'INC':  # rB4
            ac.set(ac.get() + 1)
            ir.set((14 << 11 )| 16 % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 4
            ar.set(1024>>6)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'SPA':  # rB3
            if ac.get() >= 0:  # Positive
                self.registers['PC'].set(self.registers['PC'].get() + 1)
            ir.set((14 << 11 )| 8 % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 4
            ar.set(1024>>7)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'SNA':  # rB2
            if ac.get() < 0:  # Negative
                self.registers['PC'].set(self.registers['PC'].get() + 1)
            ir.set((14 << 11 )| 4 % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 4
            ar.set(1024>>8)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'SZA':  # rB1
            if ac.get() == 0:
                self.registers['PC'].set(self.registers['PC'].get() + 1)
            ir.set((14 << 11 )| 2 % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 4
            ar.set(1024>>9)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'SZE':  # rB0
            if self.registers['E'].get() == 0:
                self.registers['PC'].set(self.registers['PC'].get() + 1)
            ir.set((14 << 11 )| 1 % (2**11))  # Assuming IR is 16 bits
            self.cycle_count += 4
            ar.set(1024>>10)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'HLT':  # uB10
                
            ir.set((15 << 11 )| 1024 % (2**11))  # Assuming IR is 16 bits);
            self.cycle_count += 4
            ar.set(1024)  # Directly sets AR to binary 10000000000
            s.set(0)
            self.update_cycle_display()
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
            return False
        
        elif opcode == 'SHR':  # uB11
            if operand is not None:
                ac.set(ac.get() >> 1)
            self.cycle_count += 4
            ar.set(1024>>1)
            
        # Directly sets AR to binary 10000000000

            ir.set((15 << 11 )| 512 % (2**11))
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'SHL':  # uB10
            if operand is not None:
                ac.set(ac.get() << 1)
            self.cycle_count += 4
            ar.set(1024>>2)

        #     ir.set((15 << 11 )|256 % (2**11))
        # elif opcode == 'SHRI':  # uB9
        #     if operand is not None:
        #         pass
        #     ir.set((15 << 11 )| 128 % (2**11))
        # elif opcode == 'SHRO':  # uB8
        #     if operand is not None:
        #         pass    
            ir.set((15  << 11 )|64% (2**11))
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'SIN':  # uB7
            if operand is not None:
                pc.set(shri.get())
                pgi.set(1)
            self.cycle_count += 4
            ir.set((15 << 11 )| 32% (2**11))
            ar.set(1024>>3)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
            
        elif opcode == 'SON':  # uB6
            if operand is not None:
                pc.set(shro.get())
                pgi.set(1)
            ir.set((15  << 11 )| 16% (2**11))
            self.cycle_count += 4
            ar.set(1024>>4)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
            
        # Input/Output and Control Instructions
        elif opcode == 'INP':  # pB10
            ac.set((ac.get() & 0xFF00) | inpr.get())
            fgi.set(0)
            self.cycle_count += 4
            ar.set(1024)
            

            ir.set((24 << 11) | 1024% (2**11))
            
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'OUT':  # pB9
            outr.set(ac.get() & 0x00FF)
            fgo.set(0)
            ir.set((24 << 11) | 512% (2**11))
            self.cycle_count += 4
            ar.set(1024>>1)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'SKI':  # pB8
            if fgi.get() == 1:
                pc.set((pc.get() + 1) % (2**11))
            self.cycle_count += 4
            ar.set(1024>>2)

            ir.set((24 << 11) | 256% (2**11))
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'SKO':  # pB7
            ir.set((24 << 11) | 128% (2**11))
            if fgo.get() == 1:
                pc.set((pc.get() + 1) % (2**11))
            self.cycle_count += 4
            ar.set(1024>>3)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data

        elif opcode == 'ION':  # pB6
            ien.set(1)

            ir.set((24 << 11) | 64% (2**11))
            self.cycle_count += 4
            ar.set(1024>>4)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        elif opcode == 'IOF':  # pB5
            ien.set(0)

            ir.set((24 << 11) | 32% (2**11))
            self.cycle_count += 4
            ar.set(1024>>5)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        
        elif opcode == 'IIN':  # pB4
            if fgi.get() == 1:
                ac.set((ac.get() & 0xFF00) | inpr.get())
                fgi.set(0)
                pc.set((pc.get() + 1) % (2**11))
            ir.set((24 << 11) | 16% (2**11))
            self.cycle_count += 4
            ar.set(1024>>6)
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
           
        elif opcode == 'IOT':  # pB3
            if fgo.get() == 1:
                outr.set(ac.get() & 0x00FF)
                fgo.set(0)
                pc.set((pc.get() + 1) % (2**11))
            ar.set(1024>>7)

            ir.set((24 << 11) | 8% (2**11))
            self.cycle_count += 4
            ir_bits = bin(ir.get())[2:].zfill(16)  # Convert int to 11-bit binary string
            ir_list = list(ir_bits)
            ir_hex = f"{int(ir_bits, 2):04X}"      # Convert to 4-char hex string
            ir_hex_list = list(ir_hex)
            # Now define value as a list of 16 characters
            value = ['0'] * 16
            # Fill value
            value[0:16]=ir_list
            op[0:4] = ir_hex_list
            value[0] = str(i.get())  # i.get() is int — convert to string
            # If needed, convert value back to string
            value_str = ''.join(value)
            formatted_str = ' '.join([value_str[i:i+4] for i in range(0, 16, 4)])
            opp=''.join(op)  # Convert list back to string
            self.sim.memory_data[pc.get()] = (address, opp,formatted_str)  # Update memory_data
        # ... (other I/O instructions)
        else:
            messagebox.showerror("Invalid Instruction", f"Unknown opcode: {opcode}")
            return False
        
        # Increment PC if not a branch/jump instruction
        if opcode not in ['BUN', 'BSA', 'SPA', 'SNA', 'SZA', 'SZE']:
            self.registers['PC'].set(self.registers['PC'].get() + 1)
        
        return True        # Update flags based on AC value

    def run_program(self):
        self.registers['S'].set(1)
        
        in_input = self.in_var.get().strip()
        if in_input:  # Only process if input is not empty
            try:
                # Validate 16-bit binary
                if len(in_input) != 8 or not all(c in '01' for c in in_input):
                    raise ValueError("Must be 16 binary digits (0s and 1s)")
                
                # Convert and set K register
                self.registers['INPR'].set(int(in_input, 2))
                
            except ValueError:
                messagebox.showerror(
                    "Invalid INPR Input",
                    "INPUT must be exactly 8 binary digits (only 0s and 1s)\n\n"
                    "Example valid input: 1010101010101010"
                )
                return  # Stop execution if invalid
        
        
        
        
        
        
        
        
        
        
        
        # First, validate and set K register from input
        key_input = self.key_var.get().strip()
        
        
        if key_input:  # Only process if input is not empty
            try:
                # Validate 16-bit binary
                if len(key_input) != 16 or not all(c in '01' for c in key_input):
                    raise ValueError("Must be 16 binary digits (0s and 1s)")
                
                # Convert and set K register
                self.registers['K'].set(int(key_input, 2))
                
            except ValueError:
                messagebox.showerror(
                    "Invalid KEY Input",
                    "KEY must be exactly 16 binary digits (only 0s and 1s)\n\n"
                    "Example valid input: 1010101010101010"
                )
                return  # Stop execution if invalid
                self.parse_program()
                self.registers['PC'].set(0)
                self.running = True
                while self.running and self.registers['PC'].get() < len(self.program):
                    self.running = self.fetch_decode_execute()
                    self.update_registers_display()
                    self.update_memory_display()
                    self.update_cycle_display()
                    self.update_key()
                    self.window.update()

                messagebox.showinfo("Execution Complete", "Program execution finished!")
    def schedule_memory_updates(self):
        self.update_memory_display()
        self.window.after(500, self.schedule_memory_updates)  # Update every 500ms
        
    def step_program(self):
        if not self.program:
            self.parse_program()
            self.registers['PC'].set(0)

        if self.registers['PC'].get() < len(self.program):
            if not self.fetch_decode_execute():
                self.running = False
            self.update_registers_display()
            self.update_memory_display()

    def reset_simulator(self):
        for register in self.registers.values():
            register.set(0)
        self.memory = [0] * 256
        self.program = []
        self.current_line = 0
        self.running = False
        self.zero_flag = False
        self.negative_flag = False
        self.update_registers_display()
        self.update_memory_display()

    def run(self):
        self.window.mainloop()


    def set_fgi(self):
        self.registers['FGI'].set(1)
        self.refresh_registers()

    def set_fgo(self):
        self.registers['FGO'].set(1)
        self.refresh_registers()
        
    def assembleprogram(self):
        pass
    # Example variable
    

    # Function to update the display
    def update_cycle_display(self):
        self.cycles_entry.configure(state="normal")  # Enable editing temporarily
        self.cycles_entry.delete(0, "end")          # Clear old value
        self.cycles_entry.insert(0, str(self.cycle_count))  # Insert new value
        self.cycles_entry.configure(state="readonly")  # Make read-only again
        
    # Function to update both the variable and the K register
    def load_example_code(self, choice):
        examples = {
    "Encryption/Decryption": """
; REC Encryption/Decryption Example
DATA 100 4   ; Store 4 at address 100
LDA 100      ; Load plain data into AC
REC 100      ; Encrypt with key (address 100)
STA 100      ; Overwrite plaintext with encrypted
LDA 100      ; Load ciphered text into AC
RDC 100      ; Decrypt with key
STA 100      ; Store decrypted result (optional)
HLT          ; Halt execution
""",
    
    "XOR+Memory Handling": """
; XOR+Memory Handling Example
DATA 100 5   ; Store 5 at address 100
DATA 200 3   ; Store 3 at address 200
LDA 100      ; Load into AC
XOR 200      ; XOR with data at address 200
SWP 200      ; Swap AC and memory at 200
HLT          ; Halt execution
""",
    
    "Optimized Input/Output": """
; Optimized Input/Output Example
DATA 100 0   ; Initialize address 100
DATA 200 0   ; Initialize address 200
IIN          ; Input interrupt trigger
STA 100      ; Store input at address 100
IOT          ; Output trigger
STA 200      ; Store output at address 200
HLT          ; Halt execution
"""
}
        
        
        if choice in examples:
            self.code_editor.delete(1.0, tk.END)  # Clear current code
            self.code_editor.insert(tk.END, examples[choice].strip())



if __name__ == "__main__":
    simulator = Assemblysimulator()
    simulator.run()




