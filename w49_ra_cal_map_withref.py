# OTF mapping
# Calibration + RA OTF map
# Expected time ~40m

# -=-=-=-=-=-=-=-
# 4mm line setup 
# -=-=-=-=-=-=-=-

execfile('/users/aginsbur/GBT15A-446/configure_Wband_H2CO72GHz.py')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Read my catalog
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

catp = Catalog("/users/aginsbur/GBT15A-446/w51.cat")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Chopper Wheel Calibration
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

Slew('W49_Center')
Balance()

CalSeq(type="manual", scanDuration=10.0, location="W49-OFF")
Nod("W49-OFF", "1", "2", 60)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Integrate on Source
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

Slew('W49_Center')

#pick beam 2 
beamName = '2'

# NOTE TO SELF: be careful that all these are floats
rasize = 1.5/60. # RA Extent 1.5 arcmin
decsize = 1.5/60. # Dec Extent 1.5 arcmin
stepsize = 4./3600. # Step 4"
total_time = 30. # 30 minutes integ. time target

nscans = decsize / stepsize
scanDuration = total_time*60. / nscans # 80 seconds

RALongMapWithReference('W49_Center',
                       hLength = Offset("J2000", rasize, 0.0, cosv=True),
                       vLength = Offset("J2000", 0.0, decsize, cosv=True),
                       vDelta  = Offset("J2000", 0.0, stepsize, cosv=True),
                       referenceOffset = Offset("J2000",1,-1, cosv=True),
                       referenceInterval = 3,
                       scanDuration = scanDuration,
                       beamName=beamName)


Nod("W49-OFF", "1", "2", 60)
CalSeq(type="manual", scanDuration=10.0, location="W49-OFF")
