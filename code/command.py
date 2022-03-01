from parameter import Parameter
class Command: #the whole command
	
	def __init__(self, command):
		
		#set command
		self.command = self.remove_comments(command)
		
		#create list of parameter objects
		self.params = self.set_params()
	
	def make_command(self):
		#combinatorially test with params = params, and values = params.params
		#write pict file
		pict = open("pict_temp", "w")
		for i in range(len(self.params)):
			pict.write(str(i)+": ")
			for j in range(len(self.params[i].params)):
				if j != 0:
					pict.write(', ')
				pict.write(str(self.params[i].params[j]))
			pict.write('\n')
		return
	
	def set_params(self):
		substrings = self.extract_brackets()
		params_list = list()
		for string in substrings:
			params_list.append(Parameter(string)) #for each parameter object there will be a list of values, which is what will be used for the command template
		return params_list
	
	#removes comments
	def remove_comments(self, command):
		i = 0
		while i<len(command)-1:
			if (command[i] == '$'):
				j = i+1
				while j < len(command) and (command[j].isalnum() or command[j] == '_'):
					j = j + 1
				start_index = i
				end_index = j
				command = command[:start_index] + command[end_index:]
			else:
				i = i+1
		return command
	
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
		string = self.command
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
		
	

		
	
