from command import Command
import os

def run_combi_test(commands):
	
	command_list = []
	
	param_set = []
		
	os.chdir("pict")
	pict = open("pict_temp", "w")
	for i in range(len(commands)):
		pict.write(str(i)+": "+commands[i])
		pict.write('\n')
	pict.close()		
	
	#run pict
	os.system("./pict pict_temp >> temp_out ")
	
	with open ('pict_temp', 'r') as pict:
		for line in pict:
			print(line)
	
	#parse pict
	i = 0
	with open("temp_out", 'r') as params_out:
		for line in params_out:
			if i == 0:
				i = 1
				continue
			combinations = line.strip('\n').split('\t')
			command_list.extend(combinations)
			
	with open ('temp_out', 'r') as pict:
		for line in pict:
			print(line)

	#reset dir
	os.system("rm temp_out")
	os.system("rm pict_temp")
	os.chdir("..")
			
	return command_list


###***###


template_file = open('config_templates', 'r')
commands_list = []
for line in template_file:
	command = Command(line)
	commands_list.extend(command.test_cases)

line_count = 0
file_index = 0

config_writer = open("config_writer", "w")
config_writer.write("#!/usr/bin/expect -f"+'\n')
config_writer.write("set timeout 1"+'\n')
config_writer.write("log_file tests.log"+'\n')
config_writer.write("spawn vtysh"+'\n')
config_writer.write(r'expect "*#"'+'\n')
config_writer.write(r'send -- "configure terminal\r"'+'\n')
config_writer.write(r'expect "*#"'+'\n')

print(str(len(commands_list)), str(len(set(commands_list))))
#print(commands_list)

for i in range(len(commands_list)-1):

	for j in range(i+1, len(commands_list)):
		
		config_writer.write(r'send -- "'+commands_list[i].strip()+r'\r"'+'\n')
		config_writer.write(r'expect "*#"'+'\n') 
		config_writer.write(r'send -- "'+commands_list[j].strip()+r'\r"'+'\n')
		config_writer.write(r'expect "*#"'+'\n')
		config_writer.write(r'send -- "exit\r"'+'\n')
		config_writer.write(r'expect "*#"'+'\n')
		config_writer.write(r'send -- "show run\r"'+'\n')
		config_writer.write(r'expect "*#"'+'\n')
		
		config_writer.write(r'send -- "configure terminal\r"'+'\n')
		config_writer.write(r'expect "*#"'+'\n')
		config_writer.write(r'send -- "no access-list WORD\r"'+'\n')
		config_writer.write(r'expect "*#"'+'\n')
	
	"""config_writer.write(r'send -- "no '+commands_list[i].strip()+r'\r"'+'\n')
	config_writer.write(r'expect "*#"'+'\n')
	config_writer.write(r'send -- "no '+commands_list[j].strip()+r'\r"'+'\n')
	config_writer.write(r'expect "*#"'+'\n')
	config_writer.write(r'send -- "'+commands_list[j].strip()+r'\r"'+'\n')
	config_writer.write(r'expect "*#"'+'\n')
	config_writer.write(r'send -- "'+commands_list[i].strip()+r'\r"'+'\n')
	config_writer.write(r'expect "*#"'+'\n')
	config_writer.write(r'send -- "exit\r"'+'\n')
	config_writer.write(r'expect "*#"'+'\n')
	config_writer.write(r'send -- "show run\r"'+'\n')
	config_writer.write(r'expect "*#"'+'\n')"""

	"""config_writer.write(r'expect "*#"'+'\n')
	config_writer.write(r'send -- "configure terminal\r"'+'\n')
	config_writer.write(r'expect "*#"'+'\n')
	config_writer.write(r'send -- "no '+commands_list[j].strip()+r'\r"'+'\n')
	config_writer.write(r'expect "*#"'+'\n')
	config_writer.write(r'send -- "no '+commands_list[i].strip()+r'\r"'+'\n')
	config_writer.write(r'expect "*#"'+'\n')"""

 
config_writer.write(r'send -- "exit\r"'+'\n')
config_writer.write(r'expect "*#"'+'\n')
config_writer.write(r'send -- "exit\r"'+'\n')
config_writer.write(r'expect eof')



