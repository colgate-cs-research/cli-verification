import ipaddress
import re

def get_ips(command):
	ip_list = []
	ip_list_str = []
	
	regex_types = ["\d+\.\d+\.\d+\.\d+/\d+", "\d+\.\d+\.\d+\.\d+ \d+\.\d+\.\d+\.\d+", "\d+\.\d+\.\d+\.\d+"]
	for regex_type in regex_types:
		values = re.findall(regex_type, command)
		if values:
			for value in values:
				try:
					ip_list.append(ipaddress.IPv4Network(value.strip().replace(" ", "/"), strict=False))
					ip_list_str.append(value.strip())
					command = command.replace(value, "")
				except ipaddress.NetmaskValueError:
					continue

	return (ip_list, ip_list_str)

def check_command(command, output):

	#print("checking command")
	
	#extract ip from command
	#what if command has multiple ips
	command_ips, command_ips_str = get_ips(command)
	#print(command_ips, "ips", command_ips_str)
	
	#get everything excluding the IP from the command from the output
	#ie get everything from the output that could be a command
	last_index = 0
	command_str = ""
	for command_ip in command_ips_str:
		#print(command_ip, "cmdip", command[last_index+1:command.index(command_ip)])
		command_str = command_str + ".*".join(command[last_index:command.index(command_ip)].split(" "))
		last_index = command.index(command_ip)+len(command_ip)
	command_str = command_str + ".*".join(command[last_index+1:].split(" "))
	if "host" in command_str:
		command_str = command_str.replace("host", "")

	possible_outputs = re.findall(command_str, output)
	#print(command, " : ",command_str)
	
	#extract all ip from the output -- make sure atleast one match
	if len(possible_outputs) == 0:
		return False
		
	check = True
	for output in possible_outputs:
		output_ips = get_ips(output)[0]
		found = False
		check = True
		for command_ip in command_ips:
			for output_ip in output_ips:
				if output_ip == command_ip:
					found = True
					break
			if not found:
				check = False
				break
		if check:
			break
	
	return check
	
logs = open("tests.log", 'r')

#get start index
line = next(logs)

while "myfrr#" not in line:
	line = next(logs)

total_count = 0
err_count = 0

#now line is at the very first configure terminal
#print("first config term:", line)

try:
	while True:
		
		err_disp = False
		
		line = next(logs)
		
		while "no" in line or "#" not in line:
			line = next(logs)
		command1 = line
		command1 = command1[command1.index("#")+2:].strip()
		
		line = next(logs)
		while "no" in line or "#" not in line:
			line = next(logs)
		command2 = line
		command2 = command2[command2.index("#")+2:].strip()
		
		#print(command1, command2)
		
		#now get to the show run
		while "show run" not in line:
			if "error" in line.lower():
				err_disp = True
			line = next(logs)
			
		#now line is at show run
		#print("show run", line)

		#grab output for commands
		output = ""
		while "end" not in line:
			line = next(logs)
			output = output + line
		
		
		#if both commands have sequence number
		if not err_disp:
			if "seq" in command1 and "seq" in command2:
				#if sequence numbers are the same:
				seq1 = command1[command1.index('seq'):].split(" ")[1]
				seq2 = command2[command2.index('seq'):].split(" ")[1]
				if int(seq1) == int(seq2):
					if not check_command(command2, output):
						print(command1, command2)
						err_count+=1
				else:
					if not (check_command(command2, output) and check_command(command1, output)):
						print(command1, command2)
						err_count+=1
			else:
				#print("commands", command1, ",", command2, ",", output)
				#print(check_command(command2, output), check_command(command1, output))
				if not (check_command(command2, output) and check_command(command1, output)):
					print(command1, command2)
					#print(check_command(command2, output),check_command(command1, output))
					err_count+=1
		
		total_count+=1
		
		while "configure terminal" not in line:
			line = next(logs)
			
		#now you are at configure term
		#print("more config term", line)
		
		line = next(logs)		
		while "no" not in line:
			line = next(logs)
		
		#print("no acl", line)
		#now you are at "no access-list WORD"
		
		
except StopIteration:
	print("made it")
	print(total_count, err_count)

	
