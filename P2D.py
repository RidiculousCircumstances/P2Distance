from pandas import DataFrame, pandas as pd
from sklearn.linear_model import LinearRegression

class P2D:
	__p2dVector: DataFrame
	__indicators = {}

	def __init__(self, dFMatrix: DataFrame, dfVector: DataFrame):
		self.__model = LinearRegression()
		self.__DFMatrix = dFMatrix
		self.__DFVector = dfVector
		self.__optimizeP2DVector()

	
	def __sortDFMatrix(self):
		corrVector: list = []
		for column in self.__DFMatrix:
			corr = self.__DFMatrix[column].corr(self.__DFVector)
			corrVector.append(corr)

		dfMatrix = self.__DFMatrix.transpose()
		dfMatrix['corr'] = corrVector
		sortedDfMatrix: DataFrame = dfMatrix.sort_values('corr', ascending=False)
		sortedDfMatrix.pop('corr')

		return sortedDfMatrix.transpose()


	def __calcP2DMatrix(self):
		sortedDF = self.__sortDFMatrix()
		weights: list = []

		for i in range(len(sortedDF.axes[1])):
			if (i == 0):
				weights.append(1.0)
				self.__indicators[sortedDF.iloc[:, i].name] = weights[i]
			else:
				numOfPassedColumns = list(range(i))
				X = DataFrame(sortedDF.iloc[:, numOfPassedColumns])
				Y = sortedDF.iloc[:, i]
				self.__model.fit(X, Y)

				depsArgArr = len(Y)
				expArgsCount = X.shape[1]
				r2Score = self.__model.score(X, Y)
				adjustedR2Reversed = 1 - (1 - r2Score) * \
                                    ((depsArgArr - 1)/(depsArgArr - 1 - expArgsCount))
				weights.append(1 - adjustedR2Reversed)
				self.__indicators[sortedDF.iloc[:, i].name] = weights[i]
		result = sortedDF.multiply(weights)
		return result.transpose()


	def __optimizeP2DVector(self):
		p2dMatrix = self.__calcP2DMatrix()
		self.__DFVector = p2dMatrix.sum()
		newP2DMatrix = self.__calcP2DMatrix()
		newVector = newP2DMatrix.sum()

		diff = newVector.sub(self.__DFVector)
		
		sumD = diff.sum()
		self.__DFVector = newVector
		if (sumD >= 0.1 or sumD <= -0.1):
			return self.__optimizeP2DVector()

		self.__p2dVector = newVector

	def getP2Distance(self):
		return self.__p2dVector, self.__indicators