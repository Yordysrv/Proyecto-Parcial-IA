# Proyecto-parcial-IA

## Nombre : (Yordys Rodriguez Valerio)

## Matrícula: (15-EISN-2-045)

## Proyecto: Mi juego es basado en alien breed el jugador es persequido en un mundo por una imbacion de alien  el cual deve sobrevibir disparando hacia los alien.

## link del repositorio es : https://github.com/Yordysrv/Proyecto-Parcial-IA
 

 ###DOCUMENTACIÓN COMPLETA DEL CÓDIGO
Juego: Alien Breed - Scroll - A - Nivel completo (con joystick, disparos, mini mapa, IA)*

1. LIBRERÍAS Y MÓDULOS
Python
import pygame, sys, heapq, random, os
CopiarEditar
       pygame	:          Motor gráfico y de sonido 2D para videojuegos.
Sys:    	                   Permite salir del juego (sys.exit()).
Heapq:	             Usado para la cola de prioridad en el algoritmo A*.
Random:	          Genera posiciones aleatorias para enemigos y obstáculos.
Os:	                      Maneja rutas para cargar imágenes y sonidos de forma compatible en                            todos los sistemas operativos.

 2. INICIALIZACIÓN
python
Copiar código
pygame.init()
pygame.mixer.init()
•	Se inicializa todo lo necesario para gráficos y sonido.

3.CONTROLADOR (JOYSTICK):
python
CopiarEditar
pygame.joystick.init()
•	Detecta y configura un control PS4/Xbox si está conectado.


4. Pantalla y escenario 
python
Copiar código
WIDTH, HEIGHT = 1300, 700
WORLD_WIDTH, WORLD_HEIGHT = 2000, 2000
WIDTH, HEIGHT:  tamaño de la ventana visible.WORLD_WIDTH, WORLD_HEIGHT: tamaño total del Mundo (scroll).
5.RECURSOS:
python
Copiar código
fondo = pygame.image.load(...)
player_sheet = ...
enemy_img = ...
•	fondo: imagen de fondo escalada al mundo.
•	player_sheet: sprites del jugador.
•	enemy_img: sprites del enemigo.
•	También se cargan sonidos: música de fondo (mp3) y sonido de disparo (.wav).
6. GENERACIÓN DE MAPA:
python
Copiar código
grid = [[0 for _ in range(...)]]
for _ in range(300): grid[random...][random...] = 1
•	El mundo se divide en una cuadrícula (grid).
•	0 = libre, 1 = obstáculo.
•	Se colocan 300 obstáculos aleatorios como paredes. 


7. DETECCIÓN DE COLISIONES
python
•	Copiar código
•	def collides_with_walls(rect):
•	Detecta si un rect (jugador, enemigo, bala) toca una celda con valor 1 (pared).

8.CLASES PRINCIPALES:
 8. CLASE Player
•	Representa al jugador principal.
•	Se controla con:
o	Teclado: W, A, S, D.
o	Joystick: palanca izquierda.
•	Usa sprite_data para elegir la animación según la dirección del movimiento.
•	Detecta colisiones y mantiene al jugador dentro del mundo.

9.CLASE  Enemy
•	Representa a los enemigos con IA.
•	Usa el algoritmo A* para seguir al jugador si está cerca.
•	Anima su dirección.
•	Si alcanza al jugador, se activa game_over().

10.FUNCIONES CLAVE:
10. ALGORITMO A* (PATHFINDING) camino generado por A*
•	python
•	Copiar código
•	def astar(start, goal):
•	Encuentra el camino más corto desde un enemigo hasta el jugador.
•	Usa una heurística de distancia Manhattan:
abs(x1 - x2) + abs(y1 - y2)
•	Ignora celdas con obstáculos (1).
•	Devuelve una lista de coordenadas (tiles) que representan el camino. 11. 

11.DISPARO:
           python
•	CopiarEditar
•	def shoot():
•	Dispara en la dirección actual del jugador.
•	Crea una bala con velocidad y dirección y la añade a la lista bullets.
•	Reproduce el sonido de disparo.
12. MINIMAPA:
python
CopiarEditar
def draw_minimap():
•	Muestra una vista pequeña del mundo en la esquina superior derecha.
•	Jugador: punto verde.
•	Enemigos: puntos rojos.
•	Paredes: grises.

13. MENÚS:
•	start_menu(): Espera a que el jugador presione ENTER o START para comenzar.
•	level_complete(): Se muestra cuando matas a todos los enemigos.
•	game_over(): Se muestra si un enemigo alcanza al jugador.



14.INTELIGENCIA ARTIFICIAL:
🔺 A. ALGORITMO A* (A-STAR)
¿Qué es?
Es un algoritmo de búsqueda inteligente que encuentra el camino más corto entre dos puntos evitando obstáculos.

Cómo funciona:
1.	Cada enemigo calcula su camino hacia el jugador si está cerca (< 500 px).
2.	Divide el mundo en tiles.
3.	Evalúa los tiles con menor "costo" usando:
o	g_score: distancia recorrida hasta ahora.
o	heuristic: estimación de lo que falta.
Componentes:
Nombre	Función
open_set	Cola de prioridad con los tiles por evaluar
came_from	Guarda el camino recorrido (para reconstrucción)
g_score	Coste acumulado desde el inicio
heuristic()	Estimación al destino usando distancia Manhattan

B. ÁRBOL DE COMPORTAMIENTO (BEHAVIOR TREE):
¿Qué es?
Una estructura jerárquica que modela las decisiones de un personaje IA (enemigo).
Aunque no está formalmente codificado como BehaviorTree, el comportamiento del enemigo simula un árbol simple.
Lógica actual del enemigo:
python
CopiarEditar
if distance < 500   path = astar(...)
Representación en Árbol:
css
CopiarEditar
Selector
├── ¿Jugador está cerca?
│   └── Sí → Calcular A* y moverse
└── No hacer nada
Posibles mejoras:
Puedes convertirlo en un árbol formal con más comportamientos:
•	Patrullar si no ve al jugador.
•	Huir si tiene poca vida.
•	Buscar cobertura.
BUCLE PRINCIPAL main()
Flujo del juego:
1.	Reinicia jugador, enemigos y balas.
2.	Muestra el menú de inicio (start_menu()).
3.	Mientras se juega:
o	Lee teclado, mouse y joystick.
o	Actualiza la posición del jugador.
o	Enemigos persiguen al jugador si está cerca.
o	Se dibujan:
	Fondo.
	Obstáculos.
	Disparos.
	Sprites.
	Minimapa.
4.	Si matas a todos los enemigos: level_complete().
5.	Si un enemigo te alcanza: game_over().





Conclusión
Este proyecto es un juego tipo "Alien Breed" desarrollado con Pygame, que incluye scroll del mapa, disparos, enemigos con IA, soporte para joystick, y un minimapa. Los enemigos usan el algoritmo A* (Pathfinding) para seguir al jugador evitando obstáculos, y su comportamiento puede extenderse fácilmente con técnicas como árboles de comportamiento. Todo el mundo está construido con una cuadrícula que permite detectar colisiones, moverse inteligentemente y mostrar información visual en tiempo real. Es una base sólida para desarrollar un juego completo con inteligencia artificial funcional y fluida

Estudiante:                      (Yordys Rodriguez Valerio)
Matricula:                               (15-EISN-2-045)
FECHA DE ENTREGA:              (07-07-2025)

