import string
import random
from .encryption import encrypt
from .decryption import decrypt

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
	
def generateKeyMatrix(key_text):
	keys = EBCDIC_table.keys()
	ebcdic_codes = []
	ebcdic_codes_binary = []
	keyMatrix = []
	# generating EBCDIC equivalent for the key text
	for i in key_text:
		if i in keys:
			ebcdic_codes.append(EBCDIC_table[i])
	# generating binary equivalent for the above EBCDIC codes by right shifting by 2
	for each in ebcdic_codes:
		each = each >> 2
		binary = str(bin(each).replace("0b", "00"))
		binary = binary.zfill(8)
		ebcdic_codes_binary.append(binary)
		# ebcdic_codes_binary.append(int(format(each, '08b')))
	# generating the key matrix
	for each in ebcdic_codes_binary:
		# keyMatrix.append(binToDec(int(each)))
		keyMatrix.append(int(each, 2))
	return keyMatrix

def getKey():
	pool_of_letters = string.ascii_letters
	randomString = ""
	for i in range(16):
		randomString += random.choice(pool_of_letters)
	return randomString.upper()

def getCipher(plainText):
	# generating key text
	keyText = getKey()

	# encrypting the message
	if len(keyText) == len(plainText):
		keyMatrix = generateKeyMatrix(keyText)
		cipher = encrypt(keyMatrix, plainText)
	else:
		if len(plainText) < 16:
			for i in range(16-len(plainText)):
				plainText += '#'
			keyMatrix = generateKeyMatrix(keyText)
			cipher = encrypt(keyMatrix, plainText)
		elif len(plainText)>16 and len(plainText)<32:
			keyText += keyText
			for i in range(32-len(plainText)):
				plainText += '#'
			keyMatrix = generateKeyMatrix(keyText)
			cipher = encrypt(keyMatrix, plainText)

	return (cipher, keyMatrix)
	# decrypting the cipher
	# decryptedText = decrypt(cipher, keyMatrix)
	# decryptedText = decryptedText.replace('#', '')
	# if plainText.islower():
	# 	decryptedText = decryptedText.lower()
	# 	print(decryptedText)
	# else:
	# 	print(decryptedText)