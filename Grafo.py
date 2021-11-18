class Vertice:
    def __init__(self,i):
        self.id =i
        self.visitado = False
        self.nivel=-1
        self.vecinos = []

    def agregaVecino(self,v):
        if not v in self.vecinos:
            self.vecinos.append(v)

class Grafica:
    def __init__(self):
        self.vertices = {}

    def agregaVertice(self,v):
        if v not in self.vertices:
            self.vertices[v] = Vertice(v)

    def agregarArista(self,a,b):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].agregaVecino(b)
            self.vertices[b].agregaVecino(a)

def main():

    g = Grafica()

    l = [0, 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 4]

    for v in l:
        g.agregaVertice(v)

    l = [0, 1.1, 0, 1.2, 0, 1.3, 1.1, 2.1, 1.1, 2.2, 1.1, 2.3, 1.2, 2.1, 1.2, 2.2, 1.2, 2.3, 1.3, 2.1, 1.3, 2.2, 1.3, 2.3, 2.1, 3.1, 2.1, 3.2, 2.1, 3.3, 2.2, 3.1, 2.2, 3.2, 2.2, 3.3, 2.3, 3.1, 2.3, 3.2, 2.3, 3.3, 3.1, 4, 3.2, 4, 3.3, 4]

    for i in range (0, len(l)-1,2):
        g.agregarArista(l[i], l[i+1])

    for v in g.vertices:
        print(v,g.vertices[v].vecinos)

main()