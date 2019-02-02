from ConvexHull import ConvexHull
from random import uniform

dados_x = []
dados_y = []
for _ in range(18):
    dados_x.append(round(uniform(0, 10), 2))
    dados_y.append(round(uniform(0, 10), 2))

print(f'dados_x = {dados_x}\ndados_y = {dados_y}')

c_hull = ConvexHull(dados_x, dados_y)
print(f'\nhull: {c_hull.hull}')
c_hull.plot_hull()
