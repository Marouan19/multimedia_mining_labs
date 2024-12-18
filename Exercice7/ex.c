#include <GLUT/glut.h>
#include <stdio.h>
#include <stdlib.h>

// Nombre de points de contrôle
#define CTRL_POINTS 3

// Points de contrôle (modifiables avec le clavier)
float controlPoints[CTRL_POINTS][CTRL_POINTS][3] = {
    {{-1.0, -1.0, 0.0}, {-0.5, -1.0, 0.5}, {0.0, -1.0, 0.0}},
    {{-1.0, -0.5, 0.5}, {-0.5, -0.5, 1.0}, {0.0, -0.5, 0.5}},
    {{-1.0, 0.0, 0.0}, {-0.5, 0.0, 0.5}, {0.0, 0.0, 0.0}}
};

int currentPoint[2] = {0, 0}; // Indice du point de contrôle courant
int signe = 1;                // Signe pour la modification (+/-)
float pas = 0.1;              // Pas de déplacement

// Fonction pour calculer une base de Bernstein
float bernstein(int i, int n, float t) {
    if (n == 2) {
        if (i == 0) return (1 - t) * (1 - t);
        if (i == 1) return 2 * (1 - t) * t;
        if (i == 2) return t * t;
    }
    return 0;
}

// Dessiner la surface de Bézier
void drawBezierSurface() {
    glColor3f(0.3, 0.7, 0.9); // Couleur de la surface
    for (float u = 0.0; u <= 1.0; u += 0.05) {
        glBegin(GL_QUAD_STRIP);
        for (float v = 0.0; v <= 1.0; v += 0.05) {
            float point1[3] = {0.0, 0.0, 0.0};
            float point2[3] = {0.0, 0.0, 0.0};

            for (int i = 0; i < CTRL_POINTS; i++) {
                for (int j = 0; j < CTRL_POINTS; j++) {
                    float b1 = bernstein(i, CTRL_POINTS - 1, u);
                    float b2 = bernstein(j, CTRL_POINTS - 1, v);
                    for (int k = 0; k < 3; k++) {
                        point1[k] += b1 * b2 * controlPoints[i][j][k];
                        point2[k] += b1 * bernstein(j, CTRL_POINTS - 1, v + 0.05) * controlPoints[i][j][k];
                    }
                }
            }

            glVertex3fv(point1);
            glVertex3fv(point2);
        }
        glEnd();
    }
}

// Dessiner les points de contrôle
void drawControlPoints() {
    glColor3f(1.0, 0.0, 0.0); // Rouge
    glPointSize(8.0);
    glBegin(GL_POINTS);
    for (int i = 0; i < CTRL_POINTS; i++) {
        for (int j = 0; j < CTRL_POINTS; j++) {
            glVertex3fv(controlPoints[i][j]);
        }
    }
    glEnd();
}

// Affichage principal
void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();

    // Update camera position
    gluLookAt(3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0); // Camera looking at the center

    // Apply slight translation to center the view
    glTranslatef(0.0f, 0.0f, -3.0f);

    drawBezierSurface();
    drawControlPoints();

    glutSwapBuffers();
    glFlush(); // Make sure the display is updated
}

// Gestion des touches clavier
void keyboard(unsigned char key, int x, int y) {
    switch (key) {
        case 'x':
            printf("Pressed 'x'\n");
            controlPoints[currentPoint[0]][currentPoint[1]][0] += signe * pas;
            break;
        case 'y':
            printf("Pressed 'y'\n");
            controlPoints[currentPoint[0]][currentPoint[1]][1] += signe * pas;
            break;
        case 'z':
            printf("Pressed 'z'\n");
            controlPoints[currentPoint[0]][currentPoint[1]][2] += signe * pas;
            break;
        case 's':
            printf("Pressed 's'\n");
            signe = -signe;
            break;
        case '\t':
            printf("Pressed 'Tab'\n");
            currentPoint[1]++;
            if (currentPoint[1] >= CTRL_POINTS) {
                currentPoint[1] = 0;
                currentPoint[0]++;
                if (currentPoint[0] >= CTRL_POINTS) {
                    currentPoint[0] = 0;
                }
            }
            break;
    }

    // Debug: Print control point after modification
    printf("Control Point [%d][%d]: (%f, %f, %f)\n", currentPoint[0], currentPoint[1],
          controlPoints[currentPoint[0]][currentPoint[1]][0],
          controlPoints[currentPoint[0]][currentPoint[1]][1],
          controlPoints[currentPoint[0]][currentPoint[1]][2]);

    glutPostRedisplay();
}

// Initialisation
void init() {
    glEnable(GL_DEPTH_TEST);
    glClearColor(0.8, 0.8, 0.8, 1.0); // Fond gris clair
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, 1.33, 1.0, 10.0); // Adjust perspective for better view
    glMatrixMode(GL_MODELVIEW);
}

// Main
int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(800, 600);
    glutCreateWindow("Surface de Bézier");

    init();

    glutDisplayFunc(display);
    glutKeyboardFunc(keyboard);

    glutMainLoop();
    return 0;
}