from pandas import DataFrame, Series, pandas as pd
from sklearn.linear_model import LinearRegression


class DFMatrix:
	__worstVector: DataFrame
	__subtractedMatrix: DataFrame
	__sigmaVector: DataFrame
	DFMatrix: DataFrame
	DFVector: DataFrame

	def __init__(self, data: DataFrame):
		self.baseData = data
		self.__makeWorstVector()
		self.__makeSubtractedMatrix()
		self.__calculateSigmaVector()
		self.__makeDFMatrix()
		self.__makeDFVector()
	
	def __makeWorstVector(self):
		self.worstVector = self.baseData.min()

	def __makeSubtractedMatrix(self):
		self.subtractedMatrix = self.baseData.sub(self.worstVector.squeeze(), axis=1)

	def __calculateSigmaVector(self):
		self.sigmaVector = self.baseData.std(ddof=0)
	
	def __makeDFMatrix(self):
		self.DFMatrix = self.subtractedMatrix.divide(self.sigmaVector.squeeze(), axis=1)

	def __makeDFVector(self):
		self.DFVector = self.DFMatrix.transpose().sum()
	
	def getDFData(self):
		return self.DFMatrix, self.DFVector

