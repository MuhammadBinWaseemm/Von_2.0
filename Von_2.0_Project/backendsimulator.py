# backend_simulator.py
class Simulator:
    def __init__(self):
        self.DR='0000000000000000'
        self.AR='00000000000'
        self.IR='0000000000000000'
        self.AC='0000000000000000'
        self.PC='00000000000'
        self.TR='0000000000000000'
        self.K='0000000000000000'
        self.INPR='00000000'
        self.OUTR='00000000'
        self.SC='000'
        self.SHRI='00000000000'
        self.SHRO='00000000000'
        self.SHI='00000000000'
        self.SHO='00000000000'
        self.M = ["0000000000000000"] * 2048
        self.temp = 0
        self.FGI = 0
        self.FGO = 0
        self.PGI = 0
        self.IEN = 0
        self.S = 0
        self.I = 0
        self.E = 0
        self.R = 0
        # Example: memory contents
        self.memory_data = [
            ("000", "0000", "0000 0000 0000 0000"),
            ("001", "0000", "0000 0000 0000 0000"),
            ("002", "0000", "0000 0000 0000 0000"),
            ("003", "0000", "0000 0000 0000 0000"),
            ("004", "0000", "0000 0000 0000 0000"),
            ("005", "0000", "0000 0000 0000 0000"),
            ("006", "0000", "0000 0000 0000 0000"),
            ("007", "0000", "0000 0000 0000 0000"),
            ("008", "0000", "0000 0000 0000 0000"),
            ("009", "0000", "0000 0000 0000 0000"),
            ("00A", "0000", "0000 0000 0000 0000"),
            ("00B", "0000", "0000 0000 0000 0000"),
            ("00C", "0000", "0000 0000 0000 0000"),
            ("00D", "0000", "0000 0000 0000 0000"),
            ("00E", "0000", "0000 0000 0000 0000"),
            ("00F", "0000", "0000 0000 0000 0000"),
            ("010", "0000", "0000 0000 0000 0000"),
            ("011", "0000", "0000 0000 0000 0000"),
            ("012", "0000", "0000 0000 0000 0000"),
            ("013", "0000", "0000 0000 0000 0000"),
            ("014", "0000", "0000 0000 0000 0000"),
            ("015", "0000", "0000 0000 0000 0000"),
            ("016", "0000", "0000 0000 0000 0000"),
            ("017", "0000", "0000 0000 0000 0000"),
            ("018", "0000", "0000 0000 0000 0000"),
            ("019", "0000", "0000 0000 0000 0000"),
            ("01A", "0000", "0000 0000 0000 0000"),
            ("01B", "0000", "0000 0000 0000 0000"),
            ("01C", "0000", "0000 0000 0000 0000"),
            ("01D", "0000", "0000 0000 0000 0000"),
            ("01E", "0000", "0000 0000 0000 0000"),
            ("01F", "0000", "0000 0000 0000 0000"),
            ("020", "0000", "0000 0000 0000 0000"),
            ("021", "0000", "0000 0000 0000 0000"),
            ("022", "0000", "0000 0000 0000 0000"),
            ("023", "0000", "0000 0000 0000 0000"),
            ("024", "0000", "0000 0000 0000 0000"),
            ("025", "0000", "0000 0000 0000 0000"),
            ("026", "0000", "0000 0000 0000 0000"),
            ("027", "0000", "0000 0000 0000 0000"),
            ("028", "0000", "0000 0000 0000 0000"),
            ("029", "0000", "0000 0000 0000 0000"),
            ("02A", "0000", "0000 0000 0000 0000"),
            ("02B", "0000", "0000 0000 0000 0000"),
            ("02C", "0000", "0000 0000 0000 0000"),
            ("02D", "0000", "0000 0000 0000 0000"),
            ("02E", "0000", "0000 0000 0000 0000"),
            ("02F", "0000", "0000 0000 0000 0000"),
            ("030", "0000", "0000 0000 0000 0000"),
            ("031", "0000", "0000 0000 0000 0000"),
            ("032", "0000", "0000 0000 0000 0000"),
            ("033", "0000", "0000 0000 0000 0000"),
            ("034", "0000", "0000 0000 0000 0000"),
            ("035", "0000", "0000 0000 0000 0000"),
            ("036", "0000", "0000 0000 0000 0000"),
            ("037", "0000", "0000 0000 0000 0000"),
            ("038", "0000", "0000 0000 0000 0000"),
            ("039", "0000", "0000 0000 0000 0000"),
            ("03A", "0000", "0000 0000 0000 0000"),
            ("03B", "0000", "0000 0000 0000 0000"),
            ("03C", "0000", "0000 0000 0000 0000"),
            ("03D", "0000", "0000 0000 0000 0000"),
            ("03E", "0000", "0000 0000 0000 0000"),
            ("03F", "0000", "0000 0000 0000 0000"),
            ("040", "0000", "0000 0000 0000 0000"),
            ("041", "0000", "0000 0000 0000 0000"),
            ("042", "0000", "0000 0000 0000 0000"),
            ("043", "0000", "0000 0000 0000 0000"),
            ("044", "0000", "0000 0000 0000 0000"),
            ("045", "0000", "0000 0000 0000 0000"),
            ("046", "0000", "0000 0000 0000 0000"),
            ("047", "0000", "0000 0000 0000 0000"),
            ("048", "0000", "0000 0000 0000 0000"),
            ("049", "0000", "0000 0000 0000 0000"),
            ("04A", "0000", "0000 0000 0000 0000"),
            ("04B", "0000", "0000 0000 0000 0000"),
            ("04C", "0000", "0000 0000 0000 0000"),
            ("04D", "0000", "0000 0000 0000 0000"),
            ("04E", "0000", "0000 0000 0000 0000"),
            ("04F", "0000", "0000 0000 0000 0000"),
            ("050", "0000", "0000 0000 0000 0000"),
            ("051", "0000", "0000 0000 0000 0000"),
            ("052", "0000", "0000 0000 0000 0000"),
            ("053", "0000", "0000 0000 0000 0000"),
            ("054", "0000", "0000 0000 0000 0000"),
            ("055", "0000", "0000 0000 0000 0000"),
            ("056", "0000", "0000 0000 0000 0000"),
            ("057", "0000", "0000 0000 0000 0000"),
            ("058", "0000", "0000 0000 0000 0000"),
            ("059", "0000", "0000 0000 0000 0000"),
            ("05A", "0000", "0000 0000 0000 0000"),
            ("05B", "0000", "0000 0000 0000 0000"),
            ("05C", "0000", "0000 0000 0000 0000"),
            ("05D", "0000", "0000 0000 0000 0000"),
            ("05E", "0000", "0000 0000 0000 0000"),
            ("05F", "0000", "0000 0000 0000 0000"),
            ("060", "0000", "0000 0000 0000 0000"),
            ("061", "0000", "0000 0000 0000 0000"),
            ("062", "0000", "0000 0000 0000 0000"),
    ]













 


        self.D0=self.D1=self.D2=self.D3=self.D4=self.D5=self.D6=self.D7=0
        self.D8=self.D9=self.D10=self.D11=self.D12=self.D13=self.D14=0
        self.D15=0
    def fetch(self):
        self.AR = self.PC
        self.IR = self.M[int(self.AR,2)]
        self.PC = format(int(self.PC,2)+1, '011b')
        if self.IR[1:5] == '0000':
            self.D0 = 1
            self.D1 = self.D2 = self.D3 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '0001':
            self.D1 = 1
            self.D0 = self.D2 = self.D3 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '0010':
            self.D2 = 1
            self.D0 = self.D1 = self.D3 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '0011':
            self.D3 = 1
            self.D0 = self.D1 = self.D2 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '0100':
            self.D4 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '0101':
            self.D5 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D4 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '0110':
            self.D6 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D4 = self.D5 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '0111':
            self.D7 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D4 = self.D5 = self.D6 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '1000':
            self.D8 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D9 = self.D10 = self.D11 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '1001':
            self.D9 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D10 = self.D11 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '1010':
            self.D10 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D11 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '1011':
            self.D11 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D12 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '1100':
            self.D12 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D13 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '1101':
            self.D13 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D12 = self.D14 = self.D15 = 0
        elif self.IR[1:5] == '1110':
            self.D14 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D12 = self.D13 = self.D15 = 0
        elif self.IR[1:5] == '1111':
            self.D15 = 1
            self.D0 = self.D1 = self.D2 = self.D3 = self.D4 = self.D5 = self.D6 = self.D7 = \
            self.D8 = self.D9 = self.D10 = self.D11 = self.D12 = self.D13 = self.D14 = 0
            self.AR = self.IR[5:16]
            self.I = int(self.IR[0])
            self.DR = self.M[int(self.AR, 2)]    
    def execute(self):
        if self.D14==1 or self.D15==1:
            if self.I==1:
                self.executeinpout()
            else:
                self.executeregister()
        else:
            if self.I==1:
                self.AR=self.M[int(self.AR,2)]
            self.executememory()
    
    def executememory(self):
        if self.D1 == 1:
            self.DR = self.M[int(self.AR, 2)]
            temp = int(self.AC, 2) + int(self.DR, 2)
            if temp >= 2**16:
                self.E = 1
            else:
                self.E = 0
            self.AC = temp % (2**16)
            self.AC = format(self.AC, '016b')
        elif self.D0 == 1:
            self.DR = self.M[int(self.AR, 2)]
            temp = int(self.AC, 2) & int(self.DR, 2)
            self.AC = format(temp, '016b')
        elif self.D2 == 1:
            self.DR = self.M[int(self.AR, 2)]
            self.AR = self.DR
        elif self.D3 == 1:
            self.M[self.AR] = self.AC
        elif self.D4 == 1:
            self.PC = self.AR
        elif self.D5 == 1:
            self.M[int(self.AR, 2)] = self.PC
            temp = int(self.AR, 2) + 1
            self.AR = format(temp, '011b')
            self.PC = self.AR
        elif self.D6 == 1:
            self.DR = self.M[int(self.AR, 2)]
            temp = int(self.DR, 2) + 1
            self.DR = format(temp, '016b')
            self.M[self.AR] = self.DR
            if self.DR == '0000000000000000':
                temp = int(self.PC, 2) + 1
                self.PC = format(temp, '011b')
        elif self.D7 == 1:
            self.DR = self.M[int(self.AR, 2)]
            temp = ''.join('1' if bit == '0' else '0' for bit in self.DR)
            temp = int(self.AC, 2) + int(temp, 2) + 1
            temp = temp % (2**16)
            self.AC = format(temp, '016b')
        elif self.D8 == 1:
            temp = int(self.DR, 2) ^ int(self.K, 2)
            self.AC = format(temp, '016b')
            self.AC = self.AC[1:] + '0'
            self.DR = self.AC[::-1]
            self.M[self.AR] = self.DR
        elif self.D9 == 1:
            self.DR = self.M[int(self.AR, 2)]
            temp = int(self.DR, 2) - 1
            self.DR = format(temp, '016b')
            self.M[int(self.AR, 2)] = self.DR
            if self.DR == '0000000000000000':
                temp = int(self.PC, 2) + 1
                self.PC = format(temp, '011b')
        elif self.D10 == 1:
            self.DR = self.M[int(self.AR, 2)]
            temp = int(self.AC, 2) ^ int(self.DR, 2)
            self.AC = format(temp, '016b')
        elif self.D11 == 1:
            self.DR = self.M[int(self.AR, 2)]
            self.M[int(self.AR, 2)] = self.AC
            self.AC = self.DR
        elif self.D12 == 1:
            self.AC = '0000000000000000'
            self.M[int(self.AR, 2)] = self.AC
        elif self.D13 == 1:
            self.DR = self.M[int(self.AR, 2)]
            self.AC = self.DR[::-1]
            self.AC = '0' + self.AC[0:-1]
            temp = int(self.AC, 2) ^ int(self.K, 2)
            self.AC = format(temp, '016b')

    def executeregister(self):
        if self.D14 == 1:
            if self.AR == '10000000000':
                self.AC = '0000000000000000'
            elif self.AR == '01000000000':
                self.E = 0
            elif self.AR == '00100000000':
                self.AC = ''.join('1' if bit == '0' else '0' for bit in self.AC)
            elif self.AR == '00010000000':
                self.E = 0 if self.E == 1 else 1
            elif self.AR == '00001000000':
                self.AC = self.AC[-1] + self.AC[:-1]
                self.E = self.AC[15]
            elif self.AR == '00000100000':
                self.AC = self.AC[1:] + self.AC[0]
                self.E = self.AC[0]
            elif self.AR == '00000010000':
                temp = int(self.AC, 2) + 1
                self.AC = format(temp, '016b')
            elif self.AR == '00000001000':
                if self.AC[0] == '0':
                    temp = int(self.PC, 2) + 1
                    self.PC = format(temp, '011b')
            elif self.AR == '00000000100':
                if self.AC[0] == '1':
                    temp = int(self.PC, 2) + 1
                    self.PC = format(temp, '011b')
            elif self.AR == '00000000010':
                if self.AC == '0000000000000000':
                    temp = int(self.PC, 2) + 1
                    self.PC = format(temp, '011b')
            elif self.AR == '00000000001':
                if self.E == 0:
                    temp = int(self.PC, 2) + 1
                    self.PC = format(temp, '011b')
        
        if self.D15 == 1:
            if self.AR == '10000000000':
                self.S = 0
            elif self.AR == '01000000000':
                self.AC = '0' + self.AC[0:-1]
            elif self.AR == '00100000000':
                self.AC = self.AC[1:] + '0'
            elif self.AR == '00010000000':
                self.PC = self.SHRI
                self.AR = self.SHRI
                self.PGI = 1
            elif self.AR == '00001000000':
                self.PC = self.SHRO
                self.AR = self.SHRO
            elif self.AR == '00000100000':
                temp = int(self.AC, 2) - 1
                self.AC = format(temp, '016b')

    def executeinpout(self):
        if self.AR == '10000000000':
            self.AC = self.AC[0:8] + self.INPR
            self.FGI = 0
        elif self.AR == '010000000000':
            self.OUTR = self.AC[0:8]
            self.FGO = 0
        elif self.AR == '001000000000':
            if self.FGI == 1:
                temp = int(self.PC, 2) + 1
                self.PC = format(temp, '011b')
        elif self.AR == '000100000000':
            if self.FGO == 1:
                temp = int(self.PC, 2) + 1
                self.PC = format(temp, '011b')
        elif self.AR == '00001000000':
            self.IEN = 1
        elif self.AR == '00000100000':
            self.IEN = 0
        elif self.AR == '00000010000':
            if self.FGI == 1:
                self.AC = self.AC[0:8] + self.INPR
                self.FGI = 0
        elif self.AR == '00000001000':
            if self.FGO == 1:
                self.OUTR = self.AC[0:8]
                self.FGO = 0
                temp = int(self.PC, 2) + 1
                self.PC = format(temp, '011b')
    
    def show(message):
        self.display_line.configure(text=f"▶ {message}")  # Add prefix if desired
    #backendsimulator.py
    def reset(self):
            self.AC = '0' * 16
            self.PC = '0' * 16
            self.IR = '0' * 16
            self.AR = '0' * 16
            self.TR = '0' * 16
            self.DR = '0' * 16
            self.K = ''
            self.IEN = '0'
            self.FGI = '0'
            self.FGO = '0'
            self.R = '0'
            self.S = '0'
            self.PGI = '0'
            self.I = '0'
            self.E = '1'
            self.SHRI = '0' * 8
            self.SHRO = '0' * 8
            self.SHI = '0' * 8
            self.SHO = '0' * 8
            self.SC = '0' * 8
            self.INPR = '0' * 8
            self.OUTR = '0' * 8
            self.M = ['0'] * 256  # Reset memory
            