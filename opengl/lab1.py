import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class OpenGLScene:
    def __init__(self, width=800, height=600):
        """Initialize the OpenGL scene and window"""
        self.width = width
        self.height = height
        self.init_glut()
        self.init_gl()

    def init_glut(self):
        """Initialize GLUT settings"""
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
        glutInitWindowPosition(50, 50)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow(b'Labs Note 8')

        # Register callback functions
        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutReshapeFunc(self.reshape)

    def init_gl(self):
        """Initialize OpenGL settings"""
        glClearColor(0., 0., 0., 1.)
        glEnable(GL_DEPTH_TEST)

    def reshape(self, w, h):
        """Handle window reshape events"""
        # Prevent division by zero
        h = max(h, 1)
        
        # Set viewport to cover entire window
        glViewport(0, 0, w, h)
        
        # Reset projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Set perspective projection
        gluPerspective(90., w/h, 0.1, 15)
        
        # Switch back to modelview matrix
        glMatrixMode(GL_MODELVIEW)

    def draw_axes(self):
        """Draw coordinate axes"""
        glLineStipple(1, 0x0CFF)
        glEnable(GL_LINE_STIPPLE)
        glLineWidth(1)

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

    def display(self):
        """Main display function"""
        # Clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Reset modelview matrix
        glLoadIdentity()
        
        # Set camera position
        gluLookAt(5, 5, 5, 0., 0., 0., 0., 1., 0.)
        
        # Draw coordinate axes
        self.draw_axes()
        
        # Draw first sphere (red)
        glPushMatrix()
        glColor3f(1., 0., 0.)
        glutSolidSphere(1., 12, 12)
        
        # Draw second sphere (green) - transformed
        glRotatef(30, 0., 1., 0.)
        glTranslated(5., 0., 0.)
        glColor3f(0., 1., 0.)
        glutSolidSphere(0.4, 12, 12)
        
        # Draw third sphere (white) - further transformed
        glRotatef(90, 0., 1., 0.)
        glTranslated(1.2, 0., 0.)
        glColor3f(1., 1., 1.)
        glutSolidSphere(0.1, 12, 12)
        
        glPopMatrix()
        
        # Swap buffers to display the rendered scene
        glutSwapBuffers()

    def keyboard(self, key, x, y):
        """Handle keyboard input"""
        # Convert key to integer
        int_key = ord(key)
        
        # Exit on Escape key
        if int_key == 27:  # Escape key
            sys.exit()

    def run(self):
        """Start the GLUT main loop"""
        glutMainLoop()

def main():
    """Create and run the OpenGL scene"""
    scene = OpenGLScene()
    scene.run()

if __name__ == '__main__':
    main()