
catp= Catalog("/home/astro-util/astridcats/wband_pointing.cat")
source='1924+1540'
Slew(source)

execfile('/users/aginsbur/GBT15A-446/configure_Wband_H2CO72GHz.py')
Balance()
CalSeq("manual",10)
beamName1 = '1'
beamName2 = '2'
scanDuration = 30
#Nod data to verify calibration of both beams and polarizations
Nod(source, beamName1, beamName2, scanDuration)
