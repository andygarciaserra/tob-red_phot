#-*- coding: utf-8 -*-

''' 


 ~~~~~  Pyraf-6-objetos-fotometria.py 
  

  Programa para hacer fotometria sobre las imagenes de objetos, ya corregidas de bias y flat,
  y alineadas. 


''' 


# Importamos módulos:
import numpy as np
import os, glob 
import pylab as pl 
from pyraf import iraf





# Paquetes de IRAF:
iraf.noao.digiphot(_doprint=0) 
iraf.noao.digiphot.phot(_doprint=0) 
iraf.noao.digiphot.daophot(_doprint=0) 





#MEDICION FWHMPSF y SIGMA:

	#Mostramos imágenes en el filtro I de M67 y usaremos las que tengan un Texp intermedio:
iraf.hselect('ffO*',"$I,OBJECT,INSFILTE,EXPTIME","OBJECT?='M67*'") 


	#Pillamos un objeto de cada filtro y lo renombramos para ubicar las estrellas referencia:
iraf.delete("referencia_M67_V.fits",verify="no")                  # borra antes si existe 
iraf.imcopy("alO151127_0158.fits","referencia_M67_V.fits") 

iraf.delete("referencia_M67_R.fits",verify="no")                  # borra antes si existe 
iraf.imcopy("alO151127_0162.fits","referencia_M67_R.fits") 

iraf.delete("referencia_M67_I.fits",verify="no")                  # borra antes si existe 
iraf.imcopy("alO151127_0166.fits","referencia_M67_I.fits") 


	#Parámetros para 'daofind':
iraf.datapars.ccdread = "RDNOISE"  
iraf.datapars.gain = "GAIN" 
iraf.datapars.exposure = "EXPTIME" 
iraf.datapars.airmass = "AIRMASS" 
iraf.datapars.filter = "INSFILTE"


	# Y otros parámetros:
iraf.datapars.noise = "poisson"            # tipo de ruido
iraf.datapars.scale = 1.                  
iraf.findpars.nsigma = 1.5 
iraf.findpars.ratio = 1.0 
iraf.findpars.theta = 0. 

iraf.centerpars.calgorithm="centroid" 
iraf.fitskypars.salgorithm="centroid" 
iraf.photpars.weighting="constant" 

iraf.phot.interactive="no" 
iraf.phot.verify="no" 
iraf.phot.update="no" 

iraf.datapars.datamax= 50000.              # limite de cuentas de saturacion del CCD 
iraf.findpars.threshold = 5.0              # razon S/R minima para detectar estrellas 


	# Medimos los valores usando 'daofind' haciendo una media para varias estrellas:
filtro= ['V', 'R', 'I']                 # filtros de las imagenes
for j in range(3):                      # para los tres filtros V, R, I
  print('   ')
  print('Filtro: ',filtro[j])
  print('   ')
  iraf.display('referencia_M67_'+filtro[j],1)
  iraf.daoedit('referencia_M67_'+filtro[j])

fwhm= [3.8, 4.6, 4.9]           # fwhmpsf en V, R, I
sigma= [7.8, 9.8, 11.0]         # sigma de las cuentas de cielo en V, R, I


	# Creación de fichero .coo con las coordenadas de las estrellas:
iraf.delete("referencia_M67_*.coo.*",verify="no")              # borra si ya existe
for j in range(3):                      # para los tres filtros V, R, I
  print('   ')
  print('j, filtro, fwhmpsf, sigma=',j, filtro[j], fwhm[j], sigma[j])
  iraf.datapars.fwhmpsf = fwhm[j]       # fwhm de las estrellas  
  iraf.datapars.sigma = sigma[j]        # promedio de la sigma de las cuentas de cielo
  imag= 'referencia_M67_'+filtro[j]
  print('imag=', imag)
  iraf.daofind(imag, output="default", starmap="", skymap="", interactive="no", verify="no")


	# Mostramos en DS9 los tres filtros para comprobar:
colores= [207, 205, 209]
for j in range(3):                      # para los tres filtros V, R, I
  print('j, filtro=',j, filtro[j])
  imag= 'referencia_M67_'+filtro[j]
  print('imag=', imag)
  iraf.display(imag, j+1, zrange="yes", zscale="yes", contrast=0.15) 
  iraf.tvmark(j+1, imag+'.coo.1', mark="circle", radii="15,16,17,18", color=colores[j])  


	# Mostramos también el disco de la estrella dentro de cada anillo solo para el filtro V:
