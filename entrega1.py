from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    limited_depth_first,
    iterative_limited_depth_first,
    astar,
    greedy,
)
from simpleai.search.viewers import WebViewer, BaseViewer

def jugar(paredes, cajas, objetivos, jugador, maximos_movimientos):

    INICIAL = (jugador, maximos_movimientos , tuple(cajas))
    PAREDES = tuple(paredes)
    CAJAS_OK = tuple(objetivos)
    META = len(CAJAS_OK)
    ANCHO = max(PAREDES)[0]
    LARGO = max(PAREDES)[1]
    secuencia = []

    def hay_caja(posicion, cajas):
        for caja in cajas:
            if caja == posicion:
                return True
        return False


    def casillero_valido(nueva_posicion):
        for pared in PAREDES:
            if pared == nueva_posicion:
                return False
        return True

    

    class SocobanProblem(SearchProblem):
        def is_goal(self, state):
            posicion, maximos_movimientos, cajas = state
            correctas = 0
            for caja in cajas:
                for ok in CAJAS_OK:
                    if ok == caja:
                        correctas += 1
            #print(META == correctas and maximos_movimientos > 0)
            return META == correctas and maximos_movimientos > 0
        
        def cost(self, state, action, state2):
            return 1
        
        def heuristic(self, state):
            posicion, maximos_movimientos, cajas = state
            distancias = []
            correctas = 0
            for caja in cajas:
                distancias.append(abs(posicion[0]-caja[0])+abs(posicion[1]-caja[1])-1) 
                for ok in CAJAS_OK:
                    if ok == caja:
                        correctas += 1
            #print("Dist",distancias)
            #print("PorRes",META - correctas)
            #print("HEURISTIC", META - correctas + min(distancias))
            return META - correctas + min(distancias)
            
            

        def actions(self, state):
            posicion, maximos_movimientos, cajas = state
            acciones_posibles = []

            #Sin movimientos
            if maximos_movimientos == 0:
                return acciones_posibles

            #Para que casilla puedo moverme, Hay caja en esa casilla?, La Caja puede moverse a la siguiente?
            if posicion[0] > 0:
                if casillero_valido((posicion[0]-1, posicion[1])): 
                    if hay_caja((posicion[0]-1, posicion[1]), cajas): 
                        if casillero_valido((posicion[0]-2, posicion[1])): 
                            if not hay_caja((posicion[0]-2, posicion[1]), cajas): 
                                acciones_posibles.append(((posicion[0]-1, posicion[1]),"arriba")) 
                    else:
                        acciones_posibles.append(((posicion[0]-1, posicion[1]),"arriba"))

            if posicion[0] < ANCHO:
                if casillero_valido((posicion[0]+1, posicion[1])):
                    if hay_caja((posicion[0]+1, posicion[1]), cajas):
                        if casillero_valido((posicion[0]+2, posicion[1])):
                            if not hay_caja((posicion[0]+2, posicion[1]), cajas):
                                acciones_posibles.append(((posicion[0]+1, posicion[1]),"abajo"))
                    else:
                        acciones_posibles.append(((posicion[0]+1, posicion[1]),"abajo"))

            if posicion[1] > 0:
                if casillero_valido((posicion[0], posicion[1]-1)):
                    if hay_caja((posicion[0], posicion[1]-1), cajas):
                        if casillero_valido((posicion[0], posicion[1]-2)):
                            if not hay_caja((posicion[0], posicion[1]-2), cajas):
                                acciones_posibles.append(((posicion[0], posicion[1]-1),"izquierda"))
                    else:
                        acciones_posibles.append(((posicion[0], posicion[1]-1),"izquierda"))

            if posicion[1] < LARGO:
                if casillero_valido((posicion[0], posicion[1]+1)):
                    if hay_caja((posicion[0], posicion[1]+1), cajas):
                        if casillero_valido((posicion[0], posicion[1]+2)):
                            if not hay_caja((posicion[0], posicion[1]+2), cajas):
                                acciones_posibles.append(((posicion[0], posicion[1]+1),"derecha"))
                    else:
                        acciones_posibles.append(((posicion[0], posicion[1]+1),"derecha"))

            #print("acciones",acciones_posibles)
            return acciones_posibles
            
                   
        def result(self, state, action):
            posicion, maximos_movimientos, cajas = state
            posicion_nueva, accion = action
            estado_cajas = []
            mov_fil = posicion_nueva[0] - posicion[0] 
            mov_col = posicion_nueva[1] - posicion[1] 

            for caja in cajas:
                if caja == posicion_nueva:
                    estado_cajas.append((caja[0]+mov_fil,caja[1]+mov_col))
                else:
                    estado_cajas.append(caja)
            
            #print("esrcaj",estado_cajas)
            #print("nuevo estado",(posicion_nueva,maximos_movimientos-1,tuple(estado_cajas)))
            return (posicion_nueva,maximos_movimientos-1,tuple(estado_cajas))
            
        
            
    
    if __name__ == "__main__":
        viewer = BaseViewer()
        #viewer = WebViewer()
        result = astar(SocobanProblem(INICIAL), viewer=viewer, graph_search=True)

        print("Meta:",result.state)

        for action, state in result.path():
            if action != None:
                secuencia.append(action[1])
            #else:
            #    print("NNNNNNNNNOOOOOONEEEEEEEEEEE")

        print("Profundidad:", len(list(result.path())))
        print("Costo",result.cost)
        print("Stats:",viewer.stats)
        return secuencia
    else:
        viewer = BaseViewer()
        result = astar(SocobanProblem(INICIAL), graph_search=True)
        for action, state in result.path():
            if action != None:
                secuencia.append(action[1])
        return secuencia
    


if __name__ == "__main__":
    paredes = [
        (0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
        (1,0),(1,6),
        (2,0),(2,6),
        (3,0),(3,3),(3,4),(3,5),(3,6),
        (4,0),(4,3),(4,6),
        (5,0),(5,6),
        (6,0),(6,6),
        (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6)
    ]
    objetivos = [(4,4)]
    cajas = [(2,4)]
    jugador = (1,2)
    movimientos = 30
    
    secuencia = jugar(paredes, cajas, objetivos, jugador, movimientos)
    print(secuencia)

