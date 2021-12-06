import pygame
from pygame.locals import *

pygame.init()
ventana_x = 619
ventana_y = 540
ventana = pygame.display.set_mode((ventana_x, ventana_y))
pygame.display.set_caption("The Legend of Zelda The Way of the TriForce")
reloj = pygame.time.Clock()
icono=pygame.image.load("Imagenes/TriForce.png")
pygame.display.set_icon(icono)


# Clase Personaje
class personaje(object):

    def __init__(self, x, y):
        self.x = x+165
        self.y = y-17
        self.velocidad = 7
        # Atributos para animación de Sprites
        self.va_izquierda = False
        self.va_derecha = False
        self.va_arriba = False
        self.va_abajo = False
        self.contador_pasos = 0
        self.camina_izquierda = [pygame.image.load("Imagenes/Personaje/Movimiento/Izquierda/I1.png"),
                                 pygame.image.load("Imagenes/Personaje/Movimiento/Izquierda/I2.png"),
                                 pygame.image.load("Imagenes/Personaje/Movimiento/Izquierda/I3.png"),
                                 pygame.image.load("Imagenes/Personaje/Movimiento/Izquierda/I4.png"),
                                 pygame.image.load("Imagenes/Personaje/Movimiento/Izquierda/I5.png"),
                                 pygame.image.load("Imagenes/Personaje/Movimiento/Izquierda/I6.png"),]
        self.camina_derecha = [pygame.image.load("Imagenes/Personaje/Movimiento/Derecha/D1.png"),
                               pygame.image.load("Imagenes/Personaje/Movimiento/Derecha/D2.png"),
                               pygame.image.load("Imagenes/Personaje/Movimiento/Derecha/D3.png"),
                               pygame.image.load("Imagenes/Personaje/Movimiento/Derecha/D4.png"),
                               pygame.image.load("Imagenes/Personaje/Movimiento/Derecha/D5.png"),
                               pygame.image.load("Imagenes/Personaje/Movimiento/Derecha/D6.png"),]
        self.camina_arriba = [pygame.image.load("Imagenes/Personaje/Movimiento/Arriba/Ar1.png"),
                              pygame.image.load("Imagenes/Personaje/Movimiento/Arriba/Ar2.png"),
                              pygame.image.load("Imagenes/Personaje/Movimiento/Arriba/Ar3.png"),
                              pygame.image.load("Imagenes/Personaje/Movimiento/Arriba/Ar4.png"),
                              pygame.image.load("Imagenes/Personaje/Movimiento/Arriba/Ar5.png"),
                              pygame.image.load("Imagenes/Personaje/Movimiento/Arriba/Ar6.png"),
                              pygame.image.load("Imagenes/Personaje/Movimiento/Arriba/Ar7.png"),
                              pygame.image.load("Imagenes/Personaje/Movimiento/Arriba/Ar8.png")]
        self.camina_abajo = [pygame.image.load("Imagenes/Personaje/Movimiento/Abajo/A1.png"),
                            pygame.image.load("Imagenes/Personaje/Movimiento/Abajo/A2.png"),
                            pygame.image.load("Imagenes/Personaje/Movimiento/Abajo/A3.png"),
                            pygame.image.load("Imagenes/Personaje/Movimiento/Abajo/A4.png"),
                            pygame.image.load("Imagenes/Personaje/Movimiento/Abajo/A5.png"),
                            pygame.image.load("Imagenes/Personaje/Movimiento/Abajo/A6.png"),
                            pygame.image.load("Imagenes/Personaje/Movimiento/Abajo/A7.png"),
                            pygame.image.load("Imagenes/Personaje/Movimiento/Abajo/A8.png")]
        self.quieto = pygame.image.load("Imagenes/Personaje/Movimiento/quieto.png")
        self.ancho = self.quieto.get_width()
        self.alto = self.quieto.get_height()
        self.zona_impacto = (self.x, self.y, 58, 65)

        self.vertice_SI = [0, 0]
        self.vertice_SD = [0, 0]
        self.vertice_II = [0, 0]
        self.vertice_ID = [0, 0]
        self.rango_Empuje = 10
        self.holgura_empuje = 3
        self.Cooldown = 0
        self.max_Cooldown = 5
    def dibujar(self, cuadro):
        if self.contador_pasos + 1 > 18:
            self.contador_pasos = 0

        if self.va_izquierda:
            cuadro.blit(self.camina_izquierda[self.contador_pasos // 3], (self.x, self.y))
            self.contador_pasos += 1
        elif self.va_derecha:
            cuadro.blit(self.camina_derecha[self.contador_pasos // 3], (self.x, self.y))
            self.contador_pasos += 1
        elif self.va_arriba:
            cuadro.blit(self.camina_arriba[self.contador_pasos // 3], (self.x, self.y))
            self.contador_pasos += 1
        elif self.va_abajo:
            cuadro.blit(self.camina_abajo[self.contador_pasos // 3], (self.x, self.y))
            self.contador_pasos += 1
        else:
            cuadro.blit(self.quieto, (self.x, self.y))

        self.zona_impacto = (self.x + 10, self.y + 5, 38, 51)
        #pygame.draw.rect(cuadro, (255, 0, 0), self.zona_impacto, 2)

    def se_mueve_segun(self, k, iz, de, ar, ab, barriles):
        if k[iz] and self.x - 80 > self.velocidad:
            self.x -= self.velocidad
            self.Calcular_Vertices()
            if Calculo_Colisiones(self,barriles) == bool(1):
                self.x += self.velocidad
            else:
                self.va_izquierda = True
                self.va_derecha = False
                self.va_abajo = False
                self.va_arriba = False

        elif k[de] and self.x < ventana_x - self.ancho - self.velocidad - 80:
            self.x += self.velocidad
            self.Calcular_Vertices()
            if Calculo_Colisiones(self, barriles) == bool(1):
                self.x -= self.velocidad
            else:
                self.va_derecha = True
                self.va_izquierda = False
                self.va_abajo = False
                self.va_arriba = False

        elif k[ar] and self.y - 50 > self.velocidad:
            self.y -= self.velocidad
            self.Calcular_Vertices()
            if Calculo_Colisiones(self, barriles) == bool(1):
                self.y += self.velocidad
            else:
                self.va_arriba = True
                self.va_abajo = False
                self.va_izquierda = False
                self.va_derecha = False

        elif k[ab] and self.y < ventana_y - self.alto - self.velocidad - 45:
            self.y += self.velocidad
            self.Calcular_Vertices()
            if Calculo_Colisiones(self, barriles) == bool(1):
                self.y -= self.velocidad
            else:
                self.va_abajo = True
                self.va_arriba = False
                self.va_izquierda = False
                self.va_derecha = False

        else:
            # Controles de animación en caso de dejar de moverse en horizonal
            self.va_izquierda = False
            self.va_derecha = False
            self.va_abajo = False
            self.va_arriba = False
            self.contador_pasos = 0

    def empujar_cajas(self, k, q, barriles):
        self.Cooldown -= 1
        if k[q] and self.Cooldown < 0:
            self.Calcular_Vertices()
            self.vertice_a = [self.vertice_SI[0]+self.holgura_empuje, self.vertice_SI[1]-self.rango_Empuje]
            self.vertice_b = [self.vertice_SD[0]-self.holgura_empuje, self.vertice_SD[1]-self.rango_Empuje]
            self.vertice_c = [self.vertice_SD[0]+self.rango_Empuje, self.vertice_SD[1]+self.holgura_empuje]
            self.vertice_d = [self.vertice_ID[0]+self.rango_Empuje, self.vertice_ID[1]-self.holgura_empuje]
            self.vertice_e = [self.vertice_ID[0]-self.holgura_empuje, self.vertice_ID[1]+self.rango_Empuje]
            self.vertice_f = [self.vertice_II[0]+self.holgura_empuje, self.vertice_II[1]+self.rango_Empuje]
            self.vertice_g = [self.vertice_II[0]-self.rango_Empuje, self.vertice_II[1]-self.holgura_empuje]
            self.vertice_h = [self.vertice_SI[0]-self.rango_Empuje, self.vertice_SD[1]+self.holgura_empuje]
            for index in range(len(barriles)):
                if barriles [index].empujable == bool(1):
                    if Punto_dentro(self.vertice_a,barriles[index]) or Punto_dentro(self.vertice_b,barriles[index] ):
                        barriles[index].empujar_caja(0)
                        self.Cooldown = self.max_Cooldown
                        break
                    elif Punto_dentro(self.vertice_c,barriles[index]) or Punto_dentro(self.vertice_d,barriles[index] ):
                        barriles[index].empujar_caja(3)
                        self.Cooldown = self.max_Cooldown
                        break
                    elif Punto_dentro(self.vertice_f,barriles[index]) or Punto_dentro(self.vertice_e,barriles[index] ):
                        barriles[index].empujar_caja(2)
                        self.Cooldown = self.max_Cooldown
                        break
                    elif Punto_dentro(self.vertice_g,barriles[index]) or Punto_dentro(self.vertice_h,barriles[index] ):
                        barriles[index].empujar_caja(1)
                        self.Cooldown = self.max_Cooldown
                        break



# colisiones del personaje

    def Calcular_Vertices(self):
        self.vertice_SI = [self.x+10, self.y+5]
        self.vertice_SD = [self.x+48, self.y+5]
        self.vertice_II = [self.x+10, self.y + 56]
        self.vertice_ID = [self.x+48, self.y + 56]
class meta(object):
    def __init__(self):
        self.vertice_SI = [80,250]
        self.vertice_SD = [100, 250]
        self.vertice_II = [80, 290]
        self.vertice_ID = [100,290]
    def nivel_final(self):
        self.vertice_SI = [290, 250]
        self.vertice_SD = [320, 250]
        self.vertice_II = [290, 290]
        self.vertice_ID = [320, 290]


class caja(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.empujable = bool(1)
        self.velocidad = 7
        self.direccion_dibujo= "Imagenes/Objetos/barril.png"
        self.Dibujo_Caja = pygame.image.load(self.direccion_dibujo)
        self.vertice_SI = [0, 0]
        self.vertice_SD = [0, 0]
        self.vertice_II = [0, 0]
        self.vertice_ID = [0, 0]
        self.moviendose = bool(0)
        self.direccion = 0
        self.Frames_Mov = 0
        self.Frames_Mov_Max = 3
        self.crear_imagen_representacion()

    def crear_imagen_representacion(self):
        self.image = pygame.image.load(self.direccion_dibujo)
        self.ancho = self.image.get_width()
        self.alto = self.image.get_height()

    def dibujar(self, cuadro):
        cuadro.blit(self.Dibujo_Caja, (self.x, self.y))
        self.zona_impacto = (self.x + 0, self.y + 0, self.ancho, self.alto)
        #pygame.draw.rect(cuadro, (255, 255, 255), self.zona_impacto, 2)

    def Calcular_Vertices(self):
        self.vertice_SI = [self.x + 0, self.y+0]
        self.vertice_SD = [self.x+self.ancho, self.y+0]
        self.vertice_II = [self.x+0, self.y+self.alto]
        self.vertice_ID = [self.x+self.ancho, self.y+self.alto]

    def empujar_caja(self, direccion):
        self.moviendose = bool(1)
        self.direccion = direccion
        self.Frames_Mov = 0


    def Mover_Caja(self, barriles): #0 = arriba , 1 = izquierda , 2 = abajo , 3 = derecha

        if self.direccion==1 and self.x - 80 > self.velocidad:
            self.x -= self.velocidad
            self.Calcular_Vertices()
            if Calculo_Colisiones(self, barriles) == bool(1):
                self.x += self.velocidad

        elif self.direccion==3 and self.x < ventana_x - self.ancho - self.velocidad - 80:
            self.x += self.velocidad
            self.Calcular_Vertices()
            if Calculo_Colisiones(self, barriles) == bool(1):
                self.x -= self.velocidad


        elif self.direccion==0 and self.y - 50 >  self.velocidad:
            self.y -= self.velocidad
            self.Calcular_Vertices()
            if Calculo_Colisiones(self, barriles) == bool(1):
                self.y += self.velocidad


        elif self.direccion==2 and self.y < ventana_y - self.alto - self.velocidad - 45:
            self.y += self.velocidad
            self.Calcular_Vertices()
            if Calculo_Colisiones(self, barriles) == bool(1):
                self.y -= self.velocidad

        self.Frames_Mov +=1
        if self.Frames_Mov >= self.Frames_Mov_Max:
            self.moviendose = bool(0)


class Caja2(caja):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.empujable = bool(0)
        self.velocidad = 7
        self.direccion_dibujo= "Imagenes/Objetos/cuadro.png"
        self.Dibujo_Caja = pygame.image.load(self.direccion_dibujo)
        self.vertice_SI = [0, 0]
        self.vertice_SD = [0, 0]
        self.vertice_II = [0, 0]
        self.vertice_ID = [0, 0]
        self.moviendose = bool(0)
        self.direccion = 0
        self.Frames_Mov = 0
        self.Frames_Mov_Max = 3
        self.crear_imagen_representacion()



class Contenedor_Escenario1(object):
    def __init__(self):


        self.link = personaje(int(ventana_x / 2), int(ventana_y / 2))
        self.barriles = [caja(int(ventana_x / 2) + 0, int(ventana_y / 2) - 157)]
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) - 100))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) - 43))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) + 14))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) + 71))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) + 128))


