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

Slew('w51m_irs2')
Balance()

CalSeq(type="manual", scanDuration=10.0, location="W51-OFF")


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Integrate on Source
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

Slew('w51m_irs2')

#pick beam 2 
beamName = '2'

# NOTE TO SELF: be careful that all these are floats
rasize = 1.5/60. # RA Extent 1.5 arcmin
decsize = 1.5/60. # Dec Extent 1.5 arcmin
stepsize = 4./3600. # Step 4"
total_time = 30. # 30 minutes integ. time target

nscans = decsize / stepsize
scanDuration = total_time*60. / nscans # 80 seconds

RALongMap('w51m_irs2',
          hLength = Offset("J2000", rasize, 0.0, cosv=True),
          vLength = Offset("J2000", 0.0, decsize, cosv=True),
          vDelta  = Offset("J2000", 0.0, stepsize, cosv=True),
          scanDuration = scanDuration,
          beamName=beamName)


CalSeq(type="manual", scanDuration=10.0, location="W51-OFF")
