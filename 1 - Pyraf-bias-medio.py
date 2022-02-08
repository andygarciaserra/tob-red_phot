# BIAS MEDIO:

#Importamos módulos:
import numpy,glob
from pyraf import iraf

#Lista de BIAS:
listabias = sorted(glob.glob("B15*.fits"))
	#Comprobamos que son BIAS:
for im in listabias:
	iraf.imhead(im)

#DS9:
for im in range(4):
	iraf.display(listabias[im],im+1,zscale="yes",zrange="yes",ztran="linear",fill="no")





# BUSQUEDA DE OVERSCAN:	
	#Hacemos un 'prows' de la imagen que es una media de todas las filas
iraf.prows(listabias[0], 1, 2048)

	#Preparamos 'section' como la sección que se usa para hacer esta media dentro de la imagen:
section="[1:2097,2:2048]"
iraf.pcols(listabias[0]+section, 1, 2048)

	#Comprobamos pcols para ver si hay problemas en las filas (overscan):
iraf.pcols(listabias[0], 1, 50, wy1=398., wy2= 405.)		#1,50: filas en las que promedia
iraf.pcols(listabias[0], 51, 2097, wy1=398., wy2= 405.)		#wyz,wy2: límites gráfica

	#Section que recorta las filas de 100 a 2000 y las columnas de 10 a 2000:
section = "[100:2000,10:2000]"

	#Estadística de cada BIAS de la lista dentro de la sección elegida sin overscan:
for im in listabias:
	iraf.imstat(im+section, fields="image,mean,stddev,min,max",format="yes")
	
	#Formato a la lista para poder usarla en IRAF:
listabias2 = ",".join(listabias)

	#Nombre del BIAS medio:
biasmedio = "Biasmedio"

	#Creamos BIAS medio:
iraf.imdelete(biasmedio, verify="no")				#Borramos si ya existe:
iraf.imcombine(listabias2, biasmedio, combine="average", reject="minmax")

	#Comparamos las estadísitcas del BIAS medio y de los BIAS por separado:
iraf.imstat('B*.fits'+section, fields="image,npix,mean,stddev", format="yes")
iraf.imstat(biasmedio+section, fields="image,npix,mean,stddev", format="no")
