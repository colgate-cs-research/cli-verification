ip_values = ["0.0.0.0", "1.1.1.1", "1.1.1.0", "1.1.0.0"]
ip_mask_values = ["0", "23", "24", "32"]
mask_values = ["0.0.0.0", "255.255.254.0", "255.255.255.0", "255.255.255.255"]

class IPvalue:
	
	def __init__(self, value):
		self.value = self.add_mask(value)
		self.options = self.make_fewer_options()
	
	def __str__(self):
		print(self.value)
		
	def add_mask(self, value):
		if(value.count("A.B.C.D") > 1 and value.count("A.B.C.D\M") == 0):
			return value[::-1].replace("D.C.B.A", "K.S.A.M", 1)[::-1]
		else:
			return value
	
	def make_options(self):
		values = [self.value]
		if "A.B.C.D" in self.value:
			values = self.replace_ip_values(values)
		if "/M" in self.value:
			values = self.replace_ip_with_mask_values(values)
		if "M.A.S.K" in self.value:
			values = self.replace_mask_values(values)
		return values
		
	def replace_ip_values(self, values):
		sub_values = []
		for value in values:
			for ip in ip_values: #iterate through keys
				sub_values.append(value.replace("A.B.C.D", ip))
		return sub_values

	def replace_ip_with_mask_values(self, values):
		sub_values = []
		for value in values:
			for ip_mask in ip_mask_values:
				sub_values.append(value.replace("M", ip_mask))
		return sub_values
	
	def replace_mask_values(self, values):
		sub_values = []
		for value in values:
			for mask in mask_values:
				sub_values.append(value.replace("M.A.S.K", mask))
		return sub_values
		
	def make_fewer_options(self):
		values = [self.value]
		ip_dict = {"0.0.0.0":["0", "0.0.0.0"], "1.1.1.1":["32", "255.255.255.255"], "1.1.1.0":["24", "255.255.255.0"], "1.1.0.0":["23", "255.255.254.0"]}
		if "A.B.C.D" in self.value:
			sub_values = []
			for value in values:
				for ip in ip_dict.keys(): #iterate through keys
					sub_value = value
					sub_value = sub_value.replace("A.B.C.D", ip)
					if "/M" in sub_value:
						sub_value = sub_value.replace("M", ip_dict[ip][0])
					if "M.A.S.K" in sub_value:
						sub_value = sub_value.replace("M.A.S.K", ip_dict[ip][1])
					sub_values.append(sub_value)
			values = sub_values
		return values
	
		
		
		
		
