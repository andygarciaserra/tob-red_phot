#CALIBRACIÓN FOTOMÉTRICA:


# Módulos de python necesarios:
import numpy as np
import glob 
import pylab as pl 
from pyraf import iraf




# Paquetes de IRAF:
iraf.noao.digiphot(_doprint=0) 
iraf.noao.digiphot.phot(_doprint=0) 
iraf.noao.digiphot.daophot(_doprint=0) 





	#Descargamos fichero de asterismos de M67 y mostramos en DS9:
iraf.display('referencia_M67_V.fits',1)
iraf.tvmark(1,"M67-asterismo-Schild.coo", mark="circle", radii="15,16,17,18", color=207)  


	#Creamos las listas de imagenes alineadas de M67 en los filtros V, R, I:
lista_M67_V= iraf.hselect("alO*.fits","$I","OBJECT?='M67*'&INSFILTE='V'",Stdout=1) 
lista_M67_R= iraf.hselect("alO*.fits","$I","OBJECT?='M67*'&INSFILTE='R'",Stdout=1) 
lista_M67_I= iraf.hselect("alO*.fits","$I","OBJECT?='M67*'&INSFILTE='I'",Stdout=1) 


	#Leemos ficheros .phot con la fotometría y medimos las estrellas del asterismo:
for imag in lista_M67_V:
   imag= imag+'_V.phot'
   iout= imag[:-12]+"_V_asterismo.phot"
   iraf.delete(iout,verify="no")  # Borra salida si ya existe  
   fiche2= 'M67-asterismo-Schild.coo'
   iraf.tmatch(imag,fiche2,iout,match1="c1,c2",match2="c1,c2",maxnorm="2.",incol1='1,2,3,4,5',incol2='1,2,3')
   print('Creado: ',iout) 


for imag in lista_M67_R:
   imag= imag+'_R.phot'
   iout= imag[:-12]+"_R_asterismo.phot"
   iraf.delete(iout,verify="no")  # Borra salida si ya existe  
   fiche2= 'M67-asterismo-Schild.coo'
   iraf.tmatch(imag,fiche2,iout,match1="c1,c2",match2="c1,c2",maxnorm="2.",\
incol1='1,2,3,4,5',incol2='1,2,3')
   print('Creado: ',iout)


for imag in lista_M67_I:
   imag= imag+'_I.phot'
   iout= imag[:-12]+"_I_asterismo.phot"
   iraf.delete(iout,verify="no")  # Borra salida si ya existe  
   fiche2= 'M67-asterismo-Schild.coo'
   iraf.tmatch(imag,fiche2,iout,match1="c1,c2",match2="c1,c2",maxnorm="2.",\
incol1='1,2,3,4,5',incol2='1,2,3')
   print('Creado: ',iout) 


	#Lee las magnitudes y colores fotometricos de las estrellas del asterismo:

XCa,YCa,Vfot,VRfot,VIfot=np.loadtxt("M67-asterismo-fot-Schild.dat",dtype='float',skiprows=7,usecols=(0,1,2,3,4),unpack=True)
print('XCa,YCa,Vfot,VRfot,VIfot=',XCa,YCa,Vfot,VRfot,VIfot)
Nast= XCa.size
print('Numero de estrellas del asterismo=',Nast)               


	#En vez de los ficheros toma el .phot de cada imagen apra medir la fotometría:

Vdif= np.zeros(100)
VRdifV= np.zeros(100)
VIdifV= np.zeros(100)
ndV= 0

for imag in lista_M67_V:
  xc, yc, Mins, err= np.loadtxt(imag+"_V.phot",usecols=(0,1,2,3),unpack=True) 
  nEst= xc.size
  ie=0
  while ie < nEst:
    j=0
    while j < Nast:
      dist= np.sqrt((xc[ie]-XCa[j])**2+(yc[ie]-YCa[j])**2)
      if dist <= 2.:
        Vdif[ndV ]= Mins[ie] - Vfot[j]
        VRdifV[ndV ]= VRfot[j]
        VIdifV[ndV ]= VIfot[j]
        ndV += 1
      j += 1
    ie += 1