class Contenedor_Escenario2(object):
    def __init__(self):
        self.link = personaje(int(ventana_x / 2), int(ventana_y / 2))
        self.barriles = [caja(int(ventana_x / 2) + 70, int(ventana_y / 2) + 20)]
        self.barriles.append(caja(int(ventana_x / 2) + 120, int(ventana_y / 2) + 75))
        self.barriles.append(caja(int(ventana_x / 2) + 25, int(ventana_y / 2) - 35))
        self.barriles.append(caja(int(ventana_x / 2) - 25, int(ventana_y / 2) - 90))
        self.barriles.append(caja(int(ventana_x / 2) - 140, int(ventana_y / 2) + 75))
        self.barriles.append(caja(int(ventana_x / 2) - 60, int(ventana_y / 2) - 35))
        self.barriles.append(caja(int(ventana_x / 2) - 90, int(ventana_y / 2) + 20))

        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 60, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 10, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 70, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 140, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 120, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 60, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 10, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 70, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 140, int(ventana_y / 2) - 157))



class Contenedor_Escenario3(object):
    def __init__(self):
        self.link = personaje(int(ventana_x / 2), int(ventana_y / 2))
        self.barriles = [caja(int(ventana_x / 2) + 70, int(ventana_y / 2) + 20)]
        self.barriles.append(caja(int(ventana_x / 2) + 120, int(ventana_y / 2) + 75))
        self.barriles.append(caja(int(ventana_x / 2) + 25, int(ventana_y / 2) - 35))
        self.barriles.append(caja(int(ventana_x / 2) - 20, int(ventana_y / 2) - 90))
        self.barriles.append(caja(int(ventana_x / 2) - 60, int(ventana_y / 2) - 150))
        self.barriles.append(caja(int(ventana_x / 2) - 100, int(ventana_y / 2) - 100))
        self.barriles.append(caja(int(ventana_x / 2) - 100, int(ventana_y / 2) - 43))
        self.barriles.append(caja(int(ventana_x / 2) - 100, int(ventana_y / 2) + 14))
        self.barriles.append(caja(int(ventana_x / 2) - 100, int(ventana_y / 2) + 71))
        self.barriles.append(caja(int(ventana_x / 2) - 10, int(ventana_y / 2) + 81))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) + 135))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) + 135))
        self.barriles.append(Caja2(int(ventana_x / 2) - 58, int(ventana_y / 2) + 135))
        self.barriles.append(Caja2(int(ventana_x / 2) + 9, int(ventana_y / 2) + 135))
        self.barriles.append(Caja2(int(ventana_x / 2) + 76, int(ventana_y / 2) + 135))
        self.barriles.append(Caja2(int(ventana_x / 2) + 143, int(ventana_y / 2) + 135))

