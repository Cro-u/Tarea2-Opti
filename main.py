import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.lines import Line2D

from RSA import RSA

T = 300
rep = 30

all_fitness, lastIter_list = [], []

def dominates(sol1, sol2):
    return all(x <= y for x, y in zip(sol1, sol2)) and any(x < y for x, y in zip(sol1, sol2))

def extract_non_dominated(solutions):
    non_dominated = []
    for sol in solutions:
        is_dominated = False
        for other_sol in solutions:
            if dominates(other_sol, sol):
                is_dominated = True
                break
        if not is_dominated:
            non_dominated.append(sol)
    return non_dominated

def combine_and_extract_pareto(fronts):
    combined_front = []
    for front in fronts:
        combined_front.extend(front)
    return extract_non_dominated(combined_front)

all_pareto_fronts = []
for _ in range(rep):
    fitness, solutions, lastIter = RSA(T, 10).solve()
    all_fitness.append(fitness)
    lastIter_list.append(lastIter)
    pareto_solutions = extract_non_dominated(solutions)
    all_pareto_fronts.append(pareto_solutions)

global_pareto_front = combine_and_extract_pareto(all_pareto_fronts)

objectives1 = [sol[0] for sol in global_pareto_front]
objectives2 = [sol[1] for sol in global_pareto_front]

with open("data/fitness3.csv", mode="w", newline="") as f:
    for data in all_fitness:
        csv.writer(f).writerow(data)
with open("data/iter3.csv", mode="w", newline="") as f:
    csv.writer(f).writerow(lastIter_list)

def data(results):
    media, mediana, std, rqi, min, max = [], [], [], [], [], []
    for d in results:
        m = np.mean(d)
        med = np.median(d)
        s = np.std(d)
        r = np.percentile(results, 75) - np.percentile(results, 25)
        mn = np.min(d)
        mx = np.max(d)

        media.append(m)
        mediana.append(med)
        std.append(s)
        rqi.append(r)
        min.append(mn)
        max.append(mx)
    print(f'Media: {np.mean(media):.2e}')
    print(f'Mediana: {np.median(mediana):.2e}')
    print(f'Desviación Estandar: {np.std(std):.2e}')
    print(f'IQR: {np.mean(rqi):.2e}')
    print(f'Min: {np.min(min):.2e}')
    print(f'Max: {np.max(max):.2e}')
data(all_fitness)

def graf2d(x1):
    # Creamos la figura
    fig, ax = plt.subplots()

    # Generamos los ejes x para la función Max Z
    T = len(x1[0])  # Número de iteraciones
    X = np.linspace(0, T-1, T)
    Z1 = np.array(x1)

    # Calculamos la media de los valores en cada iteración
    media_Z1 = np.mean(Z1, axis=0)

    # Graficamos las líneas de la media
    ax.plot(X, media_Z1, color='blue', linewidth=2, label='Media Max Z')

    ax.axvline(np.mean(lastIter_list), color='black', linestyle='--', linewidth=1, label='Última Iteración Media')

    # Graficamos las líneas para cada iteración por separado
    for i in range(Z1.shape[0]):
        ax.plot(X, Z1[i], color='green', alpha=0.7, label='Max Z' if i == 0 else "")

    # Etiquetamos los ejes
    ax.set_xlabel('Iteraciones')
    ax.set_ylabel('Valores obtenidos')

    # Crear proxies para la leyenda
    legend_elements = [Line2D([0], [0], color='green', lw=1, label='Max Z')]

    ax.legend(handles=legend_elements, loc='best')

    # Mostramos la gráfica
    plt.show()
graf2d(all_fitness)

def graf2d_a(x1):
    # Creamos la figura
    fig, ax = plt.subplots()

    # Generamos los ejes x para la función Max Z
    T = len(x1[0])  # Número de iteraciones
    X = np.linspace(0, T-1, T)
    Z1 = np.array(x1)

    # Calculamos la media de los valores en cada iteración
    media_Z1 = np.mean(Z1, axis=0)

    # Graficamos las líneas de la media
    ax.plot(X, media_Z1, color='blue', linewidth=2, label='Media Max Z')

    # Línea vertical para la última iteración media
    ax.axvline(np.mean(lastIter_list), color='black', linestyle='--', linewidth=1, label='Última Iteración Media')

    # Etiquetamos los ejes
    ax.set_xlabel('Iteraciones')
    ax.set_ylabel('Valores obtenidos')

    # Crear proxies para la leyenda
    legend_elements = [
        Line2D([0], [0], color='blue', lw=2, label='Media Max Z'),
        Line2D([0], [0], color='black', lw=1, linestyle='--', label='Última Iteración Media')
    ]

    ax.legend(handles=legend_elements, loc='best')

    # Mostramos la gráfica
    plt.show()
graf2d_a(all_fitness)

plt.scatter(objectives1, objectives2)
plt.title('Frente de Pareto Global')
plt.xlabel('Objetivo 1')
plt.ylabel('Objetivo 2')
plt.show()