
#NORMALIZACIÓN DE FLATS:

	#Importamos módulos:
import numpy,glob
from pyraf import iraf

	#Ordenamos lista de FLATS corregidos por BIAS:
listaflats_b = sorted(glob.glob('bF*.fits'))
listaflats_b

	#Los FLATS dependen de la ganancia de los píxeles para cada filtro, así que separamos:
	#FLATS en V:
listaflats_V = iraf.hselect('bF*.fits','$I',"INSFILTE='V' ", Stdout=1)
	#Comprobación de los FLATS de V:
for m in listaflats_V:
	iraf.imhead(m)				#Mostramos el header y tiene que ser de filtro V

	#FLATS en R:
listaflats_R= iraf.hselect('bF15*.fits','$I',"INSFILTE='R' ",Stdout=1)
	#Comprobación de los FLATS de R:
for m in listaflats_R:
	iraf.imhead(m)				#Mostramos el header y tiene que ser de filtro R

	#FLATS en I:
listaflats_I= iraf.hselect('bF15*.fits','$I',"INSFILTE='I' ",Stdout=1)
	#Comprobación de los FLATS de I:
for m in listaflats_I:
	iraf.imhead(m)				#Mostramos el header y tiene que ser de filtro I





#COMBINAMOS FLATS DE CADA FILTRO:

	#Paquetes para poder combinar:
iraf.ctio() # carga m \u0301odulo con tarea apropos
iraf.apropos('combine') # tareas IRAF con la cadena 'combine'
iraf.imred()
iraf.ccdred()
iraf.ccdred.instrument= ' ' # espacio entre las comillas
iraf.ccdproc.fixpix='no' # no corrige de pixeles malos
iraf.ccdproc.zerocor='no' # no corrige de imagen biasmedio
iraf.ccdproc.darkcor='no' # no corrige de corriente de oscuridad
iraf.ccdproc.flatcor='no' # no corrige de flat
iraf.ccdproc.readaxis='line' # como se lee el CCD

	#Borramos flatmedios ya creados just in case:
iraf.imdelete('Flatmedio_*', verify='no')

	#Calculo de los flats promedio en V, R, I con 'flatcombine':
iraf.flatcombine(','.join(listaflats_V),output='Flatmedio_V',combine='average',\
reject='avsigclip',ccdtype=' ',subsets='no',scale='none',process='yes')

iraf.flatcombine(','.join(listaflats_R),output='Flatmedio_R',combine='average',\
reject='avsigclip',ccdtype=' ',subsets='no',scale='none',process='yes')

iraf.flatcombine(','.join(listaflats_I),output='Flatmedio_I',combine='average',\
reject='avsigclip',ccdtype=' ',subsets='no',scale='none',process='yes')

	#Muestra los promedios de cada filtro en la DS9:
iraf.display('Flatmedio_V',1,zscale='yes',zrange='yes',ztran='linear',fill='no')
iraf.display('Flatmedio_R',2,zscale='yes',zrange='yes',ztran='linear',fill='no')
iraf.display('Flatmedio_I',3,zscale='yes',zrange='yes',ztran='linear',fill='no')

	#Estadísticas de los FLATS:
section='[500:600,500:600]'			#Porción pequeña de la imagen para estadísiticas:

iraf.imstat("Flatmedio_V"+section, fields='image,npix,mean,stddev',format='yes')
iraf.imstat('Flatmedio_R'+section, fields='image,npix,mean,stddev',format='yes')
iraf.imstat('Flatmedio_I'+section, fields='image,npix,mean,stddev',format='yes')





#NORMALIZACIÓN DE FLATS:

	#Estadísticas de cada filtro:
section='[10:2000,10:2000]'
estadV= iraf.imstat('Flatmedio_V'+section, fields='npix,mean,stddev',format='no',Stdout=1)
estadR= iraf.imstat('Flatmedio_R'+section, fields='npix,mean,stddev',format='no',Stdout=1)
estadI= iraf.imstat('Flatmedio_I'+section, fields='npix,mean,stddev',format='no',Stdout=1)

	#Identificamos los valores de interés: (número de píxeles, media y desviación)
npixV, meanV, stddevV= estadV[0].split()
npixR, meanR, stddevR= estadR[0].split()
npixI, meanI, stddevI= estadI[0].split()

	#Normalizamos:
iraf.imdelete('Flat_norm_V',verify='no')				#Borramos si ya existe
iraf.imdelete('Flat_norm_R',verify='no')				#Borramos si ya existe
iraf.imdelete('Flat_norm_I',verify='no')				#Borramos si ya existe
iraf.imarith('Flatmedio_V', '/', float(meanV), 'Flat_norm_V')
iraf.imarith('Flatmedio_R', '/', float(meanR), 'Flat_norm_R')
iraf.imarith('Flatmedio_I', '/', float(meanI), 'Flat_norm_I')
	
	#Comprobamos que la media es 1 y que las desviaciones son pequeñas:
iraf.imstat('Flat_norm_V'+section, fields='image,npix,mean,stddev',format='yes')
iraf.imstat('Flat_norm_R'+section, fields='image,npix,mean,stddev',format='yes')
iraf.imstat('Flat_norm_I'+section, fields='image,npix,mean,stddev',format='yes')

	#Podemos ver los flats normalizados, usando el puntero para ver las zonas más brillantes que tendrán valores por encima de 1 y las menos que estarán por debajo de 1:
iraf.display('Flat_norm_V',1,zscale='yes',zrange='yes',ztran='linear',fill='no')
iraf.display('Flat_norm_R',2,zscale='yes',zrange='yes',ztran='linear',fill='no')
iraf.display('Flat_norm_I',3,zscale='yes',zrange='yes',ztran='linear',fill='no')


