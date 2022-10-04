from pandas import DataFrame, Series, pandas as pd
from sklearn.linear_model import LinearRegression

result = pd.read_excel('./testing_calc.xlsx', 'Лист1', index_col='region')

#Возвращает вектор фиктивного региона

def makeWorstVector(data: DataFrame):

	worstVector = data.min()

	return worstVector

#Возвращает матрицу разниц между фактическим индикатором и худшим показателем

def makeSubtractedMatrix(data: DataFrame, vector: DataFrame):

	difference = data.sub(vector.squeeze(), axis=1)

	return difference

#Возвращает вектор СКО для базовой матрицы

def calculateSigma(data: DataFrame):

	std = data.std(ddof=0)
	return std

#Возвращает DF матрицу

def makeDFMatrix(subtractedData: DataFrame, sigma: DataFrame):

	dFMatrix = subtractedData.divide(sigma.squeeze(), axis=1)

	return dFMatrix


def makeDFVector(dfMatrix: DataFrame):
	res = dfMatrix.transpose().sum()
	return res


DFMatrix = makeDFMatrix(makeSubtractedMatrix(
	result, makeWorstVector(result)), calculateSigma(result))

dfVector = makeDFVector(DFMatrix)

def sortMatrix(dfMatrix: DataFrame, dfVector: DataFrame):
	vector: list = []
	for column in dfMatrix:
		corr = dfMatrix[column].corr(dfVector)
		vector.append(corr)


	dfMatrix = dfMatrix.transpose()
	dfMatrix['corr'] = vector
	sortedDfMatrix: DataFrame = dfMatrix.sort_values('corr', ascending=False)
	sortedDfMatrix.pop('corr')
	return sortedDfMatrix
	

def calcP2DMatrix(dfMatrix: DataFrame, dfVector: DataFrame):
	sortedDF = sortMatrix(dfMatrix, dfVector).transpose()
	model = LinearRegression()
	weights: list = []
	
	for i in range(len(sortedDF.axes[1])):
		if(i == 0):
			weights.append(1.0)
		else:
			numOfPassedColumns = list(range(i))
			X = DataFrame(sortedDF.iloc[:, numOfPassedColumns])
			Y = sortedDF.iloc[:, i]
			model.fit(X, Y)
			
			ln = len(Y)
			xshape = X.shape[1]
			r2Sscore = model.score(X, Y)
			adjustedR2Reversed = (1 - r2Sscore)*(ln - xshape -1)
			weights.append(adjustedR2Reversed)

	result = sortedDF.multiply(weights)
	return result.transpose()
	
def optimizeP2DVector(dfMatrix: DataFrame, dfVector: DataFrame):
	p2dMatrix = calcP2DMatrix(dfMatrix, dfVector)
	vector = p2dMatrix.sum()
	
	newP2DMatrix = calcP2DMatrix(dfMatrix, vector)
	newVector = newP2DMatrix.sum()
	diff = newVector.sub(vector)
	sumD = diff.sum()
	
	if (sumD != 0):
		return optimizeP2DVector(dfMatrix, newVector)
	
	return newVector

res = optimizeP2DVector(DFMatrix, dfVector)
writer = pd.ExcelWriter('./2.xlsx', engine='openpyxl')
res.to_excel(writer, sheet_name='1')
writer.close()