import pulp

peso_calidad = 0.5
peso_costo = 0.5

prob = pulp.LpProblem("Campaña_Publicitaria", pulp.LpMaximize)

x1 = pulp.LpVariable('x1', lowBound=0, upBound=15, cat='Integer')  # Televisión tarde
x2 = pulp.LpVariable('x2', lowBound=0, upBound=10, cat='Integer')  # Televisión noche
x3 = pulp.LpVariable('x3', lowBound=0, upBound=25, cat='Integer')  # Diarios
x4 = pulp.LpVariable('x4', lowBound=0, upBound=4, cat='Integer')   # Revistas
x5 = pulp.LpVariable('x5', lowBound=0, upBound=30, cat='Integer')  # Radio

calidad_total = 83 * x1 + 92 * x2 + 54 * x3 + 73 * x4 + 27 * x5
costo_total = 194 * x1 + 320 * x2 + 68 * x3 + 113 * x4 + 17 * x5
prob += peso_calidad * calidad_total + peso_costo * costo_total, "Función Objetivo Ponderada"

prob += x1 <= 15, "Máx Anuncios Televisión Tarde"
prob += x2 <= 10, "Máx Anuncios Televisión Noche"
prob += x3 <= 25, "Máx Anuncios Diarios"
prob += x4 <= 4, "Máx Anuncios Revistas"
prob += x5 <= 30, "Máx Anuncios Radio"

prob += 194 * x1 + 320 * x2 <= 3800, "Máx Costo Televisión"
prob += 68 * x3 + 113 * x4 <= 2800, "Máx Costo Diarios y Revistas"
prob += 68 * x3 + 17 * x5 <= 3500, "Máx Costo Diarios y Radio"

prob.solve()

# Mostrar resultados
estado = pulp.LpStatus[prob.status]
funcion_objetivo_ponderada = pulp.value(prob.objective)
resultados = {v.name: v.varValue for v in prob.variables()}
costo_total = 194 * resultados['x1'] + 320 * resultados['x2'] + 68 * resultados['x3'] + 113 * resultados['x4'] + 17 * resultados['x5']
calidad_total = 83 * resultados['x1'] + 92 * resultados['x2'] + 54 * resultados['x3'] + 73 * resultados['x4'] + 27 * resultados['x5']

print("Estado:", estado)
print("Función Objetivo Ponderada:", funcion_objetivo_ponderada)
for nombre, valor in resultados.items():
    print(f"{nombre} = {valor}")

print("Costo Total:", costo_total)
print("Calidad Total:", calidad_total)
