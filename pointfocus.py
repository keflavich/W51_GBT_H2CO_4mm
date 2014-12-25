# Point and focus for W-Band. 


catp = Catalog("/home/astro-util/astridcats/wband_pointing.cat")


# Closest to W51, 0.387 Jy
source = "1924+1540"

Slew(source)

#Peak
#AutoPeak(source)

#Optimize focus near target frequency (default auto frequency is 77GHz)
#AutoFocus(source,frequency=89000.,calSeq=False)

# Do AutoPeakFocus within one command including the CalSeq observations
AutoPeakFocus(source)

