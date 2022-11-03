from itertools import combinations
from simpleai.search import CspProblem, backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE, HIGHEST_DEGREE_VARIABLE

def armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):

    paredes = []
    cajas = []
    objetivos = []
    esquinas = [(0,0),(filas-1,0),(0,columnas-1),(filas-1,columnas-1)]

    for pared in range(cantidad_paredes):
        paredes.append('pared'+str(pared))

    for caja_objetivo in range(cantidad_cajas_objetivos):
        cajas.append('caja'+str(caja_objetivo))
        objetivos.append('obj'+str(caja_objetivo))

    variables = ['Jugador'] + cajas + objetivos + paredes
    print(variables)
    #/////////////////////////////////////////////////////////////////
    dominios = {}

    for var in variables:
        dominio_var = []
        for fila in range(filas):
            for col in range(columnas): 
                if var in cajas:
                    if (fila,col) not in esquinas:
                        dominio_var.append((fila,col))
                else:
                    dominio_var.append((fila,col))
        dominios[var] = dominio_var

    #print(dominios)
    #//////////////////////////////////////////////////////////////////

    restricciones = []

    def distinta_posicion(variables,values):
        pos_obj1, pos_obj2 = values
        return pos_obj1 != pos_obj2

    for obj1, obj2 in combinations(["Jugador"]+paredes+cajas,2):
        restricciones.append(((obj1,obj2),distinta_posicion))

    def distinta_posicion_paredobjetivo(variables,values):
        pos_pared, pos_objetivo = values
        return pos_pared != pos_objetivo

    for pared, objetivo in combinations(paredes+objetivos,2):
        restricciones.append(((pared,objetivo),distinta_posicion_paredobjetivo))

    def distinta_posicion_objetivo(variables,values):
        pos_pared, pos_objetivo = values
        return pos_pared != pos_objetivo

    for v1, v2 in combinations(objetivos,2):
        restricciones.append(((v1,v2), distinta_posicion_objetivo))

    def caja_contra_pared(posicion):
        return posicion[0] == 0 or posicion[0] == filas-1 or posicion[1] == 0 or posicion[1] == columnas-1

    def hasta_una_pared_adyacente (variables, values):
        caja , *paredes = values
        print("CAJA",caja)
        print("PAREDES",paredes)
        
        cantidad_paredes_adyacentes = 0

        if caja_contra_pared:
            cantidad_paredes_adyacentes += 1

        posiciones_adyacentes = [(caja[0]+1,caja[1]),(caja[0]-1,caja[1]),(caja[0],caja[1]+1),(caja[0],caja[1]-1)]
        for adyacente in posiciones_adyacentes:
            for pared in paredes:  
                if pared == adyacente:
                    cantidad_paredes_adyacentes += 1
        print(cantidad_paredes_adyacentes)
        return cantidad_paredes_adyacentes < 2


    for caja in cajas:
        if len(paredes) > 1:
            for pared1, pared2 in combinations(paredes,2):
                restricciones.append(((caja,pared1,pared2), hasta_una_pared_adyacente))
        else:
            restricciones.append((([caja]+paredes), hasta_una_pared_adyacente))


    socobanProblem = CspProblem(variables, dominios, restricciones)

    solucion = backtrack(
        socobanProblem,
        inference=False,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
        value_heuristic=LEAST_CONSTRAINING_VALUE,
    )

    resultado_paredes = []
    for pared in paredes:
        resultado_paredes.append(solucion[pared])

    resultado_objetivos = []
    for objetivo in objetivos:
        resultado_objetivos.append(solucion[objetivo])

    resultado_cajas = []
    for caja in cajas:
        resultado_cajas.append(solucion[caja])


    print(solucion)
    return (resultado_paredes, resultado_cajas, resultado_objetivos, solucion['Jugador'])

if __name__ == "__main__":
    mapa_resultante = armar_mapa(5,5,4,2)
    print(mapa_resultante)