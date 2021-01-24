'''
ESKİ VERSİYON (YAVAŞ ÇALIŞAN)
Grup No:7
E. Aleyna Elmas 18120205033
Çağla Betül Sezer 18120205031
Emirhan Yılmaz 18120205037
Zeynep Ülkü Kılıoç 18120205011
Final Proje Ödevi : .obj file görselleştirme
'''
import os
import sys

from OpenGL.GLUT import *
from OpenGL.GL import *
from PIL import Image
from pywavefront import Wavefront
from OpenGL.GLU import *
import math as m

id = []
meshes = []

#objenin konumu için koordinatlar
x = [0]
y = [0]
z = [2]
#path'lerin tutulduğu dizi

paths = []

#kamera ayarları için değişkenler
zoom = 0  # mouse ile küp ölçeklendirmesi yapmak için
angle = 0.0
deltax = 0.0
deltaz = -1.0
eye_x = 0.0
eye_z = 5.0
angleX = 0.0
angleY = 0.0
#mouse ile kamera ayarları için değişkenler
deltaAngleX = 0.0
deltaAngleY = 0.0
checkX = -1
checkY = -1

# paths dizisine dosya isimlerini ekliyoruz ve geri kalan işler diğer fonksiyonlarda hallediliyor
paths.append("Japanese_Maple.obj")

# meshes dizisine objeleri ekliyoruz
for i in range(0, len(paths)):
    meshes.append(Wavefront(paths[i], cache=True))


# mesh objesini alıp mtl dosyasındaki texture dosyasının ismini dönderir
def getFilename(mesh):
    filename = ""
    for name, material in mesh.materials.items():
        try:
            if material.texture != None:
                filename = material.texture.name
        except:
            pass

    return filename


# herhangi bir obje için texture yükler
def LoadTexture(file):
    image = Image.open(file)
    if image is None:
        print("Dosya Acilamadi!")
        sys.exit(0)
    ix = image.size[0]
    iy = image.size[1]

    #texture dosya tipine göre RGB çeşitlendirmesi
    if file.split(".")[1] == "png":
        image = image.tobytes("raw", "RGBA")
    elif file.split(".")[1] == "jpg":
        image = image.tobytes("raw", "RGBX")
    else:
        image = image.tobytes("raw", "RGB")

    id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    return id


def init():
    global id, meshes
    glActiveTexture(GL_TEXTURE0)
    # sırasıyla id dizisine objelerin texture ını yükleyip id lerini atar
    for i in range(0, len(meshes)):
        for name, material in meshes[i].materials.items():
            try:
                id.append(LoadTexture(material.texture.name))
            except:
                pass
    glEnable(GL_TEXTURE_2D)
    glClearColor(1, 1.0, 1.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)

    glEnable(GL_DEPTH_TEST)


