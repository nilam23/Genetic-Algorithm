from .transformationTables import get_EBCDIC_TABLE

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
	EBCDIC_table = get_EBCDIC_TABLE()
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