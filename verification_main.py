import subprocess
import send_bits

def main():
	# print("Scan your fingerprint")
	# output = subprocess.check_output(["./Verification"])
	# if "Match found!" in output:
	# 	print("Match found!")
	# 	print("Sending bits...")
	# 	send()
	# elif "No matches" in output:
	# 	print("No matches.")
	# else:
	# 	print("ERROR: Something weird happened")
	# print("Finished...")
	send()

def send():
	send_bits.main()

if __name__ == '__main__':
	main()