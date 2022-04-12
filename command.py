from parameter import Parameter
import os
class Command: #the whole command
	
	def __init__(self, command):
		
		#set command
		self.command = self.remove_comments(command)
		
		#create list of parameter objects
		self.params = self.set_params()
		
		#create test cases (only goes one level down)
		self.test_params = self.combi_test()
		
		#complete test cases
		self.test_cases = self.make_command()

	def make_command(self):
		#returns all possible combinations of the command
		#run through all test_cases and for each sub in the test cases of the sub command
		
		complete_cases = []
		for test_case in self.test_params:
			new_case = self.command
			for param, test_param in zip(self.params, test_case):
				new_case = new_case.replace(str(param).strip(), "MAKING_COMMAND", 1)
				new_case = new_case.replace("MAKING_COMMAND", test_param, 1)
			complete_cases.append(new_case)

		return complete_cases
	
	def combi_test(self):
		#combinatorially test with params = params, and values = params.params
		#write pict file
		param_set = []
		
		os.chdir("pict")
		pict = open("pict_temp", "w")
		for i in range(len(self.params)):
			pict.write(str(i)+": ")
			for j in range(len(self.params[i].options)):
				if j != 0:
					pict.write(', ')
				pict.write(str(self.params[i].options[j]))
			pict.write('\n')
		pict.close()		
		
		#run pict
		os.system("./pict pict_temp >> temp_out ")
		
		#parse pict
		i = 0
		with open("temp_out", 'r') as params_out:
			for line in params_out:
				if i == 0:
					i = 1
					continue
				current_params = line.strip('\n').split('\t')
				param_set.append(current_params)

		#reset dir
		os.system("rm temp_out")
		os.system("rm pict_temp")
		os.chdir("..")
				
		return param_set
			
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
		
	

		
	
