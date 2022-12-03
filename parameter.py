import random
import os
from ipvalue import IPvalue

class Parameter: #anything with atleast one set of brackets
	
	def __init__(self, param):
		self.parameter = param
		
		#create list of all possible options for this parameter
		self.options = self.make_options()

	def make_options(self):
		options_list = []
		substrings = []
		if self.is_brackets():
			substrings = self.sub_command()
			for string in substrings:
				if self.has_brackets(string):
					subparam_options = Parameter(string).options
					options_list.extend(subparam_options)
				else:
					if "A.B.C.D" in string or "X:X::X:X" in string:
						string_options = IPvalue(string).options
						options_list.extend(string_options)
					else:
						options_list.append(string)
		elif self.extract_brackets():
			substrings = self.extract_brackets()
			options_list = [""]
			last_index = 0
			
			for string in substrings:
				temp_list = []
				for option in options_list:
					substr = self.parameter[last_index:self.parameter.index(string, last_index)]
					if "A.B.C.D" in substr or "X:X::X:X" in substr:
						new_option = IPvalue(substr).options
					else:
						new_option = [option.rstrip() + " " + substr.lstrip()]
				temp_list.extend(new_option)	
				options_list = temp_list
				temp_list = []
				subparam_options = Parameter(string).options
				for subparam_option in subparam_options:
					for option in options_list:
						new_option = option.rstrip() + " " + subparam_option.lstrip()
						temp_list.append(new_option)
				options_list = temp_list
				temp_list = []
				last_index = self.parameter.index(string, last_index) + len(string)
				
			temp_list = []
			for option in options_list:
				substr = self.parameter[last_index+1:]
				if "A.B.C.D" in substr or "X:X::X:X" in substr:
					temp_options = IPvalue(substr).options
					new_option = []
					for temp in temp_options:
						new_option.append(option.rstrip()+" "+temp.lstrip())
				else:
					new_option = [option.rstrip() + " " + self.parameter[last_index+1:].rstrip()]
				temp_list.extend(new_option)
			options_list = temp_list
		else:
			if (self.parameter == 'A.B.C.D' or self.parameter == 'A.B.C.D/M' or self.parameter == "X:X::X:X"):
				options_list = IPvalue(self.parameter).options

		return options_list
		
	#substitute/fill-in commands depending on bracket type
	def sub_command(self):
		string = self.parameter
		if(string[0] == '<' and string[-1] == '>'):
			return self.bracket_gt(string[1:-1])
		elif(string[0] == '[' and string[-1] == ']'):
			return self.bracket_sq(string[1:-1])
		elif(string[0] == '(' and string[-1] == ')'):
			return self.bracket_cr(string[1:-1])
		elif(string[0] == '{' and string[-1] == '}'):
			return self.bracket_gt(string[1:-1])
		else:
			return string
		
	#substitute commands of the form <...>
	def bracket_gt(self, string):
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
	def bracket_sq(self, string):
		outputs = []
		outputs.append(string)
		outputs.append("")
		return outputs

	#substitute commands of the form (...)
	def bracket_cr(self, string):
		outputs = []
		index = string.index("-")
		start = int(string[:index])
		end = int(string[index+1:])
		outputs.append(str(start))
		outputs.append(str(random.randint(start, end)))
		outputs.append(str(end - 1))
		return outputs
	
	#extracts top level brackets and sets parameters
	def extract_brackets(self):
		open_brackets = ['<', '[', '(', '{']
		close_brackets = ['>', ']', ')', '}']
		start_index = -1
		end_index = -1
		nested_count = 0
		bracket_index = -1
		bracket_count = 0
		substrings = []
		string = self.parameter
		#if string[0] in open_brackets and string[-1] in close_brackets:
		#	string = string[1:-1]
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
		
	def __str__(self):
		return self.parameter
	
	#simple function to check if string starts and ends with brackets
	#with no brackets in between
	def is_brackets(self):
		string = self.parameter
		open_brackets = ['<', '[', '(', '{']
		close_brackets = ['>', ']', ')', '}']
		stack = []
		if not (string[0] in open_brackets and string[-1] in close_brackets):
			return 0
		first_bracket_closed = 0
		for i in range(len(string)):
			char = string[i]
			if char in open_brackets:
				stack.append(char)
				continue
			if char in close_brackets:
				index = close_brackets.index(char)
				if stack[-1] == open_brackets[index]:
					stack.pop()
				else:
					raise ValueError("invalid bracketing")
			if (i < (len(string) - 1)) and len(stack) == 0:
				return 0
		return 1
		
	def has_brackets(self, string):
		brackets = ['<', '[', '(', '{', '>', ']', ')', '}']
		for bracket in brackets:
			if bracket in string:
				return True
		return False
