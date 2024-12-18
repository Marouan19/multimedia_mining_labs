import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import OpenGL.GLU as glu
import math

# Points de contrôle initiaux pour une surface de Bézier quadratique
control_points = np.array([
    [[0.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, 2.0, 0.0]],
    [[1.0, 0.0, 1.0], [1.0, 1.0, 2.0], [1.0, 2.0, 1.0]],
    [[2.0, 0.0, 0.0], [2.0, 1.0, 1.0], [2.0, 2.0, 0.0]]
])

# Variables globales
current_point_row = 0
current_point_col = 0
sign = 1
pas_x, pas_y, pas_z = 0.1, 0.1, 0.1
rotation_x, rotation_y = 0, 0
view_mode = 0

def factorial(n):
    """Calcul du factoriel"""
    return math.factorial(n)

def binomial_coefficient(n, k):
    """Calcul du coefficient binomial"""
    return factorial(n) // (factorial(k) * factorial(n - k))

def bernstein_polynomial(n, i, u):
    """Polynôme de Bernstein pour la surface de Bézier"""
    return binomial_coefficient(n, i) * (u**i) * ((1-u)**(n-i))

def bezier_surface(u, v):
    """Calcul d'un point sur la surface de Bézier"""
    point = np.zeros(3)
    for i in range(3):
        for j in range(3):
            b_u = bernstein_polynomial(2, i, u)
            b_v = bernstein_polynomial(2, j, v)
            point += control_points[i, j] * b_u * b_v
    return point

def display():
    """Fonction de rendu OpenGL"""
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glLoadIdentity()
    
    # Positionnement de la caméra et rotation
    gl.glTranslatef(0, 0, -5)
    gl.glRotatef(rotation_x, 1, 0, 0)
    gl.glRotatef(rotation_y, 0, 1, 0)

    # Dessin des points de contrôle
    gl.glPointSize(10)
    gl.glBegin(gl.GL_POINTS)
    for i in range(3):
        for j in range(3):
            # Point sélectionné en vert, autres points en rouge
            if i == current_point_row and j == current_point_col:
                gl.glColor3f(0, 1, 0)  # Vert pour le point sélectionné
            else:
                gl.glColor3f(1, 0, 0)  # Rouge pour les autres points
            gl.glVertex3fv(control_points[i, j])
    gl.glEnd()

    # Dessin de la surface de Bézier
    gl.glColor3f(0, 0, 1)
    if view_mode == 0:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
    elif view_mode == 1:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    else:
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_POINT)

    for u in np.linspace(0, 1, 30):
        gl.glBegin(gl.GL_TRIANGLE_STRIP)
        for v in np.linspace(0, 1, 30):
            point = bezier_surface(u, v)
            gl.glVertex3fv(point)
            point = bezier_surface(u + 0.1, v)
            gl.glVertex3fv(point)
        gl.glEnd()

    glut.glutSwapBuffers()

def reshape(width, height):
    """Gestion du redimensionnement de la fenêtre"""
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(45, width/height, 0.1, 100.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)

def keyboard(key, x, y):
    """Gestion des événements clavier"""
    global current_point_row, current_point_col, sign
    global control_points, rotation_x, rotation_y, view_mode

    key = key.decode('utf-8')

    # Navigation entre les points de contrôle
    if key == '\t':
        current_point_col = (current_point_col + 1) % 3
        if current_point_col == 0:
            current_point_row = (current_point_row + 1) % 3

    # Changement de signe
    if key == 's':
        sign *= -1

    # Modification des coordonnées
    if key == 'x':
        control_points[current_point_row, current_point_col, 0] += sign * pas_x
    elif key == 'y':
        control_points[current_point_row, current_point_col, 1] += sign * pas_y
    elif key == 'z':
        control_points[current_point_row, current_point_col, 2] += sign * pas_z

    # Rotation de la vue
    if key == 'a':
        rotation_y -= 5
    elif key == 'd':
        rotation_y += 5
    elif key == 'w':
        rotation_x -= 5
    elif key == 'q':
        rotation_x += 5

    # Mode de visualisation
    if key == 'v':
        view_mode = (view_mode + 1) % 3

    glut.glutPostRedisplay()

def main():
    """Initialisation et lancement de l'application"""
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
    glut.glutInitWindowSize(800, 600)
    glut.glutCreateWindow(b"Surface de Bezier 3D")

    gl.glEnable(gl.GL_DEPTH_TEST)

    glut.glutDisplayFunc(display)
    glut.glutReshapeFunc(reshape)
    glut.glutKeyboardFunc(keyboard)

    glut.glutMainLoop()

if __name__ == '__main__':
    main()