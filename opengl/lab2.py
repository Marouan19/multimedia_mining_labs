from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Global variables for window dimensions
W, H = 800, 600

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowPosition(50, 50)
    glutInitWindowSize(W, H)
    glutCreateWindow('Labs Note 8')

    # Background color
    glClearColor(0., 0., 0., 1)
    
    glutDisplayFunc(aff)
    glutKeyboardFunc(keyboard)
    glutReshapeFunc(redim)
    
    glutMainLoop()

def redim(w, h):
    global W, H
    W, H = w, h

def keyboard(key, x, y):
    intKey = int.from_bytes(key, 'little')
    if intKey == 27:  # Escape key
        exit(1)

def axes():
    glLineStipple(1, 0x0CFF)
    glEnable(GL_LINE_STIPPLE)
    glLineWidth(1)
    
    # Draw axes
    glBegin(GL_LINES)
    
    # X-axis (Red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-10.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)
    
    # Y-axis (Green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -10.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)
    
    # Z-axis (Blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -10.0)
    glVertex3f(0.0, 0.0, 10.0)
    
    glEnd()
    glDisable(GL_LINE_STIPPLE)

def dessiner():
    axes()
    
    # Draw red teapot
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glTranslatef(-1, 0., 0.)
    glutSolidTeapot(0.3)
    glPopMatrix()
    
    # Draw green teapot
    glColor3f(0.0, 1.0, 0.0)
    glTranslatef(1, 0., 0.)
    glutSolidTeapot(0.3)

def aff():
    global W, H
    
    # Clear buffer
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Viewport 1 (Top-left)
    glViewport(0, int(H / 2), int(W / 3), int(H / 2))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2.0, 2.0, -2.0, 2.0, -10.0, 10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(1., 0., 0., 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    dessiner()

    # Viewport 2 (Top-center)
    glViewport(int(W / 3), int(H / 2), int(W / 3), int(H / 2))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2.0, 2.0, -2.0, 2.0, -10.0, 10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0., 1., 0., 0.0, 0.0, 0.0, 1.0, 0.0, 1.0)
    dessiner()

    # Viewport 3 (Top-right)
    glViewport(int(2 * W / 3), int(H / 2), int(W / 3), int(H / 2))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2.0, 2.0, -2.0, 2.0, -10.0, 10.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0., 0., 1., 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    dessiner()

    # Swap buffers
    glutSwapBuffers()

if __name__ == '__main__':
    main()