def renderScene():
    #arka plan ayarlanması
    global x
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, 4.0 / 3.0, 1, 40)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eye_x + angleX, 1.0 + angleY, eye_z, (eye_x + deltax), 1.0, (eye_z + deltaz), 0.0, 1.0, 0.0)

    #zemin çizimi
    '''
    glColor3f(0.9, 0.9, 0.9)
    id2 = LoadTexture("zemin.jpg")
    glBindTexture(GL_TEXTURE_2D, id2)
    glBegin(GL_QUADS)
    glTexCoord2f(1, 0)
    glVertex3f(-10.0, 0, 10.0)
    glTexCoord2f(1, 1)
    glVertex3f(-10.0, 0.0, -10.0)
    glTexCoord2f(0, 1)
    glVertex3f(10.0, 0.0, -10.0)
    glTexCoord2f(0, 0)
    glVertex3f(10.0, 0.0, 10.0)
    glEnd()
'''
    # yüklenen her obje için döngü
    a = 0
    for k in range(0, len(meshes)):


        # çizim kısmı
        for name, material in meshes[k].materials.items():
            glPushMatrix()

            glTranslatef(x[k], y[k], 0)
            glScale(0.1, 0.1, 0.1)
            glColor3f(1.0, 1.0, 1.0)
            glBindTexture(GL_TEXTURE_2D, id[a])

            glBegin(GL_TRIANGLES)
            j = 0
            if material.vertex_format == "T2F_N3F_V3F":  # eğer obj dosyası vn içeriyorsa bu kısım çalışır
                print(len(material.vertices))
                # material.vertices[0] [1] vt, [2] [3] [4] vn, [5] [6] [7] v diye devam eder
                for i in range(0, int(len(material.vertices) / 8)):
                    glTexCoord2f(material.vertices[j], material.vertices[j + 1])
                    glNormal3f(material.vertices[j + 2], material.vertices[j + 3], material.vertices[j + 4])
                    glVertex3f(material.vertices[j + 5], material.vertices[j + 6], material.vertices[j + 7])
                    j += 8
            elif material.vertex_format == "T2F_V3F":  # eğer obj dosyası vn içermiyorsa bu kısım çalışır
                # material.vertices[0] [1] vt, [2] [3] [4] v, diye devam eder
                for i in range(0, int(len(material.vertices) / 5)):
                    glTexCoord2f(material.vertices[j], material.vertices[j + 1])
                    glVertex3f(material.vertices[j + 2], material.vertices[j + 3], material.vertices[j + 4])
                    j += 5
            a += 1
            glEnd()
            glPopMatrix()
    glFlush()
    glutSwapBuffers()


def keyPressed(*args):
    fraction = 0.1
    global angle, eye_x, deltax, eye_z, deltaz
    if args[0] == b"a":
        angle -= 0.05
        deltax = m.sin(angle)
        deltaz = -m.cos(angle)
    elif args[0] == b"d":
        angle += 0.05
        deltax = m.sin(angle)
        deltaz = -m.cos(angle)
    glutPostRedisplay()


def mouse(mouse, state, x, y):
    global checkX, checkY, deltaAngleX, deltaAngleX, deltax, deltaz
    if mouse == GLUT_LEFT_BUTTON:
        if state == GLUT_UP:  # farenin sol tıkı basılıysa
            deltax += m.sin(deltaAngleX)
            deltaz += -m.cos(deltaAngleY)
            checkX = -1
            checkY = -1
        elif state == GLUT_DOWN:  # farenin sol tıkı basılı durumda değilse
            checkX = x
            checkY = y
    glutPostRedisplay()


def moveMouse(x, y):
    global checkX, checkY, deltaAngleX, deltaAngleY, angleX, angleY
    # eğer fare x ekseninde hareket ediyorsa angleX değerleri güncellenir.
    if checkX >= 0:
        deltaAngleX = (x - checkX)

        angleX = (angleX + deltaAngleX) * 0.005
    # eğer fare y ekseninde hareket ediyorsa angleY değerleri güncellenir.
    if checkY >= 0:
        deltaAngleY = (y - checkY)
        angleY = (angleY + deltaAngleY) * 0.005


def MouseWheel(*args):
    # mouse tekerleği döndürüldüğünde ölçeklendirme ayarını yapar
    fraction = 0.1
    global eye_x, deltax, eye_z, deltaz
    if args[1] == -1:
        eye_x -= deltax * fraction
        eye_z -= deltaz * fraction
    elif args[1] == 1:
        eye_x += deltax * fraction
        eye_z += deltaz * fraction
    else:
        pass
    glutPostRedisplay()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(10, 10)
    glutIdleFunc(renderScene)
    glutCreateWindow(b"Wild Jungle")
    init()
    glutDisplayFunc(renderScene)
    # glutIdleFunc(renderScene)
    glutMouseWheelFunc(MouseWheel)
    glutMouseFunc(mouse)
    glutMotionFunc(moveMouse)
    glutKeyboardFunc(keyPressed)
    glutMainLoop()
    glEnable(GL_DEPTH_TEST)


main()
