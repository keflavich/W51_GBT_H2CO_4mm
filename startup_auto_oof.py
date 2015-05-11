#
# Example 4mm Rx Check Out script
#

catp= Catalog("/home/astro-util/astridcats/wband_pointing.cat")
# *** Comment out all but active target source:

#source="Jupiter"
#source="Mars"
#source="0319+4130"
source="2253+1608"
#source="0927+3902"
#source="1256-0547"
#source="1229+0203"
#source="1642+3948"
#source="2253+1608"
# nearest pointing source='1924+1540'

#Slew(source)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#Depending on available time run autooof (takes 30 min)
#at default frequency of 77GHz

AutoOOF(source)

Break("Wait for AutoOOF processing and send solutions")

AutoPeakFocus(source)

Break("Check and enter solutions")

#Check Spectrometer 
#77GHz
# old version: execfile("/home/astro-util/projects/4mm/config_line_FL2")
# 68-72 GHz FL1
print("WARNING: MAKE SURE THIS WORKS BEFORE CONTINUING")
execfile('/users/aginsbur/GBT15A-446/configure_Wband_H2CO72GHz.py')
Break("Confirm: did configuration complete?")
Slew(source)
Balance()
CalSeq("manual",10)
beamName1 = '1'
beamName2 = '2'
scanDuration = 30
#Nod data to verify calibration of both beams and polarizations
Nod(source, beamName1, beamName2, scanDuration)

source='1924+1540'
Slew(source)
Balance()
CalSeq("manual",10)
beamName1 = '1'
beamName2 = '2'
scanDuration = 30
#Nod data to verify calibration of both beams and polarizations
Nod(source, beamName1, beamName2, scanDuration)
