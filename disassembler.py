class DisAssembler:
	stack = []
	call_stack = []

	funcs = []
	current_func = 0

	pc = 0
	code = b''
	completed = False

	def __init__(self, filename):
		data = open(filename, 'rb').read()
		self.funcs, sep = parse_funcs(data)
		self.code = data[sep:]
		self.init_opcodes()

	def init_opcodes(self):
		self.opcodes = {
			0x1  : self.subtract,       # 1 Byte
			0x2  : self.muiltiply,      # 1 Byte
			0x3  : self.add,            # 1 Byte
			0x8  : self.pushInt64,      # 1 + 8 Bytes
			0xB  : self.setLocal,       # 1 + 4 Bytes
			0xC  : self.getLocal,       # 1 + 4 Bytes
			0xE  : self.decFunction,    # 1 + 4 Bytes
			0xF  : self.printf,         # 1 Byte
			0x10 : self.stackPop,       # 1 Byte
			0x13 : self.divide,         # 1 Byte
			0x15 : self.incFunction,    # 1 Byte
			0x16 : self.inputd,         # 1 Byte
			0x17 : self.jumpNotEqual,   # 1 Byte
			0x18 : self.bit_or,         # 1 Byte
			0x19 : self.bit_and,        # 1 Byte
			0x1A : self.bit_xor,        # 1 Byte
			0x1B : self.jumpEqual,      # 1 Byte
			0x1C : self.jumpLessThan,   # 1 Byte
			0x1D : self.jumpGreaterThan,# 1 Byte
			0x1E : self.jump,           # 1 + 4 Bytes
			0x1F : self.jumpPop,        # 1 Byte
			0x20 : self.incCodeByte,    # 1 + 4 Bytes
			0x21 : self.decCodeByte,    # 1 + 4 Bytes
			0x22 : self.movCodeByte,    # 1 Byte
			0x23 : self.pushWord,       # 1 + 4 Bytes
			0x24 : self.jumpIfEqual,    # 1 + 4 Bytes
			0xD  : self.terminate,      # 1 Byte
		}

	def emulate(self):
		while not self.completed:
			pc = self.pc
			ins, param = self.get_instruction()
			if param != None: ins(param)
			else: ins()

			if param == None:
				print("{0:04x} ->  {1:20}".format(pc, ins.__name__))
			else:
				print("{0:04x} ->  {1:20}  0x{2:x}".format(pc, ins.__name__, param))

	def disassemble(self, pc = 0):
		self.pc = 0
		while True:
			pc = self.pc
			try:
				ins, param = self.get_instruction()
			except Exception as e:
				if self.pc < len(self.code):
					print("Error occured while disassembling : ")
					print(e)

			if ins.__name__ == "incFunction":
				param = self.funcs[param].name
			for func in self.funcs:
				if func.ptr == pc:
					print("\n\n---------------------{}------------------------\n".format(func.name))
			
			if param == None:
				print("{0:04x} ->  {1:20}".format(pc, ins.__name__))
			elif isinstance(param, str):
				print("{0:04x} ->  {1:20}  0x{2}".format(pc, ins.__name__, param))
			else:
				print("{0:04x} ->  {1:20}  0x{2:x}".format(pc, ins.__name__, param))		


	def get_instruction(self):
		param_bytes = {0xB : 4, 0xC : 4, 0x15 : 4, 0x1E : 4, 0x20 : 4, 0x21 : 4, 0x23 : 4, 0x24 : 4, 0x8 : 8}
		byte = self.get_bytes() ; func = self.opcodes[byte] ;  param = None
		if byte in param_bytes:
			param = self.get_bytes(param_bytes[byte])
		return func, param

	def get_bytes(self, count=1):
		val = self.code[self.pc:self.pc+count]
		self.pc += count
		return bytes_to_long(val)

	def terminate(self):
		self.completed = True

	def subtract(self): # 0x1
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		self.stack.append(p1 - p2)

	def muiltiply(self): # 0x2
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		self.stack.append(p1 * p2)

	def add(self): # 0x3
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		self.stack.append(p1 + p2)

	def pushInt64(self, int64): # 0x8
		self.stack.append(int64)

	def setLocal(self, int32): # 0xB  (int 32 -> ind)
		val = self.stack.pop()
		self.funcs[self.current_func].setLocal(int32, val)

	def getLocal(self, int32): # 0xC  (int 32 ->  ind)
		val = self.funcs[self.current_func].getLocal(int32)
		self.stack.append(val)

	def decFunction(self): # 0xE
		self.funcs[self.current_func].decrementFunction()
		self.current_func, self.pc = self.call_stack.pop()
	
	def printf(self): # 0xF
		print(self.stack.pop())

	def stackPop(self): # 0x10
		self.stack.pop()

	def divide(self): # 0x13
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		self.stack.append(int(p1 / p2))

	def incFunction(self, int32): # 0x15 (int 32 -> func ind)
		self.call_stack.append([self.current_func, self.pc])
		self.current_func = int32
		self.pc = self.funcs[self.current_func].ptr
		self.funcs[self.current_func].incrementFunction()

	def inputd(self): # 0x16
		num = int(input("Enter a number (lld) : "))
		self.stack.append(num)

	def jumpNotEqual(self): # 0x17
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		if (p1 != p2):
			self.pc = self.code.find(14, self.pc) + 1
		
	def bit_or(self): # 0x18
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		self.stack.append(p2 | p1)

	def bit_and(self): # 0x19
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		self.stack.append(p2 | p1)

	def bit_xor(self): # 0x1A
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		self.stack.append(p2 ^ p1)
	
	def jumpEqual(self): # 0x1B
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		if (p1 == p2):
			self.pc = self.code.find(14, self.pc) + 1

	def jumpLessThan(self): # 0x1C
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		if (p1 < p2):
			self.pc = self.code.find(14, self.pc) + 1

	def jumpGreaterThan(self): # 0x1D
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		if (p1 > p2):
			self.pc = self.code.find(14, self.pc) + 1
		
	def jump(self, int32): # 0x1E (int 32 -> address)
		self.pc = int32

	def jumpPop(self): # 0x1F
		self.pc = self.stack.pop()

	def incCodeByte(self, int32): # 0x20 (int 32 -> byte off)
		temp = list(self.code)
		temp[int32] = (temp[int32] + 1) & 256
		self.code = bytes(temp)

	def decCodeByte(self, int32): # 0x21 (int 32 -> byte off)
		temp = list(self.code)
		temp[int32] = (temp[int32] - 1) % 256
		self.code = bytes(temp)

	def movCodeByte(self): # 0x22
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		temp = list(self.code)
		temp[p2] = temp[p1]
		self.code = bytes(temp)

	def pushWord(self, int32): # 0x23  (int 32 -> byte off)
		b1 = self.code[int32] << 8
		b2 = self.code[int32 + 1]
		print("0x{:x} -> pushWord  0x{:x}      |  {:x}".format(self._temppc, int32, b1 + b2))
		self.stack.append(b1 + b2)

	def jumpIfEqual(self, int32): # 0x24 (int32 -> address)
		p1 = self.stack.pop()
		p2 = self.stack.pop()
		if p1 == p2:
			self.pc = int32

class Function:
	buffer = []
	buf_size = 0
	def __init__(self, name, ptr, buff):
		self.name = name.decode()
		self.ptr = ptr
		self.buf_size = buff
		if (self.name == "main"):
			self.incrementFunction()

	def __str__(self):
		return "<Function {0} -> 0x{1:04x}>".format(self.name, self.ptr)

	def setLocal(self, ind, val): 
		self.buffer[-1][ind] = val

	def getLocal(self, ind):
		return self.buffer[-1][ind]

	def incrementFunction(self):
		self.buffer.append([0 for _ in range(self.buf_size)])

	def decrementFunction(self):
		self.buffer.pop()


def bytes_to_long(stream):
	val = 0
	for byte in stream:
		val = ( val << 8 ) | byte
	return val

def parse_funcs(code):
	pc = 4 ; funcs = []
	while code[pc] == 17:
		end = code.find(18, pc + 1)
		name = code[pc+1:end]
		buff = bytes_to_long(code[end+1:end+5])
		ptr = bytes_to_long(code[end+5:end+9])
		func = Function(name, ptr, buff)
		print(len(funcs), func)
		funcs.append(func)
		pc = end + 9
	return funcs, pc