from .transformationTables import get_EBCDIC_TABLE

def generateTextMatrix(plainText):
	EBCDIC_table = get_EBCDIC_TABLE()
	keys = EBCDIC_table.keys()
	ebcdic_codes = []
	# generating EBCDIC equivalent for each character in the plain text
	for each in plainText:
		if each in keys:
			ebcdic_codes.append(EBCDIC_table[each])
	return ebcdic_codes

def generateSubtractiveMatrix(l1, l2):
	difference = []
	zipObject = zip(l1, l2)
	for i, j in zipObject:
		difference.append(i-j)
	return difference

def invert(binary):
	(l, m) = (3, 6)
	temp = binary[l-1:m]
	temp = temp[::-1]
	return binary.replace(binary[l-1:m], temp)

def generateCipher(subtractiveMatrix):
	EBCDIC_table = get_EBCDIC_TABLE()
	keys = EBCDIC_table.keys()
	# generating binary equivalent of each element of the subtractive matrix
	binary_equivalent = []
	for each in subtractiveMatrix:
		binary_equivalent.append(bin(each).replace('0b', '').zfill(8))
	# above binary stream is divided into two streams
	segment1 = []
	segment2 = []
	for i in range(len(binary_equivalent)//2):
		segment1.append(binary_equivalent[i])
	for i in range(len(binary_equivalent)//2, len(binary_equivalent)):
		segment2.append(binary_equivalent[i])
	# applying uniform crossover
	temp = []
	temp = segment1[:]
	for i in range(1, len(segment1), 2):
		segment1[i] = segment2[i]
	for i in range(1, len(segment2), 2):
		segment2[i] = temp[i]
	# applying inversion mutation
	for i in range(len(segment1)):
		segment1[i] = invert(segment1[i])
	for i in range(len(segment2)):
		segment2[i] = invert(segment2[i])
	# converting each segment to a bit stream
	stream1 = ""
	stream2 = ""
	finalStream = ""
	for each in segment1:
		stream1 += each
	for each in segment2:
		stream2 += each
	finalStream += stream1
	finalStream += stream2
	# obtaining hexadecimal equivalent
	hexadecimalString = ""
	for i in range(0, len(finalStream), 4):
		decimal = int(finalStream[i:i+4], 2)
		hexadecimal = hex(decimal).replace("0x", "").upper()
		hexadecimalString += hexadecimal
	return hexadecimalString

def encrypt(keyMatrix, plainText):	
	# generating the plain text matrix
	textMatrix = generateTextMatrix(plainText.upper())
	# generating the subtractive matrix by subtracting the key matrix from the text matrix
	subtractiveMatrix = generateSubtractiveMatrix(textMatrix, keyMatrix)
	# generating the cipher
	cipher = generateCipher(subtractiveMatrix)
	return cipher