iraf.datapars.fwhmpsf = fwhm[0]                                 # fwhm en V 
iraf.photpars.aperture=  float(iraf.datapars.fwhmpsf)*2.5       # radio de  apertura
iraf.fitskypars.annulus= float(iraf.photpars.aperture) + 4.0    # radio interno anillo de cielo  
iraf.fitskypars.dannulus= 6.0                                   # ancho anillo de cielo 

raper= float(iraf.photpars.aperture)                            # radio de medida del flujo de la estrella
rciel1= float(iraf.fitskypars.annulus)                          # radio interior del anillo de cielo
rciel2= rciel1 + float(iraf.fitskypars.dannulus)                # radio exterior del anillo de cielo

print('raper, rciel1,rciel2=',raper,rciel1,rciel2)

iraf.display("referencia_M67_V", 1, zrange="yes", zscale="yes", contrast=0.15) 
r= 0.
while r <= raper:
   iraf.tvmark(1,"referencia_M67_V.coo.1",mark="circle",radii=r,color=207)
   r += 1.

r= rciel1
while r <= rciel2:
   iraf.tvmark(1,"referencia_M67_V.coo.1",mark="circle",radii=r,color=205)
   r += 1.





# FOTOMETRÍA PARA TODAS LAS IMÁGENES EN V, R, I:


listasfot=[' ',' ',' ']
for j in range(3):                       # para tres filtros V, R, I
  print(' ')
  print('j, filtro, fwhmpsf, sigma=',j, filtro[j], fwhm[j], sigma[j])
  iraf.datapars.fwhmpsf = fwhm[j]        # fwhm de las estrellas  
  iraf.datapars.sigma = sigma[j]         # promedio de la sigma de las cuentas de cielo
  iraf.photpars.aperture= float(iraf.datapars.fwhmpsf)*2.5   # diametro apertura fotometria, 2.5*fwhmpsf 
  iraf.fitskypars.annulus=float(iraf.photpars.aperture)+4.0  # diametro interno anillo de cielo  
  seleccion= "OBJECT?='M67*'&" + "INSFILTE='"+filtro[j]+"'"
#  seleccion1= "OBJECT?='M67*' & INSFILTE='"+filtro[j]+"' "  # tambien funciona
  print(seleccion)
#  print(seleccion1)
  lista= iraf.hselect("alO*.fits","$I", seleccion, Stdout=1) 
  listasfot[j]= lista          
  print('lista:', lista)
  for imag in lista:
    print(' ')
    print('Fotometria de: ')
    iraf.imheader(imag)
# Para el caso de utilizar como referencia de cada imagen su propia .coo.1:
    iraf.daofind(imag,output="default",starmap="",skymap="",interactive="no",verify="no")
#
    refcoor= imag+'.coo.1'                               # referencia de coordenadas .coo
    print('refcoor=', refcoor)
#
    iraf.imdelete(imag+'.mag.*',verify="no")             # borra antes fichero de salida  
    iraf.phot(imag, coords=refcoor, output="default")
	#Tablas con MAG no INDEF y error MERR no INDEF en el filtro (fotometria valida).
    iraf.delete(imag+'_'+filtro[j]+'bien.mag.*')                   # borra si ya existe 
    iraf.txselect(imag+'.mag.1',imag+'_'+filtro[j]+'bien.mag.1','MAG!=INDEF && MERR!=INDEF') 
	#Tablas con MAG=INDEF o MERR=INDEF, en el filtro (fotometria no valida). 
    iraf.delete(imag+'_'+filtro[j]+'indef.mag.*')                   # borra si ya existe 
    iraf.txselect(imag+'.mag.1',imag+'_'+filtro[j]+'indef.mag.1','MAG==INDEF || MERR==INDEF')
#
# Los ficheros de extension '.mag' tienen mas informacion de la que en 
# general nos interesa. Podemos extraer solo las columnas en las que tenemos 
# interes con la tarea de IRAF 'txdump', especificando en el parametro 'fields'. 
#
# Los campos que nos interesa extraer son (como estan escritos en los ficheros '.mag'): 
# XCENTER,YCENTER: coordenadas del centro de las estrellas encontradas.
# MAG: magnitud de la estrella.
# MERR: error en la magnitud.
# IFILTER: filtro de la fotometria.
#
# La salida de 'txdump' es un fichero en formato ascii, y le damos el nombre 
# de la imagen de entrada con extension  '.phot' 
# Stdout=imag+".phot"  para redireccionar la salida a ese fichero 
# Utilizamos las tablas con magnitudes buenas, de extension "bien.mag.1" 
#
    iraf.delete(imag+'_'+filtro[j]+'.phot',verify="no")       # Borra salida .phot si ya existe  
    iraf.txdump(imag+'_'+filtro[j]+'bien.mag.1', fields="XCENTER,YCENTER,MAG,MERR,XAIRMASS,\
IFILTER",expr="yes",header="no", parameters="yes", Stdout=imag+'_'+filtro[j]+'.phot')

	#Mostramos las listas:
