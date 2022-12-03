'''
1. Iterate over pairs of inputs (obviously)
2. For each item in the pair - find possible output line matches 
	- for now, let's not worry about terms as they come and use regex
3. If satisfactory match found for both, move on. 
	- If satisfactory match not found for either, then it is a "possible error"
		- Categorize this bug under the difference of the closest match and the given input
	- If satisfactory match is found, but there is something like "error" in the output, then it is an "error"
		- Categorize this bug under the error line/description
Random notes:
need to account when config failed, there should not be any extraneous output
'''

'''
Semantic information
1. When command is accepted, immediate next line has no output. Else it has some information, such as "X is not running" or "Configuration failed". 

'''

'''
1. We have ~200 unique categories so let us pick one command from each at random and store in a csv along with
	entire output sequence, category and of course command pair. Also show number of commands in category. 
'''

import ipaddress
import re
import random
import csv

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

	command_ips, command_ips_str = get_ips(command)
	
	#get everything excluding the IP from the command from the output
	#ie get everything from the output that could be a command
	last_index = 0
	command_str = ""
	for command_ip in command_ips_str:
		command_str = command_str + ".*".join(command[last_index:command.index(command_ip)].split(" "))
		last_index = command.index(command_ip)+len(command_ip)
	command_str = command_str + ".*".join(command[last_index+1:].split(" "))
	if "host" in command_str:
		command_str = command_str.replace("host", "")

	possible_outputs = re.findall(command_str, output)
	
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

#assumption: one command is never spread across two lines (or separated by newline)
def close_match(command, output):
	closest_match = ""
	max_count = -1
	command = command.split(" ")
	output = output.split('\n')
	for line in output:
		count = 0
		for string in command:
			count += 1 if re.match(string, line) else 0
		if count > max_count:
			closest_match = line
			max_count = count
	if max_count <= 3: #does not seem to make much of a difference for current test, but maybe look at avg?
		closest_match = ""
	#print(closest_match)
	return closest_match

def find_difference(str1, str2):
	if str1 == "":
		return "(NO OUTPUT) "+str2
	str1 = set(str1.split(" "))
	str2 = set(str2.split(" "))
	differences = str1.difference(str2).union(str2.difference(str1))
	final_diff = ""
	for element in differences:
		final_diff += element + " "
	return final_diff

def test_overlap(command1, command2)
	if str1 == str2:
		

def check_command_new(command1, command2, output):
	'''
		0. make sure commands do not have "overlap"
		1. find plausible matches for each
	'''

	is_overlap = test_overlap(command1, command2)

	command_str = command1.replace(' ', '.*')
	possible_outputs_1 = re.search(command_str, output)
	command_str = command2.replace(' ', '.*')
	possible_outputs_2 = re.search(command_str, output)
	category = "" #category of error

	if possible_outputs_1:
		if possible_outputs_2:
			category = "" # most straightforward case - commands are present exactly, hence do not need category
		else:
			possible_outputs_2 = close_match(command2, output)
			category = find_difference(possible_outputs_2, command2)
	else:
		if not possible_outputs_2:
			possible_outputs_2 = close_match(command2, output)
			category = find_difference(possible_outputs_2, command2)
		if "NO OUTPUT" not in category:
			possible_outputs_1 = close_match(command1, output)
			category += find_difference(possible_outputs_1, command1)

	return category
	

#config file
logs = open("RERUN_Nov22/tests_7.log", 'r')

#get start index
line = next(logs)

#note: here interface can be replaced with name of subcommand
while "myfrr(config)# interface TESTWORD" not in line:
	line = next(logs)

total_count = 0
err_count = 0

category = {}

#so line is at first set of commands

try:
	while True:
		
		err_disp_1 = 0
		err_msg_1 = ""
		err_disp_2 = 0 
		err_msg_2 = ""
		
		while "config-if" not in line:
			line = next(logs)

		command1 = line
		command1 = command1[command1.index("#")+2:].strip()

		#while "no" in line or "#" not in line:
		#	line = next(logs)
		#command1 = line
		#command1 = command1[command1.index("#")+2:].strip()
		
		line = next(logs)
		while "#" not in line:
			err_disp_1 = 1
			err_msg_1 = err_msg_1 + line.strip() + '\n'
			line = next(logs)
		command2 = line
		command2 = command2[command2.index("#")+2:].strip()
		
		line = next(logs)
		#now get to the show run
		while "show run" not in line:
			if "exit" not in line:
				err_disp_2 = 1
				if line != '\n':
					err_msg_2 = err_msg_2 + line.strip() + '\n'
			line = next(logs)

		#now line is at show run
		#print("show run", line)

		#grab output for commands
		output = ""
		while "end" not in line:
			line = next(logs)
			output = output + line
		

		'''
			1. if there is even 1 error message then skip the whole thing, categorize under first err msg. 
			2. if there is no error message, then categorize. 
		'''

		if err_msg_1:
			result = err_msg_1.split('\n')[0].strip()
		elif err_msg_2:
			result = err_msg_2.split('\n')[0].strip()
		else:
			#Generalized logic
			result = check_command_new(command1, command2, output)
		
		if result:
			if result not in category.keys():
				category[result] = []
			category[result].append([command1.strip() + ' ' + command2.strip(), output])

		'''
		Logic for access lists
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
		'''

		total_count+=1
		
		while "configure terminal" not in line:
			line = next(logs)
		
		line = next(logs)	
		while "no interface" not in line:
			line = next(logs)

		
except StopIteration:
	#for key in category.keys():
	#	print(key)
	print("made it")
	print(total_count)
	no_output_count = 0
	csvfile = open('initial_rerun_tests.csv', 'w', newline='\n')
	csvwriter = csv.writer(csvfile, delimiter=',')
	for key in category.keys():
		command_output = category[key][random.randint(0, len(category[key]) - 1)]
		csvwriter.writerow([key]+[len(category[key])]+command_output)
	#print(no_output_count)
	#print(len(category))
	csvfile.close()
	