print('      ')
print('Filtro V:')
print('Numero de medidas=',ndV)
print('Diferencias  (Vins - Vfot)=',Vdif[0:ndV-1])
Vdifmed= Vdif[0:ndV-1].mean()
print('Diferencia media <Vins - Vfot>=',Vdifmed)
print('Desviacion tipica (Vins - Vfot)=',Vdif[0:ndV-1].std())


Rdif= np.zeros(100)
VRdifR= np.zeros(100)
VIdifR= np.zeros(100)
ndR= 0

for imag in lista_M67_R:
  xc, yc, Mins, err= np.loadtxt(imag+"_R.phot",usecols=(0,1,2,3),unpack=True) 
  nEst= xc.size
  ie=0
  while ie < nEst:
    j=0
    while j < Nast:
      dist= np.sqrt((xc[ie]-XCa[j])**2+(yc[ie]-YCa[j])**2)
      if dist <= 2.:
        Rdif[ndR]= Mins[ie] - (Vfot[j] - VRfot[j])
        VRdifR[ndR]= VRfot[j]
        VIdifR[ndR]= VIfot[j]
        ndR += 1 
      j +=1
    ie += 1      

print('      ')
print('Filtro R:')
print('Numero de medidas=',ndR)
print('Diferencias  (Rins - Rfot)=',Rdif[0:ndR-1])
Rdifmed= Rdif[0:ndR-1].mean()
print('Diferencia media <Rins - Rfot>=',Rdifmed)
print('Desviacion tipica (Rins - Rfot)=',Rdif[0:ndR-1].std())


Idif= np.zeros(100)
VRdifI= np.zeros(100)
VIdifI= np.zeros(100)
ndI= 0

for imag in lista_M67_I:
  xc, yc, Mins, err= np.loadtxt(imag+"_I.phot",usecols=(0,1,2,3),unpack=True) 
  nEst= xc.size
  ie=0
  while ie < nEst:
    j=0
    while j < Nast:
      dist= np.sqrt((xc[ie]-XCa[j])**2+(yc[ie]-YCa[j])**2)
      if dist <= 2.:
        Idif[ndI]= Mins[ie] - (Vfot[j] - VIfot[j])
        VRdifI[ndI]= VRfot[j]
        VIdifI[ndI]= VIfot[j]
        ndI += 1 
      j +=1
    ie += 1

print('      ')
print('Filtro I:')
print('Numero de medidas=',ndI)
print('Diferencias  (Iins - Ifot)=',Idif[0:ndI-1])
Idifmed= Idif[0:ndI-1].mean()
print('Diferencia media <Iins - Ifot>=',Idifmed)
print('Desviacion tipica (Iins - Ifot)=',Idif[0:ndI-1].std())



	# Grafica de diferencias (Magins-Magfot) las diferencias frente a color: 

pl.clf()   
pl.subplot(211)
pl.plot(VRdifV[0:ndV-1],Vdif[0:ndV-1],'go',markersize=2.5)
pl.xlabel("(V-R)") 
pl.ylabel("( Vins - Vfot )") 
pl.xlim(0.2,0.6) 
pl.ylim(2.4,2.6) 
pl.title('Estrellas del asterismo de M67')

pl.subplot(212)
pl.plot(VIdifV[0:ndV-1],Vdif[0:ndV-1],'ro',markersize=2.5)
pl.xlabel("(V-I)") 
pl.ylabel("( Vins - Vfot )") 
pl.xlim(0.4,1.2) 
pl.ylim(2.4,2.6) 
pl.subplots_adjust(hspace=0.4)
pl.savefig("difV-VR-VI.png") 
pl.show() 


