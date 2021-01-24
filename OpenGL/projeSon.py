'''
Grup No:7
E.Aleyna Elmas 18120205033
Çağla Betül Sezer 181205031
Emirhan Yılmaz 18120205037
Zeynep Ülkü Kılıç 18120205011
Final Proje Ödevi : .obj file görselleştirme
'''

#kütüphanelerin eklenmesi
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

#obj file okumak için kullanılan kütüphaneler
from pywavefront import visualization
from pywavefront import Wavefront
import math as m

#kamerayı hareket ettirmek için değişkenler
angle = 0.0
deltax = 0.0
deltaz = -1.0
delta = 0
eye_x = 0.0
eye_z = 12.0
angleX = 0.0
angleY = 0.0
deltaAngleX = 0.0
deltaAngleY = 0.0
checkX = -1
checkY = -1


meshes = []#objeleri tutan dizi
paths = []#dosya path'lerini duzan dizi

#objelerin sahne üzerindeki konumların için koordinat değerleri
x =[0.5, -2, 2, 0, -4, 4, 2, 2]
y = [0, 0.6, 0, 0, 0, 0, 0, 0]
z = [1, -0.25, 2, 0, -6, -6, -6, 3]
#objelerin büyüklükleri için değerler
scale = [0.01, 0.3, 2, 0.5, 0.3, 0.3, 0.1, 0.01]
#objelerin duruş açısı için değerler
rotate_x = [0, 0, 0, 0, 0, 0, 0, 0, 0]
rotate_y = [35, -25, 0, 0, 0, 0, 180, 0]

#her bir obj dosyasının path[] dizine yüklenmesi
paths.append('Rabbit.obj')
paths.append('Horse.obj')
paths.append('F_3.obj')
paths.append('Japanese_Maple.obj')
paths.append('treePBR.obj')
paths.append('treePBR.obj')
paths.append('farmhouse_obj.obj')
paths.append('Campfire.obj')

#object file dosyaları okunur ve meshes[] dizisine atılır
for i in range(0, len(paths)):
    meshes.append(Wavefront(paths[i], cache= True))

def LoadTexture(file):
    #dosyanın açılması ve texture'ın yüklenmesi
    image = Image.open(file)
    if image is None:
        print("Dosya Acilamadi!")
        sys.exit(0)
    ix = image.size[0]
    iy = image.size[1]

    #texture dosyasının formatına göre RGB türü verilir
    if file.split(".")[1] == "png":
        image = image.tobytes("raw", "RGBA")
    elif file.split(".")[1] == "jpg":
        image = image.tobytes("raw", "RGBX")
    else:
        image = image.tobytes("raw", "RGB")

    #texture oluşturulur
    id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    return id

def init():
    #sahne özellikleri
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, float(500) / 500, 1.0, 100.0)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    return True


def draw():
    #sahne background ayarlamaları
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.6, 1.0, 1.0, 0)
    glLoadIdentity()
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_MODELVIEW)

    #kameranın ayarlanması ve değişiklikleri için atanan değişkenler
    gluLookAt(eye_x + angleX, 1.0 + angleY, eye_z , (eye_x + deltax), 1.0, (eye_z + deltaz), 0.0, 1.0, 0.0)

    #zemin oluşturulması ve texture'lanması
    id2 = LoadTexture("zemin3.jpg")
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

    #her bir obje için çizimin gerçekleştirilmesi
    for i in range(0, len(meshes)):
        glPushMatrix()
        glTranslated(x[i], y[i], z[i])#konumu için
        #açısı için
        glRotatef(rotate_x[i], 1, 0, 0)
        glRotatef(rotate_y[i], 0, 1, 0)
        glScale(scale[i], scale[i], scale[i])#boyutu için

        #objenin çizimi
        visualization.draw(meshes[i])
        glPopMatrix()

    glFlush()
    glutSwapBuffers()

#hareket ve dönüş için klavye fonksiyonu
def keyPressed(*args):
    fraction = 0.1
    #camera'da kullanılacak olan değerler
    global angle, eye_x, deltax, eye_z, deltaz
    if args[0] == b"a":#sola dönüş
        angle -= 0.01
        deltax = m.sin(angle)
        deltaz = -m.cos(angle)
    elif args[0] == b"d":#sağa ddönüş
        angle += 0.01
        deltax = m.sin(angle)
        deltaz = -m.cos(angle)
    elif args[0] == b"w":#ileri gider
        eye_x += deltax * fraction
        eye_z += deltaz * fraction
    elif args[0] == b"s":#geri gider
        eye_x -= deltax * fraction
        eye_z -= deltaz * fraction
    glutPostRedisplay()

#mouse ile tut çek bırak özelliğinin kamera değişkenlerine verilmesi
def mouse(mouse, state, x, y):
    global checkX, checkY, deltaAngleX, deltaAngleX, deltax, deltaz
    if mouse == GLUT_LEFT_BUTTON:
        if state == GLUT_UP:  #farenin sol tıkı basılıysa
            deltax += m.sin(deltaAngleX)
            deltaz += -m.cos(deltaAngleY)
            checkX = -1
            checkY = -1
        elif state == GLUT_DOWN:  #farenin sol tıkı basılı durumda değilse
            checkX = x
            checkY = y
    glutPostRedisplay()

#mouse'un tut çek bırak özelliği için yardımcı diğer fonksiyon
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

#mouse tekerleği döndürüldüğünde ölçeklendirme ayarını yapar
def MouseWheel(*args):
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
    glutInitWindowSize(750, 750)
    glutInitWindowPosition(10, 10)
    glutIdleFunc(draw)
    glutCreateWindow(b"Final Project")
    init()
    glutDisplayFunc(draw)
    glutMouseWheelFunc(MouseWheel)
    glutMouseFunc(mouse)
    glutMotionFunc(moveMouse)
    glutKeyboardFunc(keyPressed)
    glutMainLoop()

main()