class Contenedor_Escenario4(object):
    def __init__(self):
        self.link = personaje(int(ventana_x / 2), int(ventana_y / 2))
        self.barriles = [caja(int(ventana_x / 2) + 70, int(ventana_y / 2) + 20)]
        self.barriles.append(caja(int(ventana_x / 2) - 190, int(ventana_y / 2) - 74))
        self.barriles.append(caja(int(ventana_x / 2) - 100, int(ventana_y / 2) - 1))
        self.barriles.append(caja(int(ventana_x / 2) - 100, int(ventana_y / 2) + 70))
        self.barriles.append(caja(int(ventana_x / 2) + 90, int(ventana_y / 2) - 73))
        self.barriles.append(caja(int(ventana_x / 2) + 90, int(ventana_y / 2) + 71))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) + 72))
        self.barriles.append(caja(int(ventana_x / 2) - 1, int(ventana_y / 2) - 2))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) + 72))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 58, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 9, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 76, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 143, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 58, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 9, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 76, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 143, int(ventana_y / 2) - 157))


class Contenedor_Escenario5(object):
    def __init__(self):
        self.link = personaje(int(ventana_x / 2), int(ventana_y / 2))
        self.barriles = [caja(int(ventana_x / 2) + 90, int(ventana_y / 2) + 0)]
        self.barriles.append(caja(int(ventana_x / 2) - 99, int(ventana_y / 2) - 1))
        self.barriles.append(caja(int(ventana_x / 2) - 30, int(ventana_y / 2) + 70))
        self.barriles.append(caja(int(ventana_x / 2) + 120, int(ventana_y / 2) + 75))
        self.barriles.append(caja(int(ventana_x / 2) + 25, int(ventana_y / 2) - 35))
        self.barriles.append(caja(int(ventana_x / 2) - 20, int(ventana_y / 2) - 90))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) + 65))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) - 92))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 58, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 9, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 76, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 143, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 58, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 9, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 76, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 143, int(ventana_y / 2) + 130))


