'''
IMPORTANT: IF THE FILES ARRANGEMENTS ARE CHANGED, verify.c and main.c
must be chaged accordingly, see README.txt in Enrolling folder
-This file will ask the user if they want to either enroll or verify
a fingerprint
-It will save the fingerprint to ./Enrolling directory as a .bin file
-If verifying and a match if found, it will call modulator.py and send a signal
'''

import subprocess
import modulator
import os

def main():
	print("Hello, would you like to (e)nroll a fingerprint or (v)erify one?")
	while(True):
		user_input = input()
		if (user_input[0] == 'e'):
			print("Enrolling")
			os.system("make -C ./Enrolling Enroll")
			subprocess.call(["./Enrolling/Enroll"])
			print("Quitting")
			quit()
		elif (user_input[0] == 'v'):
			print("Verifying")
			os.system("make -C ./Enrolling Verify")
			print("Please scan your finger")
			verify_output = subprocess.check_output(["./Enrolling/Verify"])
			if bytes("Match found!", "utf-8") in verify_output:
				print("Match found!")
				print("Running modulator.py...")
				modulator.main()
			elif bytes("No matches", "utf-8") in verify_output:
				print("No matches")
			elif bytes("The template set is empty.", "utf-8") in verify_output:
				print("There are no enrolled finger-prints")
			elif bytes("No fingerprint device found.", "utf-8") in verify_output:
				print("No fingerprint device found.")
			elif bytes("ABSVerify() failed", "utf-8") in verify_output:
				print("UKNOWN ERROR: Try re-plugging in the device.")
			print("Quitting")
			quit()
		elif (user_input[0] == 'q'):
			print("Quitting")
			quit()
		else:
			print("please select 'e' for enroll or 'v' for verify (q to quit)")


def send():
	modulator.main()

if __name__ == '__main__':
	main()