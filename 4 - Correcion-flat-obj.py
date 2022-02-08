
#CORRECIÓN DE FLATS DE LOS OBJETOS:

import numpy, os, glob
from pyraf import iraf

	#Listas de objetos por filtros:
listaobjetos = sorted(glob.glob("bO*.fits"))
lista_objetos_V = iraf.hselect("bO15*.fits","$I","INSFILTE='V' ",Stdout=1)
lista_objetos_R = iraf.hselect("bO15*.fits","$I","INSFILTE='R' ",Stdout=1)
lista_objetos_I = iraf.hselect("bO15*.fits","$I","INSFILTE='I' ",Stdout=1)

	#Comprobación:
for m in lista_objetos_I:
	iraf.imhead(m)
for m in lista_objetos_V:
	iraf.imhead(m)
for m in lista_objetos_R:
	iraf.imhead(m)
	
	#División de las imágenes por los FLATS:
for imag in lista_objetos_V:
  imout= "ff"+imag[1:] # sustituye el b por ff
  print(imout) # imagen resultante
  iraf.imdelete(imout,verify="no") # borra antes la imagen de salida
  iraf.imarith(imag, "/", "Flat_norm_V",imout)
  
for imag in lista_objetos_R:
  imout= "ff"+imag[1:] # sustituye el b por ff
  print(imout) # imagen resultante
  iraf.imdelete(imout,verify="no") # borra antes la imagen de salida
  iraf.imarith(imag, "/", "Flat_norm_R",imout)
  
for imag in lista_objetos_I:
  imout= "ff"+imag[1:] # sustituye el b por ff
  print(imout) # imagen resultante
  iraf.imdelete(imout,verify="no") # borra antes la imagen de salida
  iraf.imarith(imag, "/", "Flat_norm_I",imout)


	#DS9 antes y después:
iraf.display("bO151127_0157.fits",1,ztran="log")
iraf.display("ffO151127_0157.fits",2,ztran="log")
	
	#Estadística antes y después
iraf.imstat('bO151127_0157.fits[400:700,200:500]',fields='image,mean,stddev',format='no')
iraf.imstat('ffO151127_0157.fits[400:700,200:500]',fields='image,mean,stddev',format='no')
