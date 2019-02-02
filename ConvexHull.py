class ConvexHull(object):
    __matrix = []
    __hull = []

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

        self.__min_max_matrix = self.__find_max_min()

    def __find_max_min(self):
        # Encontra os pontos limites superiores e inferiores dos eixos x e y
        min_x = [self.__x[0], self.__y[0], 0]
        max_x = [self.__x[0], self.__y[0], 0]
        min_y = [self.__x[0], self.__y[0], 0]
        max_y = [self.__x[0], self.__y[0], 0]

        for i in range(len(self.__y)):
            self.__matrix.append([self.__x[i], self.__y[i]])

            if self.__y[i] < min_y[1]:
                min_y = [self.__x[i], self.__y[i], i]
            elif self.__y[i] > max_y[1]:
                max_y = [self.__x[i], self.__y[i], i]

            if self.__x[i] > max_x[0]:
                max_x = [self.__x[i], self.__y[i], i]
            elif self.__x[i] < min_x[0]:
                min_x = [self.__x[i], self.__y[i], i]

        # Garante que 1 pontos não sirva como maior valor para o eixo x e y ao mesmo tempo
        if max_x == min_y:
            max_x = [0, 0, 0]
            for i in range(len(self.__matrix)):
                if self.__matrix[i][0] > max_x[0] and self.__matrix[i] != [min_y[0], min_y[1]]:
                    max_x = [self.__matrix[i][0], self.__matrix[i][1], i]

        if max_x == max_y:
            max_y = min_y
            for i in range(len(self.__matrix)):
                if self.__matrix[i][1] > max_y[1] and self.__matrix[i] != [max_x[0], max_x[1]]:
                    max_y = [self.__matrix[i][0], self.__matrix[i][1], i]

        if min_x == max_y:
            min_x = max_x
            for i in range(len(self.__matrix)):
                if self.__matrix[i][0] < min_x[0] and self.__matrix[i] != [max_y[0], max_y[1]]:
                    min_x = [self.__matrix[i][0], self.__matrix[i][1], i]

        if min_x == min_y:
            min_x = max_x
            for i in range(len(self.__matrix)):
                if self.__matrix[i][0] < min_x[0] and self.__matrix[i] != [min_y[0], min_y[1]]:
                    min_x = [self.__matrix[i][0], self.__matrix[i][1], i]

        # Reorganiza a matriz de pontos colocando os limites nas primeiras posicoes
        # ficando as primeiras posicoes ocupadas com a ordem: min_y, max_x, max_y, min_x
        self.__matrix.remove([min_x[0], min_x[1]])
        self.__matrix.remove([max_y[0], max_y[1]])
        self.__matrix.remove([max_x[0], max_x[1]])
        self.__matrix.remove([min_y[0], min_y[1]])
        self.__matrix.insert(0, [min_x[0], min_x[1]])
        self.__matrix.insert(0, [max_y[0], max_y[1]])
        self.__matrix.insert(0, [max_x[0], max_x[1]])
        self.__matrix.insert(0, [min_y[0], min_y[1]])

        del (min_y[2], max_x[2], max_y[2], min_x[2])

        return [min_y, max_x, max_y, min_x]
