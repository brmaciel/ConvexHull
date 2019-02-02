from math import atan2, pi


class ConvexHull(object):
    __matrix = []
    __hull = []

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

        self.__min_max_matrix = self.__find_max_min()
        self.__make_hull()

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

        # Garante que 1 pontos não sirva como maior/menor valor para o eixo x e y ao mesmo tempo
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

    def __make_hull(self):
        self.__hull.append(self.__min_max_matrix[0])  # add min_y como ponto inicial

        self.__find_next_point(self.__hull[0], checkpoint=1)

    def __find_next_point(self, current_pt, checkpoint):
        # Funcao recursiva para calculo do proximo ponto que compoe o hull
        # checkpoint define qual ponto (min_y, max_x, max_y, min_x) foi o ultimo alcançado
        # pois o calculo do angulo varia de acordo com o checkpoint atual
        angle = 7  # em radianos

        for i in range(checkpoint, len(self.__matrix)):
            resp = self.__compute_angle(current_pt, self.__matrix[i])
            if checkpoint == 1 and resp < angle:
                angle = resp
                new_pt = [self.__matrix[i][0], self.__matrix[i][1], i]
            elif checkpoint == 2 and (pi / 2) < resp < angle:
                angle = resp
                new_pt = [self.__matrix[i][0], self.__matrix[i][1], i]
            elif checkpoint == 3 and pi < resp < angle:
                angle_to_1st_pt = self.__compute_angle(current_pt, self.__hull[0])
                if resp < angle_to_1st_pt:
                    angle = resp
                    new_pt = [self.__matrix[i][0], self.__matrix[i][1], i]
                else:
                    angle = angle_to_1st_pt
                    new_pt = [self.__hull[0][0], self.__hull[0][1], i]
            elif checkpoint == 4 and (3 * pi / 2) < resp < angle:
                angle_to_1st_pt = self.__compute_angle(current_pt, self.__hull[0])
                if resp < angle_to_1st_pt:
                    angle = resp
                    new_pt = [self.__matrix[i][0], self.__matrix[i][1], i]
                else:
                    angle = angle_to_1st_pt
                    new_pt = [self.__hull[0][0], self.__hull[0][1], i]
            elif (checkpoint == 4 or checkpoint == 3) and i == len(self.__matrix) - 1 and angle == 7:
                new_pt = [self.__hull[0][0], self.__hull[0][1], i]

        # Verifica se alcancou um novo checkpoint
        for i in range(len(self.__min_max_matrix)):
            if [new_pt[0], new_pt[1]] == self.__min_max_matrix[i]:
                checkpoint = i + 1

        # remove o ponto encontrado da matrix pois ele não é mais candidato para ser o proximo ponto do hull
        if [new_pt[0], new_pt[1]] != self.__matrix[checkpoint - 1]:
            del (self.__matrix[new_pt[2]])
        del (new_pt[2])
        self.__hull.append(new_pt)

        # Funcao recursiva termina quando o ponto inicial é alcancado
        if new_pt != self.__hull[0]:
            self.__find_next_point(new_pt, checkpoint)

    @staticmethod
    def __compute_angle(initial_pt, final_pt):
        # Calcula o angulo formado entre 2 pontos
        x0 = initial_pt[0]
        y0 = initial_pt[1]
        x1 = final_pt[0]
        y1 = final_pt[1]

        angle = atan2(y1 - y0, x1 - x0)  # retorna valores entre (-pi e pi)
        # transforma os valores para (0 a 2pi)
        if angle < 0:
            angle += 2 * pi

        return angle


from random import uniform

dados_x = []
dados_y = []
for _ in range(18):
    dados_x.append(round(uniform(0, 10), 2))
    dados_y.append(round(uniform(0, 10), 2))

print(f'dados_x = {dados_x}\ndados_y = {dados_y}')
c_hull = ConvexHull(dados_x, dados_y)
