import pandas as pd
import pickle
from icecream import ic

class Loader:

    def __init__(self,path,file_name):
        self.path = path
        self.filename = file_name

    def loadFile(self):        
        return df_data

    def getFilePath(self):
        return self.path + "\\" +  self.filename

    def writeFile(self):        
        pass

class PickleLoader(Loader):

    def __init__(self,path,file_name):
        super().__init__(path,file_name)

    def loadFile(self):
        path = self.getFilePath()
        print(path)
        with open(path + ".pickle" , "rb") as input_file:
            bm25 = pickle.load(input_file)
        return bm25

    def writeFile(self,data,file_name):
        super().__init__(self.path,file_name)
        path = self.getFilePath()
        ic(path)
        with open(path + ".pickle", "wb") as output_file:
            pickle.dump(data, output_file)
        

class ExcelLoader(Loader):

    def __init__(self,path,file_name):
        super().__init__(path,file_name)
    
    def loadFile(self):
        path = self.getFilePath()
        df_data = pd.read_excel(path + ".xlsx")        
        return df_data

    def writeFile(self,data,file_name):
        super().__init__(self.path,file_name)
        path = self.getFilePath()
        ic(path)
        data.to_excel(path + ".xlsx")       
        




  
        
        
