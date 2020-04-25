import pygame, sys
from pygame.locals import *
from random import randint

# variables globales
ancho = 900
alto = 400
listaEnemigo = []

class naveEspacial(pygame.sprite.Sprite):
    """Clase naves"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.ImagenNave = pygame.image.load("img/paolajuego.png")
        self.ImagenExplosion = pygame.image.load("IMG/explosion.jpg")

        self.rect = self.ImagenNave.get_rect()
        self.rect.centerx = ancho/2
        self.rect.centery = alto-30

        #disparo
        self.listaDisparo = []
        self.Vida = True #vida

        #velocidad
        self.velocidad = 20

        self.sonidoDisparo = pygame.mixer.Sound("MUSIC/disparo2.wav")
        self.sonidoExplosion = pygame.mixer.Sound("MUSIC/explosi_on.wav")

    #control pantalla
    def movimientoDerecha(self):
        self.rect.right += self.velocidad
        self.__movimiento()

    def movimientoIzquierda(self):
        self.rect.left -= self.velocidad
        self.__movimiento()

    def __movimiento(self):
        if self.Vida == True:
            if self.rect.left <= 0:
                self.rect.left =0
            elif self.rect.right>900:
                self.rect.right = 899

    def disparar(self,x,y):
        miProyectil = Proyectil(x,y,"IMG/disparoa.jpg", True)
        self.listaDisparo.append(miProyectil)
        self.sonidoDisparo.play()

    def destruccion(self):
        self.sonidoExplosion.play()
        self.Vida= False
        self.velocidad= 0
        self.ImagenNave = self.ImagenExplosion

    def dibujar(self, superficie):
        superficie.blit(self.ImagenNave, self.rect)

class Proyectil(pygame.sprite.Sprite): #proyectil
    def __init__(self, posx, posy, ruta, personaje):
        pygame.sprite.Sprite.__init__(self)

        self.imagenProyectil = pygame.image.load(ruta)

        self.rect = self.imagenProyectil.get_rect()

        self.velocidadDisparo = 3

        #direccion
        self.rect.top = posy
        self.rect.left = posx

        self.disparoPersonaje = personaje # boleano Disparo

    def trayectoria(self):
        if self.disparoPersonaje == True:
            self.rect.top = self.rect.top - self.velocidadDisparo
        else:
            self.rect.top = self.rect.top + self.velocidadDisparo

    def dibujar(self, superficie):
        superficie.blit(self.imagenProyectil, self.rect)

class Invasor(pygame.sprite.Sprite): #proyectil
    def __init__(self, posx, posy, distancia, imagenUno, imagenDos):
        pygame.sprite.Sprite.__init__(self)

        self.imagenA = pygame.image.load(imagenUno)
        self.imagenB = pygame.image.load(imagenDos)

        self.listaImagenes = [self.imagenA, self.imagenB]
        self.posImagen = 0

        self.imagenInvasor = self.listaImagenes[self.posImagen]
        self.rect = self.imagenInvasor.get_rect()
        
        self.listaDisparo = []
        self.velocidad = 5
        self.rect.top = posy
        self.rect.left = posx

        self.rangoDisparo = 5 
        self.tiempoCambio = 1 #cambio
        self.conquista = False #consquista jugador
        self.derecha = True #moviento enemigo
        self.contador = 0
        self.Maxdescenso = self.rect.top+ 40

        self.limiteDeracha = posx + distancia
        self.limiteIzquierda = posx - distancia

    def dibujar(self, superficie):
        self.imagenInvasor = self.listaImagenes[self.posImagen]
        superficie.blit(self.imagenInvasor, self.rect)

    def comportamiento(self, tiempo):
        if self.conquista == False:
            self.__movimiento()

        self.__ataque()
        if self.tiempoCambio == tiempo:
            self.posImagen +=1 #cambio de enemigo
            self.tiempoCambio += 1
            
            if self.posImagen > len(self.listaImagenes)-1:
                self.posImagen = 0 # regreso valor =
    
    def __movimiento(self):
        if self.contador < 3:
            self.__movimientoLateral()
        else:
            self.__descenso()
    
    def __descenso(self):
        if self.Maxdescenso == self.rect.top:
            self.contador = 0
            self.Maxdescenso = self.rect.top +30
        else:
            self.rect.top +=1

    def __movimientoLateral(self):
        if self.derecha == True:
            self.rect.left = self.rect.left+ self.velocidad
            if self.rect.left >  self.limiteDeracha:
                self.derecha = False

                self.contador += 1
        else:
            self.rect.left = self.rect.left - self.velocidad
            if self.rect.left < self.limiteIzquierda:
                self.derecha = True

    def __ataque(self):
        if (randint(0,100)<self.rangoDisparo):
            self.__disparo()

    def __disparo(self):
        x,y = self.rect.center
        miProyectil = Proyectil(x,y, "IMG/disparob.jpg", False)
        self.listaDisparo.append(miProyectil)

def detenerTodo():
    for enemigo in listaEnemigo:
        for disparo in enemigo.listaDisparo:
            enemigo.listaDisparo.remove(disparo)

            enemigo.conquista = True

def cargarEnemigos():
    posx = 100
    for x in range(1,5):
        enemigo = Invasor(posx,100,100,'IMG/marcianoA.jpg','IMG/MarcianoB.jpg')
        listaEnemigo.append(enemigo)
        posx = posx + 200

    posx = 100
    for x in range(1,5):
        enemigo = Invasor(posx,40,100,'IMG/Marciano2A.jpg','IMG/Marciano2B.jpg')
        listaEnemigo.append(enemigo)
        posx = posx + 200

    posx = 100    
    for x in range(1,5):
        enemigo = Invasor(posx,-100,40,'IMG/Marciano3A.jpg','IMG/Marciano3B.jpg')
        listaEnemigo.append(enemigo)
        posx = posx + 200

def SpaceF():
    pygame.init()
    start_time=pygame.time.get_ticks()
    venta = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Space LoL")

    #musica fondo
    pygame.mixer.music.load('MUSIC/Bionicle_Heroes_Intro_Nintendo_DS.mp3')
    pygame.mixer.music.play(3)

    #fondo
    ImagenFondo = pygame.image.load("IMG/Fondo.jpg")

    miFuente = pygame.font.Font(None,30)
    Texto = miFuente.render("Fin del Juego",0,(200,200,100))

    jugador = naveEspacial()
    cargarEnemigos()

    

    SJuego = True

    #reloj
    reloj = pygame.time.Clock()
    while True:

        reloj.tick(60)

        tiempo = int((pygame.time.get_ticks()-start_time)/1000)

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()

            #teclado
            if SJuego == True:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == K_LEFT:
                        jugador.movimientoIzquierda()
                    
                    elif evento.key == K_RIGHT:
                        jugador.movimientoDerecha()
                    
                    #disparo tecla
                    elif evento.key == K_s:
                        x, y = jugador.rect.center
                        jugador.disparar(x,y)

        venta.blit(ImagenFondo,(0,0))

        jugador.dibujar(venta)

        if len(jugador.listaDisparo) > 0:
            for x in jugador.listaDisparo:
                x.dibujar(venta)
                x.trayectoria()

                if x.rect.top <-10:
                    jugador.listaDisparo.remove(x)
                else:
                    for enemigo in listaEnemigo:
                        if x.rect.colliderect(enemigo.rect):
                            listaEnemigo.remove(enemigo)
                            jugador.listaDisparo.remove(x)

        if len(listaEnemigo) >0:
            for enemigo in listaEnemigo:
                enemigo.comportamiento(tiempo)
                enemigo.dibujar(venta)
                
                if enemigo.rect.colliderect(jugador.rect):
                    jugador.destruccion()
                    SJuego = False
                    detenerTodo()

                if len(enemigo.listaDisparo) > 0:
                    for x in enemigo.listaDisparo:
                        x.dibujar(venta)
                        x.trayectoria()

                        if x.rect.colliderect(jugador.rect):
                            jugador.destruccion()
                            SJuego = False
                            detenerTodo()

                        if x.rect.top >900:
                           enemigo.listaDisparo.remove(x)
                        else:
                            for disparo in jugador.listaDisparo:
                                if x.rect.colliderect(disparo.rect):
                                    jugador.listaDisparo.remove(disparo)
                                    enemigo.listaDisparo.remove(x)
            
        if SJuego == False:
            pygame.mixer.music.fadeout(3000)
            venta.blit(Texto,(400,220))

        pygame.display.update()

SpaceF()
