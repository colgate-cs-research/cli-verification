#TODO: Figure out how to choose numbers from range. Possibly: first number?

import random
import sys

#simple function to check if string starts and ends with brackets
def is_brackets(string):
	open_brackets = ['<', '[', '(', '{']
	close_brackets = ['>', ']', ')', '}']
	if(string[0] in open_brackets and string[-1] in close_brackets):
		return 1
	return 0

#function to identify masks
def add_mask(outputs):
	masked = []
	if(isinstance(outputs, str)):
		outputs = [outputs]
	for output in outputs:
		if(output.count("A.B.C.D") > 1 and output.count("A.B.C.D\M") == 0):
			masked.append(output[::-1].replace("D.C.B.A", "K.S.A.M", 1)[::-1])
		else:
			masked.append(output)
	return masked

#main function to return all possible combinations of commands
def make_command(string):
	string = remove_comments(string)
	substrings = extract_brackets(string)
	outputs = [string]
	if(is_brackets(string)):
		outputs = sub_command(string)
	if not substrings:
		return add_mask(sub_command(string))
		#return sub_command(string)
	else:
		for substring in substrings:
			commands = make_command(substring)
			outputs = add_commands(outputs, commands, substring)
	return outputs

#make all possible combinations of bracketed template
def add_commands(outputs, commands, substring):
	new_outputs = []
	temp_outputs = set()
	for command in commands:
		for output in outputs:
			try:
				index = output.index(substring)
				new_output = output[:index] + command + output[index+len(substring):]
				new_outputs.append(new_output)
			except ValueError:
				temp_outputs.add(output)
	temp_outputs = list(temp_outputs)
	new_outputs.extend(temp_outputs)
	return new_outputs

#removes comments from string template ($...)
def remove_comments(string):
	i = 0
	while i<len(string)-1:
		if (string[i] == '$'):
			j = i+1
			while j < len(string) and (string[j].isalnum() or string[j] == '_'):
				j = j + 1
			start_index = i
			end_index = j
			string = string[:start_index] + string[end_index:]
		else:
			i = i+1
	return string

#returns highest level bracketed string
def extract_brackets(string):
	open_brackets = ['<', '[', '(', '{']
	close_brackets = ['>', ']', ')', '}']
	start_index = -1
	end_index = -1
	nested_count = 0
	bracket_index = -1
	bracket_count = 0
	substrings = []
	if string[0] in open_brackets and string[-1] in close_brackets:
		string = string[1:-1]
	for i, char in enumerate(string):	
		if (char in open_brackets):
			bracket_count = bracket_count + 1
			if(nested_count == 0):
				start_index = i
				nested_count = nested_count + 1
				bracket_index = open_brackets.index(char)
		if (char in close_brackets):
			bracket_count = bracket_count - 1
			if (char == close_brackets[bracket_index]):
				if(nested_count == 1 and bracket_count == 0):
					nested_count = nested_count - 1;
					end_index = i
					substrings.append(string[start_index:end_index+1])
	return substrings

#substitute/fill-in commands depending on bracket type
def sub_command(string):
	if(string[0] == '<' and string[-1] == '>'):
		return bracket_gt(string[1:-1])
	elif(string[0] == '[' and string[-1] == ']'):
		return bracket_sq(string[1:-1])
	elif(string[0] == '(' and string[-1] == ')'):
		return bracket_cr(string[1:-1])
	elif(string[0] == '{' and string[-1] == '}'):
		return bracket_gt(string[1:-1])
	#elif(string[0].isalnum() and string[-1].isalnum()):
	#	return string
	else:
		return string
	#	print(string)
	#	raise Exception("Unexpected bracket type in command")
		
#substitute commands of the form <...>
def bracket_gt(string):
	num_options = string.count("|") + 1
	start_index = 0
	outputs = []
	for i in range(1, num_options):
		option_index = string.index("|", start_index)
		option = string[start_index:option_index]
		start_index = option_index + 1
		outputs.append(option)
	outputs.append(string[start_index:])
	return outputs

#substitute commands of the form [...]
def bracket_sq(string):
	outputs = []
	outputs.append(string)
	outputs.append("")
	return outputs

#substitute commands of the form (...)
def bracket_cr(string):
	outputs = []
	index = string.index("-")
	start = int(string[:index])
	end = int(string[index+1:])
	outputs.append(str(random.randint(start, end)))
	return outputs

test_command = "access-list WORD$name [seq (1-4294967295)$seq] <deny|permit>$action <A.B.C.D/M$prefix [exact-match$exact]|any>"
test_command = "ipv6 route X:X::X:X/M [from X:X::X:X/M] X:X::X:X <INTERFACE|Null0> [{tag (1-4294967295)|(1-255)|vrf NAME|label WORD|table (1-4294967295)|nexthop-vrf NAME|onlink|color (1-4294967295)}]"
#test_command = sys.argv[1]

commands = remove_comments(test_command)
print(commands)
commands = extract_brackets(commands)
print(commands)