class Contenedor_Escenario10(object):
    def __init__(self):
        self.link = personaje(int(ventana_x / 2), int(ventana_y / 2))
        self.barriles = [caja(int(ventana_x / 2) + 45, int(ventana_y / 2) - 125)]
        self.barriles.append(caja(int(ventana_x / 2) + 99, int(ventana_y / 2) - 70))
        self.barriles.append(caja(int(ventana_x / 2) + 99, int(ventana_y / 2) + 70))
        self.barriles.append(caja(int(ventana_x / 2) + 99, int(ventana_y / 2) + 0))
        self.barriles.append(caja(int(ventana_x / 2) + 45, int(ventana_y / 2) + 125))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) - 71))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) + 71))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) + 1))
        self.barriles.append(caja(int(ventana_x / 2) - 50, int(ventana_y / 2) - 70))
        self.barriles.append(caja(int(ventana_x / 2) - 50, int(ventana_y / 2) + 70))
        self.barriles.append(caja(int(ventana_x / 2) - 50, int(ventana_y / 2) - 125))
        self.barriles.append(caja(int(ventana_x / 2) - 50, int(ventana_y / 2) + 125))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) - 157))

class Contenedor_Escenario9(object):
    def __init__(self):
        self.link = personaje(int(ventana_x / 2), int(ventana_y / 2))
        self.barriles = [caja(int(ventana_x / 2) + 45, int(ventana_y / 2) - 125)]
        self.barriles.append(caja(int(ventana_x / 2) + 99, int(ventana_y / 2) - 70))
        self.barriles.append(caja(int(ventana_x / 2) + 99, int(ventana_y / 2) + 70))
        self.barriles.append(caja(int(ventana_x / 2) + 99, int(ventana_y / 2) + 0))
        self.barriles.append(caja(int(ventana_x / 2) + 45, int(ventana_y / 2) + 125))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) - 71))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) + 71))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) + 1))
        self.barriles.append(caja(int(ventana_x / 2) - 100, int(ventana_y / 2) - 70))
        self.barriles.append(caja(int(ventana_x / 2) - 100, int(ventana_y / 2) + 70))
        self.barriles.append(caja(int(ventana_x / 2) - 50, int(ventana_y / 2) - 126))
        self.barriles.append(caja(int(ventana_x / 2) - 50, int(ventana_y / 2) + 124))
        self.barriles.append(caja(int(ventana_x / 2) - 150, int(ventana_y / 2) + 0))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) + 181))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) + 181))
        self.barriles.append(Caja2(int(ventana_x / 2) - 58, int(ventana_y / 2) + 181))
        self.barriles.append(Caja2(int(ventana_x / 2) + 9, int(ventana_y / 2) + 181))
        self.barriles.append(Caja2(int(ventana_x / 2) + 76, int(ventana_y / 2) + 181))
        self.barriles.append(Caja2(int(ventana_x / 2) + 143, int(ventana_y / 2) + 181))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) - 205))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) - 205))
        self.barriles.append(Caja2(int(ventana_x / 2) - 58, int(ventana_y / 2) - 205))
        self.barriles.append(Caja2(int(ventana_x / 2) + 9, int(ventana_y / 2) - 205))
        self.barriles.append(Caja2(int(ventana_x / 2) + 76, int(ventana_y / 2) - 205))
        self.barriles.append(Caja2(int(ventana_x / 2) + 143, int(ventana_y / 2) - 205))

