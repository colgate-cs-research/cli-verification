from make_command import make_command

ip_values = ["0.0.0.0", "1.1.1.1", "1.1.1.0", "1.1.0.0"]
ip_mask_values = ["0", "23", "24", "32"]
mask_values = ["0.0.0.0", "255.255.254.0", "255.255.255.0", "255.255.255.255"]

def replace_ip_values(commands):
	values = []
	if(isinstance(commands, str)):
		commands_list = [commands]
	else:
		commands_list = commands
	for command in commands_list:
		for ip in ip_values: #iterate through keys
			values.append(command.replace("A.B.C.D", ip))
	return values

def replace_ip_with_mask_values(commands):
	values = []
	if(isinstance(commands, str)):
		commands_list = [commands]
	else:
		commands_list = commands
	for command in commands_list:
		for ip_mask in ip_mask_values:
			values.append(command.replace("M", ip_mask))
	return values
	
	
def replace_mask_values(commands):
	values = []
	if(isinstance(commands, str)):
		commands_list = [commands]
	else:
		commands_list = commands
	for command in commands_list:
		for mask in mask_values:
			values.append(command.replace("M.A.S.K", mask))
	return values

def get_ip_values(command):
	values = []
	if "A.B.C.D" in command:
		values = replace_ip_values(command)
	if "/M" in command:
		values = replace_ip_with_mask_values(values)
	if "M.A.S.K" in command:
		values = replace_mask_values(values)
	
	return values
	

commands_list = []

with open('config_templates') as file:
	lines = file.readlines()
	for line in lines:
		commands = make_command(line)
		if(isinstance(commands, str)):
			commands_list.append(commands)
		else:
			for command in commands:
				commands_list.append(command)

line_count = 0
file_index = 0
for command in commands_list:		
	command_types = get_ip_values(command)
	if(len(command_types) == 0):
		command_types = [command]
	
	for i in range(0, len(command_types) - 1):
		
		if line_count == 0:
			config_writer = open("config_writer_"+str(file_index), "w")
			config_writer.write("#!/usr/bin/expect -f"+'\n')
			config_writer.write("set timeout 1"+'\n')
			config_writer.write("log_file tests.log"+'\n')
			config_writer.write("spawn vtysh"+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			config_writer.write(r'send -- "configure terminal\r"'+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			file_index = file_index + 1
		
		for j in range(i+1, len(command_types)):
			config_writer.write(r'send -- "'+command_types[i].strip()+r'\r"'+'\n')
			config_writer.write(r'expect "*#"'+'\n') 
			config_writer.write(r'send -- "'+command_types[j].strip()+r'\r"'+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			config_writer.write(r'send -- "exit\r"'+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			config_writer.write(r'send -- "show run\r"'+'\n')
			#config_writer.write(r'expect "*#"'+'\n')
			config_writer.write(r'expect {'+'\n'+r'timeout { send_log "POSSIBLE ERROR DETECTED" }'+'\n'+r'".*'+command_types[i].strip()+r'.*'+command_types[j].strip()+r'.*"'+'\n'+'}'+'\n')
			'''
			expect { 
			timeout { exit 1 }
			".*command1.*command2.*"
			}
			'''
			#TODO: Add expect to test output
			config_writer.write(r'send -- "configure terminal\r"'+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			config_writer.write(r'send -- "no access-list WORD\r"'+'\n')
			config_writer.write(r'send -- "'+command_types[j].strip()+r'\r"'+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			config_writer.write(r'send -- "'+command_types[i].strip()+r'\r"'+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			config_writer.write(r'send -- "exit\r"'+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			config_writer.write(r'send -- "show run\r"'+'\n')
			#config_writer.write(r'expect "*#"'+'\n')
			'''
			expect { 
			timeout { exit 1 }
			".*command1.*command2.*"
			}
			'''
			config_writer.write(r'expect {'+'\n'+r'timeout { send_log "POSSIBLE ERROR DETECTED" }'+'\n'+r'".*'+command_types[j].strip()+r'.*'+command_types[i].strip()+r'.*"'+'\n'+'}'+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			#TODO: Add expect to test output
			config_writer.write(r'send -- "configure terminal\r"'+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			config_writer.write(r'send -- "no access-list WORD\r"'+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			
			line_count = line_count + 1
		
		if line_count > 500:
			line_count = 0
			config_writer.write(r'send -- "exit\r"'+'\n')
			config_writer.write(r'expect "*#"'+'\n')
			config_writer.write(r'send -- "exit\r"'+'\n')
			config_writer.write(r'expect eof')
			config_writer.close()
		
 
config_writer.write(r'send -- "exit\r"'+'\n')
config_writer.write(r'expect "*#"'+'\n')
config_writer.write(r'send -- "exit\r"'+'\n')
config_writer.write(r'expect eof')
			  
		
		
		
		
