import random

class Parameter: #anything with atleast one set of brackets
	
	def __init__(self, param):
		self.parameter = param
		#create list of parameter objects by looking at bracket type
		self.params = self.set_params()

	def set_params(self):
		params_list = []
		substrings = []
		if self.is_brackets():
			substrings = self.sub_command()
			for string in substrings:
				if self.has_brackets(string):
					params_list.append(Parameter(string))
				else:
					params_list.append(string)
		else:
			substrings = self.extract_brackets()
			"""start_index = 0
			for string in substrings:
				bracket_index = self.parameter.index(string)
				new_string = self.parameter[start_index:bracket_index].strip()
				if len(new_string) > 0:
					params_list.append(Parameter(new_string))
				start_index = bracket_index"""
			for string in substrings:
				params_list.append(Parameter(string))
		"""if not substrings:
			print("here")
			params_list.append(IPvalue(self.parameter))"""
		return params_list
		
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
		outputs.append(str(end))
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
		
	def __str__(self):
		return self.parameter
	
	#simple function to check if string starts and ends with brackets
	def is_brackets(self):
		string = self.parameter
		open_brackets = ['<', '[', '(', '{']
		close_brackets = ['>', ']', ')', '}']
		if(string[0] in open_brackets and string[-1] in close_brackets):
			return 1
		return 0
		
	def has_brackets(self, string):
		brackets = ['<', '[', '(', '{', '>', ']', ')', '}']
		for bracket in brackets:
			if bracket in string:
				return True
		return False