class Contenedor_Escenario8(object):
    def __init__(self):
        self.link = personaje(int(ventana_x / 2), int(ventana_y / 2))
        self.barriles = [caja(int(ventana_x / 2) + 100, int(ventana_y / 2) - 120)]
        self.barriles.append(caja(int(ventana_x / 2) + 101, int(ventana_y / 2) - 50))
        self.barriles.append(caja(int(ventana_x / 2) + 98, int(ventana_y / 2) + 90))
        self.barriles.append(caja(int(ventana_x / 2) + 99, int(ventana_y / 2) + 20))
        self.barriles.append(caja(int(ventana_x / 2) + 103, int(ventana_y / 2) + 160))
        self.barriles.append(caja(int(ventana_x / 2) + 102, int(ventana_y / 2) - 190))
        self.barriles.append(caja(int(ventana_x / 2) - 101, int(ventana_y / 2) + 161))
        self.barriles.append(caja(int(ventana_x / 2) + 40, int(ventana_y / 2) - 191))
        self.barriles.append(caja(int(ventana_x / 2) - 30, int(ventana_y / 2) - 121))
        self.barriles.append(caja(int(ventana_x / 2) - 103, int(ventana_y / 2) - 49))
        self.barriles.append(caja(int(ventana_x / 2) - 102, int(ventana_y / 2) + 21))
        self.barriles.append(caja(int(ventana_x / 2) - 101, int(ventana_y / 2) + 89))
        self.barriles.append(caja(int(ventana_x / 2) - 20, int(ventana_y / 2) + 19))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) - 157))


