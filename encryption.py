import sympy

EBCDIC_table = {
	' ':64, '&':80, '#':123, '@':125,
	'A':193, 'B':194, 'C':195, 'D':196,
	'E':197, 'F':198, 'G':199, 'H':200,
	'I':201, 'J':209, 'K':210, 'L':211,
	'M':212, 'N':213, 'O':214, 'P':215,
	'Q':216, 'R':217, 'S':226, 'T':227,
	'U':228, 'V':229, 'W':230, 'X':231,
	'Y':232, 'Z':233, '0':240, '1':241,
	'2':242, '3':243, '4':244, '5':245,
	'6':246, '7':247, '8':248, '9':249
}

Conversion_table = {
	0:'#', 1:'A', 2:'B', 3:'C', 4:'D',
	5:'E', 6:'F', 7:'G', 8:'H', 9:'I',
	10:'J', 11:'K', 12:'L', 13:'M', 14:'N',
	15:'O', 16:'P', 17:'Q', 18:'R', 19:'S',
	20:'T', 21:'U', 22:'V', 23:'W', 24:'X',
	25:'Y', 26:'Z', 27:'@', 28:'&', 29:'%', 30:'&'
}

def generateTextMatrix(plainText):
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

def substitutionAlgorithm(matrix):
	# a = sympy.randprime(0, 9)
	# b = sympy.randprime(0, 9)
	(a, b) = (5, 2)
	keys = Conversion_table.keys()
	intermediateCipher = ""
	for x in matrix:
		c = (a * x + b) % 31
		if c in keys:
			intermediateCipher = intermediateCipher + Conversion_table[c]
	return intermediateCipher

def invert(binary):
	(l, m) = (3, 6)
	temp = binary[l-1:m]
	temp = temp[::-1]
	return binary.replace(binary[l-1:m], temp)

def generateCipher(subtractiveMatrix):
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