lista_M67_V= listasfot[0]
lista_M67_R= listasfot[1]
lista_M67_I= listasfot[2]


# La fotometría resultante está en las tablas '.phot' con XCENTER, YCENTER, MAG, MERR, XAIRMASS, IFILTER 





# GRÁFICAS:
 
	#Filtro V:
leyenda= [' ']
leyenda.pop(0)                      # quita el primer elemento de la lista

pl.clf()                            # limpia la grafica anterior 
for imag in lista_M67_V: 
   Vxc, Vyc, Vmag, Vmerr = np.loadtxt(imag+"_V.phot",usecols=(0,1,2,3),unpack=True) 
   pl.plot(Vmag, Vmerr, 'o', markersize=1.5)          # circulos 
   leyenda.append(imag+"_V.phot")


pl.xlabel("V mag") 
pl.ylabel("err V mag") 
pl.xlim(10.,22.) 
pl.ylim(-0.01,0.3) 
pl.legend(leyenda,loc=2,fontsize='xx-small')
pl.title('Magnitudes instrumentales')
pl.savefig("Vmag-errVmag.png") 
pl.show() 


	#Filtro R: 
leyenda= [' ']
leyenda.pop(0)               # quita el primer elemento de la lista

pl.clf()   
for imag in lista_M67_R: 
   Rxc, Ryc, Rmag, Rmerr = np.loadtxt(imag+"_R.phot",usecols=(0,1,2,3),unpack=True) 
   pl.plot(Rmag, Rmerr, 'o', markersize=1.5)          # circulos 
   leyenda.append(imag+"_R.phot")


pl.xlabel("R mag") 
pl.ylabel("err R mag") 
pl.xlim(10.,22.) 
pl.ylim(-0.01,0.3) 
pl.legend(leyenda,loc=2,fontsize='xx-small')
pl.title('Magnitudes instrumentales')
pl.savefig("Rmag-errRmag.png") 
pl.show() 


	#Filtro I: 
leyenda= [' ']
leyenda.pop(0)               # quita el primer elemento de la lista

pl.clf()   
for imag in lista_M67_I: 
   Ixc, Iyc, Imag, Imerr = np.loadtxt(imag+"_I.phot",usecols=(0,1,2,3),unpack=True) 
   pl.plot(Imag, Imerr, 'o', markersize=1.5)          # circulos 
   leyenda.append(imag+"_I.phot")


pl.xlabel("I mag") 
pl.ylabel("err I mag") 
pl.xlim(10.,22.) 
pl.ylim(-0.01,0.3) 
pl.legend(leyenda,loc=2,fontsize='xx-small')
pl.title('Magnitudes instrumentales')
pl.savefig("Imag-errImag.png") 
pl.show() 


	# Listamos la masa de aire, Texp y filtro, para ver que relacion hay:  

iraf.hselect('alO*.fits',"$I, AIRMASS, EXPTIME, INSFILTE",expr='yes')  

# La masa de aire es casi identica, por lo cual no es la razon. 
# Pero el tiempo de exposicion crece de la primera a la ultima para cada filtro 
# EXPTIME= 5, 20, 40, 50 s. Es claro que el error va asociado a EXPTIME.  
# El mayor salto en magnitud del error es entre la primera y segunda imagen,  
# cuando EXPTIME pasa de 5 a 20 s. En cambio, el error en las dos ultimas
# casi es identico, pues el efecto de pasar de EXPTIME= 40 s a
# EXPTIME= 50 s cambia poco el numero de cuentas.  

# Es decir, las imagenes con tiempo de exposicion mayor, dan un error menor para
# una magnitud dada, y alcanzan una magnitud limite mayor (que corresponde a
# estrellas mas debiles) para un error dado, pues vemos que sus puntos se
# situan desplazados a la derecha en el eje de magnitudes de las graficas).

