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

def invert(binary):
	(l, m) = (3, 6)
	temp = binary[l-1:m]
	temp = temp[::-1]
	return binary.replace(binary[l-1:m], temp)

def convertIntoBinarySegments(cipher):
	binary = []
	for each in cipher:
		binary.append(bin(int(each, 16)).replace('0b', '').zfill(4))
	segment1 = []
	segment2 = []
	for i in range(len(binary)//2):
		segment1.append(binary[i])
	for i in range(len(binary)//2, len(binary)):
		segment2.append(binary[i])
	segment1 = [i+j for i,j in zip(segment1[::2], segment1[1::2])]
	segment2 = [i+j for i,j in zip(segment2[::2], segment2[1::2])]
	return (segment1, segment2)

def inversionMutation(segment1, segment2):
	for i in range(len(segment1)):
		segment1[i] = invert(segment1[i])
	for i in range(len(segment2)):
		segment2[i] = invert(segment2[i])
	return (segment1, segment2)

def uniformCrossover(segment1, segment2):
	temp = []
	temp = segment1[:]
	for i in range(1, len(segment1), 2):
		segment1[i] = segment2[i]
	for i in range(1, len(segment2), 2):
		segment2[i] = temp[i]
	return(segment1, segment2)

def add(m1, m2):
	sum = []
	zipObj = zip(m1, m2)
	for i, j in zipObj:
		sum.append(i+j)
	return sum

def getPlainText(textMatrix):
	plainText =""
	keys = list(EBCDIC_table.keys())
	for each in textMatrix:
		for i in range(len(keys)):
			if each == EBCDIC_table[keys[i]]:
				plainText += keys[i]
	return plainText

def decrypt(cipher, keyMatrix):
	# converting the cipher into two binary equivalent segments of 8 bit group
	(segment1, segment2) = convertIntoBinarySegments(cipher)
	# applying inversion mutation on each 8 bit group
	(segment1, segment2) = inversionMutation(segment1, segment2)
	# applying uniform crossover on each 8 bit group
	(segment1, segment2) = uniformCrossover(segment1, segment2)
	# converting each 8-bit binary group into equivalent decimal, which is also the subtractive matrix
	subtractiveMatrix = []
	for each in segment1:
		subtractiveMatrix.append(int(each, 2))
	for each in segment2:
		subtractiveMatrix.append(int(each, 2))
	# adding Subtractive and Key matrix to get the Plain Text matrix
	textMatrix = add(subtractiveMatrix, keyMatrix)
	# getting the plain text by convering each element of text matrix into EBCDIC equivalent
	plainText = getPlainText(textMatrix)
	return plainText