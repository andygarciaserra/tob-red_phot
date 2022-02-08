
#APLICANDO BIAS A LOS OBJETOS Y FLATS:

#Importamos módulos:
import numpy, glob
from pyraf import iraf

	#Lista de FLATS:
listaflats = sorted(glob.glob("F*.fits"))

	#Sección en la que recortar las imágenes:
section = "[60:2000,10:2000]"

	#Módulos de IRAF para correr "ccdproc":
iraf.imred()
iraf.ccdred()
iraf.ccdred.instrument= " "
iraf.ccdred.verbose = "yes"
listaflats_b = ["b"+ s for s in listaflats]

	#Borramos antes si existen:
iraf.imdel("bF*.fits", verify="no")

	#Desechamos las cuatro primeras y ultimas columnas del overscan.
iraf.ccdproc(",".join(listaflats),output=",".join(listaflats_b),overscan="yes",zerocor="no",flatcor="no",readaxis="line",darkcor="no",fixpix="no",\trim="yes",biassec="[5:46,1:2048]",trimsec="[51:2098,1:2048]",ccdtype=" ",function="legendre",order=1)

	#Lista de objetos:
listaobjetos = sorted(glob.glob("O*.fits"))

	#Borramos por si ya existen:
iraf.imdel("bO*.fits", verify="no")

	#Lista nueva para guardar los objetos reducidos de FLAT:
listaobjetos_b = ["b"+ s for s in listaobjetos]

	#Corrección de BIAS:
for im in listaobjetos:
	print(im)
	iraf.imdelete("b"+im,verify="no") # borra la salida si ya existe
iraf.ccdproc(im,output="b"+im,overscan="yes",trim="yes",zerocor="no",flatcor="no",readaxis="line",darkcor="no",fixpix="no",interactive="no",biassec="[5:46,1:2048]",trimsec="[51:2098,1:2048]",function="legendre",order=1)

