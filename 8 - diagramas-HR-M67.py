# DIAGRAMAS HR:

	#Importamos módulos:  

import numpy as np
import pylab as pl
from pyraf import iraf 

	#Creamos las listas de imagenes alineadas de M67 en los filtros V, R, I:

lista_M67_V= iraf.hselect("alO15*.fits","$I","OBJECT='M67_V'&INSFILTE='V'",Stdout=1) 
lista_M67_R= iraf.hselect("alO15*.fits","$I","OBJECT='M67_R'&INSFILTE='R'",Stdout=1) 
lista_M67_I= iraf.hselect("alO15*.fits","$I","OBJECT='M67_I'&INSFILTE='I'",Stdout=1) 

print('    ')
print('lista_M67_V:',lista_M67_V)
print('lista_M67_R:',lista_M67_R)
print('lista_M67_I:',lista_M67_I)
print('    ')

	#Emparejamiento de V con R:

for i in range(len(lista_M67_V)):
   iraf.tmatch(lista_M67_R[i]+"_Rcal.phot", lista_M67_V[i]+"_Vcal.phot",\
"M67_VR_combinada_"+str(i)+str(i)+".caldat", "c1,c2", "c1,c2",1.) 

	#Emparejamiento de V con I:

for i in range(len(lista_M67_V)):
   iraf.tmatch(lista_M67_I[i]+"_Ical.phot", lista_M67_V[i]+"_Vcal.phot",\
"M67_VI_combinada_"+str(i)+str(i)+".caldat", "c1,c2", "c1,c2",1.) 


print('    ')
print('Conviene mirar que ficheros .caldat se han creado en el disco, y el contenido de ellos.')
print('    ')


# Diagramas color-magnitud o HR del cumulo: 

	#Restringimos el error en mag para V,R,I: 
errmax= 0.10

	#Diagrama de magnitud V frente a color (V-R): 

for i in range(len(lista_M67_V)):
  Rmag1,Rerr,Vmag1,Verr= np.loadtxt("M67_VR_combinada_"+str(i)+str(i)+".caldat",unpack=True,usecols=(2,3,6,7))
  inderr= np.where((Verr <= errmax)*(Rerr <= errmax))    # errores Verr <= errmax y Rerr<= errmax
  Vmag= Vmag1[inderr] 
  Rmag= Rmag1[inderr]
  print('    ')
  print('Numero de puntos inicial en V y R: ',Vmag1.size, Rmag1.size)
  print('Numero de puntos con Verr, Rerr <= errmax : ',Vmag.size, Rmag.size)
  VR = Vmag - Rmag     # color (V - R) 
  pl.plot(VR, Vmag, 'o',markersize=1.5)   # fotometria calibrada

pl.axis([0.2, 1.2, 18., 10.]) 
pl.xlabel("(V - R)") 
pl.ylabel("V mag") 
pl.title('M67 , IAC80 ')
pl.savefig("M67-diagramaHR-V-VR.png") 
pl.show() 


	#Diagrama de magnitud V frente a color (V-I): 

for i in range(len(lista_M67_V)):
  Imag1,Ierr,Vmag1,Verr= np.loadtxt("M67_VI_combinada_"+str(i)+str(i)+".caldat",unpack=True,usecols=(2,3,6,7))
  inderr= np.where((Verr <= errmax)*(Ierr <= errmax))    # errores Verr <= errmax y Ierr<= errmax
  Vmag= Vmag1[inderr] 
  Imag= Imag1[inderr]
  print('    ')
  print('Numero de puntos inicial en V y I: ',Vmag1.size, Imag1.size)
  print('Numero de puntos con Verr, Ierr <= errmax : ',Vmag.size, Imag.size)
  VI = Vmag - Imag     # color (V - I) 
  pl.plot(VI, Vmag, 'o',markersize=1.5)   # fotometria calibrada

pl.axis([0.5, 1.7, 18., 10.]) 
pl.xlabel("(V - I)") 
pl.ylabel("V mag") 
pl.title('M67 , IAC80 ')
pl.savefig("M67-diagramaHR-V-VI.png") 
pl.show() 

