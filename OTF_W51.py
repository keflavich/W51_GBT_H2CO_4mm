# OTF mapping

# -=-=-=-=-=-=-=-
# 4mm line setup 
# -=-=-=-=-=-=-=-

execfile('configure_Wband_H2CO72GHz.py')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Read my catalog
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

catp = Catalog("w51.cat")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Chopper Wheel Calibration
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

Slew('W51MainAndIRS2')
Balance()

CalSeq("auto",30.0)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Integrate on Source
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

Slew('W51MainAndIRS2')

#pick beam 2 
beamName = '2'

# NOTE TO SELF: be careful that all these are floats
rasize = 1.5/60. # RA Extent 1.5 arcmin
decsize = 1.5/60. # Dec Extent 1.5 arcmin
stepsize = 4./3600. # Step 4"
total_time = 30. # 30 minutes integ. time target

nscans = decsize / stepsize
scanDuration = total_time*60. / nscans # 80 seconds

RALongMap('W51MainAndIRS2',
          hLength = Offset("J2000", rasize, 0.0, cosv=True),
          vLength = Offset("J2000", 0.0, decsize, cosv=True),
          vDelta  = Offset("J2000", 0.0, stepsize, cosv=True),
          scanDuration = scanDuration,
          beamName=beamName)


CalSeq("auto",30.0)

nscans = rasize / stepsize
scanDuration = total_time*60. / nscans # 80 seconds

DecLatMap('W51MainAndIRS2',
          hLength = Offset("J2000", rasize, 0.0, cosv=True),
          vLength = Offset("J2000", 0.0, decsize, cosv=True),
          hDelta  = Offset("J2000", stepsize, 0.0, cosv=True),
          scanDuration = scanDuration,
          beamName=beamName)

CalSeq("auto",30.0)