class Contenedor_Escenario6(object):
    def __init__(self):
        self.link = personaje(int(ventana_x / 2), int(ventana_y / 2))
        self.barriles = [caja(int(ventana_x / 2) + 0, int(ventana_y / 2) - 0)]
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) - 70))
        self.barriles.append(caja(int(ventana_x / 2) + 0, int(ventana_y / 2) + 70))
        self.barriles.append(caja(int(ventana_x / 2) - 100, int(ventana_y / 2) + 70))
        self.barriles.append(caja(int(ventana_x / 2) - 50, int(ventana_y / 2) - 71))
        self.barriles.append(caja(int(ventana_x / 2) - 100, int(ventana_y / 2) - 69))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 58, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 9, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 76, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 143, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 58, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 9, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 76, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 143, int(ventana_y / 2) - 157))

class Contenedor_Escenario7(object):
    def __init__(self):
        self.link = personaje(int(ventana_x / 2), int(ventana_y / 2))
        self.barriles = [caja(int(ventana_x / 2) + 0, int(ventana_y / 2) - 89)]
        self.barriles.append(caja(int(ventana_x / 2) + 45, int(ventana_y / 2) - 35))
        self.barriles.append(caja(int(ventana_x / 2) - 45, int(ventana_y / 2) - 40))
        self.barriles.append(caja(int(ventana_x / 2) + 90, int(ventana_y / 2) + 20))
        self.barriles.append(caja(int(ventana_x / 2) - 89, int(ventana_y / 2) + 20))
        self.barriles.append(caja(int(ventana_x / 2) - 90, int(ventana_y / 2) + 80))
        self.barriles.append(caja(int(ventana_x / 2) + 90, int(ventana_y / 2) + 80))
        self.barriles.append(caja(int(ventana_x / 2) - 90, int(ventana_y / 2) - 90))
        self.barriles.append(Caja2(int(ventana_x / 2) - 10, int(ventana_y / 2) + 80))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 58, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 9, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 76, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) + 143, int(ventana_y / 2) + 130))
        self.barriles.append(Caja2(int(ventana_x / 2) - 125, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 192, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) - 58, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 9, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 76, int(ventana_y / 2) - 157))
        self.barriles.append(Caja2(int(ventana_x / 2) + 143, int(ventana_y / 2) - 157))

class Contenedor_Escenario11(object):
    def __init__(self):
        self.link = personaje(int(ventana_x / 2) -165, int(ventana_y / 2) +200)
        self.barriles = [caja(int(ventana_x / 2) + 6000, int(ventana_y / 2) + 6000)]



# Función para repintar el cuadro de juego
def repintar_cuadro_juego():
    ventana.blit(imagen_fondo[0], (0, 0))
    # Dibujar Personaje
    Escenario_Activo[0].link.dibujar(ventana)
    for index in range(len(Escenario_Activo[0].barriles)):
        Escenario_Activo[0].barriles[index].dibujar(ventana)
    # Se refresca la imagen
    pygame.display.update()

# calculo de colisiones
def Calculo_Colisiones(personaje, barriles):
    for index in range(len(barriles)):
        if Punto_dentro(personaje.vertice_SI,barriles[index]) or Punto_dentro(personaje.vertice_SD,barriles[index]) or Punto_dentro(personaje.vertice_II,barriles[index]) or Punto_dentro(personaje.vertice_ID,barriles[index]):
            return bool(1)
    return bool(0)

def Llegar_Meta(personaje, meta):
    if Punto_dentro(personaje.vertice_SI,meta) or Punto_dentro(personaje.vertice_SD,meta) or Punto_dentro(personaje.vertice_II,meta) or Punto_dentro(personaje.vertice_ID,meta):
        return bool(1)
    return bool(0)

