from machine import Pin, ADC

class ReadVoltages:
	
	def __init__(self,ADCPin,FADCrat):		#Specific ADCPin values and FADC ratios will be specified in config file
		self.ADCpin = ADC(Pin(ADCPin))		
		self.ADCpin.atten(ADC.ATTN_11DB)
		self.FADCrat = FADCrat
		
		
	def read_pin_fadc(self):
		return self.ADCpin.read()
		
		
	def read_source_voltage(self):  
		Vsource = self.read_pin_fadc() * self.FADCrat
		return Vsource
	
	
	#def Compare(self):
	#	if self.ADCpin.read() > (12 * (4095/3)):
	#		return Greater
	#	else:
	#		return Less Than
