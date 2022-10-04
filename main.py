from pandas import DataFrame, pandas as pd
from DFMatrix import DFMatrix
from P2D import P2D


class P2DCalculator():

	__baseData: DataFrame
	__outputData: DataFrame

	def __init__(self, inputPath: str, inSheetName: str, index_col: str, outputPath: str, outSheetName: str):
		self.__inputPath = inputPath
		self.__sheetName = inSheetName
		self.__index_col = index_col
		self.__outputPath = outputPath
		self.__outSheetName = outSheetName
		self.__getBaseData()
		self.__calculate()
	
	def __getBaseData(self):
		self.__baseData = pd.read_excel(
			io=self.__inputPath, sheet_name= self.__sheetName, index_col=self.__index_col)

	def __calculate(self):
		dfEntity = DFMatrix(self.__baseData)
		dfMatrix, dfVector = dfEntity.getDFData()
		p2dEntity = P2D(dfMatrix, dfVector)
		self.__outputData = p2dEntity.getP2Distance()

	def saveData(self):
		writer = pd.ExcelWriter(self.__outputPath, engine='openpyxl')
		self.__outputData.to_excel(writer, sheet_name=self.__outSheetName)
		writer.close()
	
	def getData(self):
		return self.__outputData



#config params
inputPath = './data.xlsx'
inSheetName = 'Лист1'
index_col = 'region'
outputPath = '../p2dResults/output.xlsx'
outSheetName = 'output'

calc = P2DCalculator(inputPath, inSheetName, index_col, outputPath, outSheetName)
calc.saveData()