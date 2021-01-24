from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

from pywavefront import visualization
from pywavefront import Wavefront


file_abspath = 'Godzilla 2019 Color V2 mm.obj'

rotation = 0.0
meshes = Wavefront(file_abspath, cache= True)


def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, float(500) / 500, 1.0, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    return True

def draw():
    global rotation
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0.0, 0.0, 0.0)
    glLoadIdentity()

    glEnable(GL_LIGHTING)

    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_MODELVIEW)

    glTranslated(0, .8, -20)
    glRotatef(-66.5, 0, 0, 1)
    glRotatef(rotation, 1, 0, 0)
    glRotatef(90, 0, 0, 1)
    glRotatef(0, 0, 1, 0)
    glScale(0.05, 0.05, 0.05)
    
    visualization.draw(meshes)

    rotation += 45 * 0.01

    if rotation > 720.0:
        rotation = 0.0
    glFlush()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(750, 750)
    glutInitWindowPosition(10, 10)
    glutIdleFunc(draw)
    glutCreateWindow(b"Solar System")
    init()
    glutDisplayFunc(draw)
    glutMainLoop()

main()