def Pasar_LVL(personaje, meta, Escenario, Grafica, imagen_fondo):
    if Llegar_Meta(personaje, meta) == bool(1):
        if Grafica.vertice_actual == 0:
            Escenario[0] = Grafica.vertices[Grafica.vertices[Grafica.vertice_actual].vecinos[0]].Nivel_Vertice()
            Grafica.vertice_actual= Grafica.vertices[Grafica.vertice_actual].vecinos[0]
        elif Grafica.vertice_actual== 3.3:
            Escenario[0] = Grafica.vertices[Grafica.vertices[Grafica.vertice_actual].vecinos[1]].Nivel_Vertice()
            Grafica.vertice_actual = Grafica.vertices[Grafica.vertice_actual].vecinos[1]
            imagen_fondo[0] = pygame.image.load("Imagenes/Mapa/FondoNivelFinalR-3.png")
            meta.nivel_final()

        elif Grafica.vertice_actual == 4:
            quit()

        else:
            Escenario[0] = Grafica.vertices[Grafica.vertices[Grafica.vertice_actual].vecinos[1]].Nivel_Vertice()
            Grafica.vertice_actual= Grafica.vertices[Grafica.vertice_actual].vecinos[1]


def reset(k, r, Escenario, Grafica):
    if k[r]:
        Escenario[0] = Grafica.vertices[Grafica.vertice_actual].Nivel_Vertice()






def Punto_dentro(punto_jugador , Vertices_Caja):
    if punto_jugador[0] <= Vertices_Caja.vertice_SD[0] and punto_jugador[0] >= Vertices_Caja.vertice_SI[0] and punto_jugador[1] >= Vertices_Caja.vertice_SI[1]  and punto_jugador[1] <= Vertices_Caja.vertice_II[1]:
        if (punto_jugador[0] == Vertices_Caja.vertice_SD[0] and punto_jugador[1] == Vertices_Caja.vertice_SD[1]) or (punto_jugador[0] == Vertices_Caja.vertice_SI[0] and punto_jugador[1] == Vertices_Caja.vertice_SI[1]) or (punto_jugador[0] == Vertices_Caja.vertice_II[0] and punto_jugador[1] == Vertices_Caja.vertice_II[1]) or (punto_jugador[0] == Vertices_Caja.vertice_ID[0] and punto_jugador[1] == Vertices_Caja.vertice_ID[1]):
            return bool(0)
        else:
            return bool(1)
    else:
        return bool(0)
def Calculo_Vertices_Barriles(barriles):
    for index in range(len(barriles)):
        barriles[index].Calcular_Vertices()
#movimiento de cajas
def mover_Todas_cajas(barriles):
    for index in range(len(barriles)):
       if barriles[index].moviendose== bool(1):
           barriles[index].Mover_Caja(barriles)


#grafo
class Vertice:
    def __init__(self,i):
        self.id =i
        self.visitado = False
        self.nivel=-1
        self.vecinos = []

    def Nivel_Vertice(self):
        if self.id == 0:
            return Contenedor_Escenario1()
        elif self.id == 1.1:
            return Contenedor_Escenario2()
        elif self.id == 1.2:
            return Contenedor_Escenario3()
        elif self.id == 1.3:
            return Contenedor_Escenario4()
        elif self.id == 2.1:
            return Contenedor_Escenario5()
        elif self.id == 2.2:
            return Contenedor_Escenario6()
        elif self.id == 2.3:
            return Contenedor_Escenario7()
        elif self.id == 3.1:
            return Contenedor_Escenario8()
        elif self.id == 3.2:
            return Contenedor_Escenario9()
        elif self.id == 3.3:
            return Contenedor_Escenario10()
        elif self.id == 4:
            return Contenedor_Escenario11()


    def agregaVecino(self,v):
        if not v in self.vecinos:
            self.vecinos.append(v)

class Grafica:
    def __init__(self):
        self.vertices = {}
        self.vertice_actual = 0


    def agregaVertice(self,v):
        if v not in self.vertices:
            self.vertices[v] = Vertice(v)

    def agregarArista(self,a,b):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].agregaVecino(b)
            self.vertices[b].agregaVecino(a)




#Inicio Funcion principal
g = Grafica()
l = [0, 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 4]

for v in l:
    g.agregaVertice(v)

    #l = [0, 1.1, 0 , 1.2, 0, 1.3, 1.1, 2.1, 1.1, 2.2, 1.1, 2.3, 1.2, 2.1, 1.2, 2.2, 1.2, 2.3, 1.3, 2.1, 1.3, 2.2, 1.3, 2.3, 2.1, 3.1, 2.1, 3.2, 2.1, 3.3, 2.2, 3.1, 2.2, 3.2, 2.2, 3.3, 2.3, 3.1, 2.3, 3.2, 2.3, 3.3, 3.1, 4, 3.2, 4, 3.3, 4]
l = [0, 1.1, 1.1, 1.2, 1.2, 1.3, 1.3, 2.1, 2.1, 2.2, 2.2, 2.3, 2.3, 3.1, 3.1, 3.2, 3.2, 3.3, 3.3, 4]
for i in range (0, len(l)-1,2):
    g.agregarArista(l[i], l[i+1])


