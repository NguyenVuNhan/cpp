class Matrix():
    def __init__(self):
        self.setPoint = []
        self.setPointLen = 0
        pass

    def refresh(self):
        self.setPoint = []
        self.setPointLen= 0

    def addSetPoint(self, x, y):
        self.setPoint.append([x,y])
        self.setPointLen += 1

    def createMatrix(self):
        m = []
        for i in range(self.setPointLen):
            r = []
            for j in range(self.setPointLen):
                r.append(self.setPoint[i][0]**j)
            m.append(r)
        return m

    def inverseMatrix(self, matrix):
        def matrixMinor(matrix, i, j):
            return [row[:j] + row[j+1:] for row in (matrix[:i]+matrix[i+1:])]

        def getDeterminant(matrix):
            if ( len(matrix) == 2  ):
                return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
            
            determinant = 0
            for i in range(len(matrix)):
                determinant += ((-1)**i)*matrix[0][i]*getDeterminant(matrixMinor(matrix, 0, i))

            return determinant


        determinant = getDeterminant(matrix)

        inverseMatrix = []
        for i in range(len(matrix)):
            row = []
            for j in range(len(matrix)):
                minor = matrixMinor(matrix, i, j)
                row.append(((-1)**(i+j)) * getDeterminant(minor))
            inverseMatrix.append(row)

        inverseMatrix = list(map(list, zip(*inverseMatrix))) # Transpose matrix
        for i in range(len(inverseMatrix)):
            for j in range(len(inverseMatrix)):
                inverseMatrix[i][j] /= determinant
        
        return inverseMatrix

    def matrixMul(self, matrixA, matrixB):
        zip_b = list(zip(*matrixB))
        return [[sum(ele_a*ele_b for ele_a, ele_b in zip((row_a if type(row_a) == list else [row_a]), col_b)) for col_b in zip_b] for row_a in matrixA]

    def getVector(self, method="Gaussian"):
        if (method == "Gaussian"):
            m = self.createMatrix()
            for i in range(len(m)):
                m[i].append(self.setPoint[i][1])
            
            # Gaussian
            for j in range(len(m)):
                for i in range(len(m)):
                    if ( i != j ):
                        try:
                            quotion = m[i][j] / m[j][j]
                        except:
                            print(m[i][j], m[j][j])
                        for k in range(len(m)+1):
                            m[i][k] -= quotion*m[j][k]
            try:
                vector = [ m[i][len(m)]/m[i][i] for i in range(len(m)) ]
                return vector
            except ZeroDivisionError:
                return [0]


        elif (method == "Normal"):
            inverseMatrix = self.inverseMatrix(self.createMatrix())

            y = [ [point[1]] for point in self.setPoint ]

            return [m[0] for m in self.matrixMul(inverseMatrix, y)]

        return []
