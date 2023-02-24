#pip install fuzzywuzzy
#pip install python-Levenshtein


import os
import sys
import typing as tp
from fuzzywuzzy import fuzz
import json
from decimal import Decimal

class DataManagement:
	
	__slots__ = ("foods_list", "folder" , "folderbase" , "past_foods_list" , "recieptfolder")
	
	def __init__(self , folder : str , database : str , f_reciept : str) :
		self.folderbase = os.path.join( os.getcwd() , database )
		self.folder = os.path.join( os.getcwd() , folder )
		self.recieptfolder = os.path.join( os.getcwd() , f_reciept )
		self.foods_list = { } # { id : [ filename , name , price , quantity  ] }
		self.past_foods_list = {} # { filename : { id : [ filename , name , price , quantity  ] } }
		
		self.get_foods_in_folder()	# Load all file and datas
	

# ===== Calculations Of Data
	
	def get_selected_info(self) -> tp.Union[ None , list[ tuple[str , float , int], ... ] ] :
		selected = self.get_selected_foods()
		if not selected :
			return None
		
		info = []
		for key in selected :
			name = self.foods_list[key][1]
			price = float(self.foods_list[key][2])
			quan = int(self.foods_list[key][3])
			info.append( (name , price * quan , quan ))
		return info
	
	def get_total_of_selected(self) -> tp.Union[ None , tuple[float , int]] :
		selected = self.get_selected_foods()
		if not selected :
			return None
		
		total_price = 0
		total_quan = 0
		for key in selected :
			price = float(self.foods_list[key][2])
			quan = int(self.foods_list[key][3])
			total_price = total_price + ( quan * price )
			total_quan = total_quan + quan
		return ( total_price , total_quan )
	
# ===== File Getter and Modification
	def load_all_past_selected(self) :
		for file in self.folderbase :
			self.load_past_selected(file)
	
	def load_past_selected(self , filename : str  ) -> tp.Union[ None , dict ] :
		directory = os.path.join(self.folderbase , filename )
		if not os.path.exists(directory) :
			raise FileNotFoundError(f"[ ! ] File not found in past transaction : {filename} ")
		
		with open(directory , 'r') as jf :
			past_data = json.load(jf)
			self.past_foods_list[filename] = past_data
		
	def save_selected(self , filename : str ) :
		selected = self.get_selected_foods()
		if not selected :
			raise ValueError("[ ! ] Should atleast 1 selected foods to save it ")
		
		foods = { key : tuple(self.foods_list[key]) for key in selected }
		with open( os.path.join(self.folderbase , filename ) , "w") as jf :
			json.dump(foods , jf)
		
	def min_quantity_to( self , f_id = None) :
		if not f_id :
			return False
		if self.foods_list[f_id][3]  == 0 :
			return False
		self.foods_list[f_id][3] -= 1
		return True
	
	def add_quantity_to(self , f_id = None ) -> bool :
		if not f_id :
			return False
		self.foods_list[f_id][3] += 1
		return True
	
	def reset_foods_list(self) :
		for key in self.foods_list :
			self.foods_list[key][3] = 0
	
	def get_selected_foods(self) -> tp.Union[ list[str , ...] , None ] :
		found = []
		for key , values in self.foods_list.items() :
			if values[3] > 0 :
				found.append(key)
		if found :	return found
		else :	return None
	
	def search_food(self , find = None  ) -> tp.Union[ list[ str , ... ] , None ] :
		if not find :
			return None
		
		found = []
		passing = 70
		for key , values in self.foods_list.items() :
			if fuzz.ratio( key , find ) > passing :
				found.append( key )
			elif fuzz.ratio(values[1] , find ) > passing :
				found.append( key )
			elif fuzz.ratio( str(values[2]) , find ) > passing :
				found.append( key )
		return found
		
	def get_foods_in_folder(self , sep = ",") :
		os.makedirs( self.folderbase , exist_ok=True)
		os.makedirs(self.recieptfolder , exist_ok= True)
		for num , file in enumerate(os.listdir(self.folder)) :
			data = self.checking_format(file , sep)
			filename = os.path.join( self.folder , file )
			self.foods_list[f"{ num + 100}"] = [ filename , data[0] , data[1] , 0 ]
	
	def checking_format(self , file : str , sep : str  ) -> tuple[str , str] :
		data = os.path.splitext(file)[0] # get the filename only
		data = data.split(sep) # name , price
		
		if len(data) != 2  :
			raise ValueError(f"[ ! ] Must be  ' filename {sep} price ' : {data} ")	
		try :
			float(data[1])
			int(data[1])
		except ValueError :
			print(f"[ ! ] Must be ' filename {sep} price ' : {data[1]} should be numbers ")
			sys.exit()
		else :
			return data
	
	def create_reciept(self , filename : str ) :
		selected = self.get_selected_foods()
		if not selected :
			raise ValueError("[ ! ] Should atleast 1 selected foods to create reciept ")
		
		reciept = "Food Reciept".center(40 , " ")
		

if __name__ == "__main__":
	a  , b= "ywywyw , 2e0".split(",")
	reciept = "Food Reciept".center(40 , " ")
	print(reciept)
	res = Decimal(1.01) + Decimal(5.00)
	print(res)
	a = { "1" : 5 }
	b = { "1" : a }
	print(b)