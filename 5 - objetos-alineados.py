
#ALIENACIÓN DE CHAKRAS:

	#Importamos módulos:
import numpy, glob, os, sys
from pyraf import iraf

	#Tomamos imágenes M67 como ejemplo para alinear:
iraf.display('O151127_0157.fits',1, zrange='yes', zscale='yes', contrast=0.05)
iraf.display('O151127_0160.fits',2, zrange='yes', zscale='yes', contrast=0.05)
iraf.display('O151127_0163.fits',3, zrange='yes', zscale='yes', contrast=0.05)
iraf.display('O151127_0168.fits',4, zrange='yes', zscale='yes', contrast=0.05)

	#Lista de imágenes de M67:
lista_M67= iraf.hselect('ffO*.fits','$I',"OBJECT?='M67*' ",Stdout=1)
	#Comprobación:
for im in lista_M67:
  iraf.imheader(im)

	#Creamos imagen de referencia:
iraf.imdelete('M67-referencia-xy.fits',verify="no") # borra antes si existe
iraf.imcopy('ffO151127_0160.fits','M67-referencia-xy.fits')
iraf.display('M67-referencia-xy.fits',1) # la vemos en la DS9

	#Medimos com imexam (pulsando ',') las estrellas de referencia, coordenadas en la terminal:
iraf.imexam()

	#Creamos un fichero M67-coords-xy.dat con las coordenadas copiadas:
j=0 
for im in lista_M67:
  j += 1
  iraf.imheader(im)
  iraf.display(im,1)
  sal= 'M67-coords-xy-'+str(j)+'.dat'
  print('j, sal=',str(j),sal)
  iraf.delete(sal, verify="no")
  iraf.imexam(im, 1, imagecur='M67-coords-xy.dat',defkey='a', use_display="no", wcs="logical", display="",Stdout=sal)

	#DS9 de la imagen de referencia:
iraf.display('M67-referencia-xy.fits',1)
iraf.tvmark(1, 'M67-coords-xy.dat', mark="circle", radii="19,20,21,22", color=209)
iraf.tvmark(1, 'M67-coords-xy.dat', mark="none", txsize="8",color=205,number='yes',\
nxoffset=25, nyoffset=0)

	#IMagen para cada filtro y ubicando las estrellas:
iraf.display('ffO151127_0158.fits',1)
iraf.tvmark(1, 'M67-coords-xy.dat', mark="circle", radii="19,20,21,22", color=209)
iraf.tvmark(1, 'M67-coords-xy.dat', mark="none", txsize="8", color=205,number='yes',\
nxoffset=25, nyoffset=0)

iraf.display('ffO151127_0162.fits',2)
iraf.tvmark(2, 'M67-coords-xy.dat', mark="circle", radii="19,20,21,22", color=209)
iraf.tvmark(2, 'M67-coords-xy.dat', mark="none", txsize="8", color=205,number='yes',\
nxoffset=25, nyoffset=0)

iraf.display('ffO151127_0166.fits',3)
iraf.tvmark(3, 'M67-coords-xy.dat', mark="circle", radii="19,20,21,22",color=209)
iraf.tvmark(3, 'M67-coords-xy.dat', mark="none", txsize="8", color=205,number='yes',\
nxoffset=25, nyoffset=0)

	#Lista para guardar imágenes alineadas:
lista_M67_al = ["al"+ s[2:] for s in lista_M67

	#Alineado:
iraf.imalign(",".join(lista_M67),"M67-referencia-xy.fits","M67-coords-xy.dat",\
output=",".join(lista_M67_al),shiftimages="yes",boundary_type="nearest",\
trimimages="no",interp_type="poly3")