repetir = True  # Variable que controla la repeticion del juego completo con todas sus pantallas
while repetir:

    # Inicializacion de elementos del juego
    esta_en_intro = True
    menu = True
    puntajes = True
    texto_intro = pygame.font.SysFont('console', 30, True)
    texto_menu = pygame.font.SysFont('console', 45, True)
    texto_titulo = pygame.font.SysFont('console', 80, True)
    texto_pequeno = pygame.font.SysFont('console', 25, True)

    if esta_en_intro == True:
        musica_titulo = pygame.mixer.music.load(
            "Sonidos/Legend Of Zelda Theme (8 Bit Remix Cover Version) [Tribute to NES] - 8 Bit Universe.mp3")
        pygame.mixer.music.play(-1)

    while esta_en_intro:
        reloj.tick(27)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
        pantalla_titulo = pygame.image.load("Imagenes/Titulo.jpg")
        instrucciones = texto_intro.render("Presione ENTER para continuar", 1, (0, 0, 0))

        ventana.blit(pantalla_titulo, (0, 0))
        ventana.blit(instrucciones, ((ventana_x // 2) - instrucciones.get_width() // 2, 470))
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_RETURN]:
            esta_en_intro = False
            menu = True

        pygame.display.update()

    if menu == True:
        musica_titulo = pygame.mixer.music.load(
            "Sonidos/The Legend Of Zelda A Link To The Past - Fairy Theme By 8-Bit Arcade.mp3")
        pygame.mixer.music.play(-1)

    while menu:
        reloj.tick(27)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
        pantalla_menu = pygame.image.load("Imagenes/Menu.jpg")
        ventana.blit(pantalla_menu, (0, 0))
        nueva_partida = texto_menu.render("Nueva Partida - N", 1, (28, 30, 156))
        ventana.blit(nueva_partida, (90, 100))
        puntajes = texto_menu.render("Puntajes - P", 1, (28, 30, 156))
        ventana.blit(puntajes, (160, 230))
        salir = texto_menu.render("Salir - C", 1, (28, 30, 156))
        ventana.blit(salir, (190, 390))

        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_n]:
            menu = False
            puntajes = False
            esta_jugando = True

        if tecla[pygame.K_p]:
            menu = False
            puntajes = True
            esta_jugando = False
            while puntajes:
                reloj.tick(27)
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        quit()
                pantalla_menu = pygame.image.load("Imagenes/Menu.jpg")
                ventana.blit(pantalla_menu, (0, 0))
                titulo = texto_titulo.render("Puntajes", 1, (28, 30, 156))
                ventana.blit(titulo, ((ventana_x // 2) - titulo.get_width() // 2, 0))
                volver = texto_pequeno.render("<- Volver - B ", 1, (28, 30, 156))
                ventana.blit(volver, (0, 510))
                tecla = pygame.key.get_pressed()

                if tecla[pygame.K_b]:
                    menu = True
                    puntajes = False
                    esta_jugando = False

                pygame.display.update()

        if tecla[pygame.K_c]:
            menu = False
            quit()

        pygame.display.update()

    # Creación Personaje Héroe , barriles y cuadros
    Escenario_Activo = [Contenedor_Escenario1()]
    meta = meta()







    # Seccion de juego
    esta_jugando = True
    if esta_jugando == True:
        imagen_fondo = [pygame.image.load("Imagenes/Mapa/FondoNivelR.jpg")]
        musica_fondo = pygame.mixer.music.load("Sonidos/Gerudo Valley - The Legend of Zelda - Ocarina Of Time.mp3")
        pygame.mixer.music.play(-1)
    while esta_jugando:
        # control de velocidad del juego
        reloj.tick(27)
        # evento de boton de cierre de ventana
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()




        teclas = pygame.key.get_pressed()
        Calculo_Vertices_Barriles(Escenario_Activo[0].barriles)
        Escenario_Activo[0].link.empujar_cajas(teclas,pygame.K_q, Escenario_Activo[0].barriles)
        mover_Todas_cajas(Escenario_Activo[0].barriles)
        Escenario_Activo[0].link.se_mueve_segun(teclas, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, Escenario_Activo[0].barriles)
        Pasar_LVL(Escenario_Activo[0].link,meta,Escenario_Activo, g, imagen_fondo)
        reset(teclas, pygame.K_r,Escenario_Activo, g)
        repintar_cuadro_juego()

# Termina el juego y finaliza los elementos de pygame
pygame.quit()


#def asd(self, ventana):
    #pygame.draw.line(ventana, (0, 10, 0), (self.vertice_SI[0], self.vertice_SI[1]), (100, 100), 2)