pl.clf()   
pl.subplot(211)
pl.plot(VRdifR[0:ndR-1],Rdif[0:ndR-1],'go',markersize=2.5)
pl.xlabel("(V-R)") 
pl.ylabel("( Rins - Rfot )") 
pl.xlim(0.2,0.6) 
pl.ylim(2.4,2.6) 
pl.title('Estrellas del asterismo de M67')

pl.subplot(212)
pl.plot(VIdifR[0:ndR-1],Rdif[0:ndR-1],'ro',markersize=2.5)
pl.xlabel("(V-I)") 
pl.ylabel("( Rins - Rfot )") 
pl.xlim(0.4,1.2) 
pl.ylim(2.4,2.6) 
pl.subplots_adjust(hspace=0.4)
pl.savefig("difR-VR-VI.png") 
pl.show() 



pl.clf()   
pl.subplot(211)
pl.plot(VRdifI[0:ndI-1],Idif[0:ndI-1],'go',markersize=2.5)
pl.xlabel("(V-R)") 
pl.ylabel("( Iins - Ifot )") 
pl.xlim(0.2,0.6) 
pl.ylim(2.8,3.3) 
pl.title('Estrellas del asterismo de M67')

pl.subplot(212)
pl.plot(VIdifI[0:ndI-1],Idif[0:ndI-1],'ro',markersize=2.5)
pl.xlabel("(V-I)") 
pl.ylabel("( Iins - Ifot )") 
pl.xlim(0.4,1.2) 
pl.ylim(2.8,3.3) 
pl.subplots_adjust(hspace=0.4)
pl.savefig("difI-VR-VI.png") 
pl.show() 


# Calibramos las magnitudes instrumentales, y las hacemos fotometricas.
# Como no se aprecian diferencias con el color, restamos las diferencias medias
# de (Magins - Magfot). Hace: Magfot_i = Magins_i - < Magins - Magfot> , con los
# valores de Vdifmed, Rdifmed, Idifmed.

Dmed= Vdifmed
for imag in lista_M67_V:
   imag1= imag+'_V.phot'
   iout= imag+'_Vcal.phot'
   xc, yc, Mins, err= np.loadtxt(imag1,usecols=(0,1,2,3),unpack=True) 
   iraf.delete(iout,verify="no")  # Borra salida si ya existe 
   sal= open(iout,'w')
   j=0
   while j <= (xc.size-1):
      sal.write('%.6f %.6f %.6f %.6f' %(xc[j],yc[j],Mins[j]-Dmed,err[j]))
      sal.write("\n")
      j += 1
   sal.close()
   print('Creado fichero con magnitudes fotometricas: ',iout) 

Dmed= Rdifmed
for imag in lista_M67_R:
   imag1= imag+'_R.phot'
   iout= imag+'_Rcal.phot'
   xc, yc, Mins, err= np.loadtxt(imag1,usecols=(0,1,2,3),unpack=True) 
   iraf.delete(iout,verify="no")  # Borra salida si ya existe 
   sal= open(iout,'w')
   j=0
   while j <= (xc.size-1):
      sal.write('%.6f %.6f %.6f %.6f' %(xc[j],yc[j],Mins[j]-Dmed,err[j]))
      sal.write("\n")
      j += 1
   sal.close()
   print('Creado fichero con magnitudes fotometricas: ',iout)

Dmed= Idifmed
for imag in lista_M67_I:
   imag1= imag+'_I.phot'
   iout= imag+'_Ical.phot'
   xc, yc, Mins, err= np.loadtxt(imag1,usecols=(0,1,2,3),unpack=True) 
   iraf.delete(iout,verify="no")  # Borra salida si ya existe 
   sal= open(iout,'w')
   j=0
   while j <= (xc.size-1):
      sal.write('%.6f %.6f %.6f %.6f' %(xc[j],yc[j],Mins[j]-Dmed,err[j]))
      sal.write("\n")
      j += 1
   sal.close()
   print('Creado fichero con magnitudes fotometricas: ',iout) 


