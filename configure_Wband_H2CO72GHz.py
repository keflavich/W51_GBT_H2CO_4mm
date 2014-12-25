# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# 4mm line setup FL1 72GHz
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Original:
"""
receiver  = 'Rcvr68_92'
beam      = 'B12'
obstype   = 'Spectroscopy'
backend   = 'Spectrometer'
nwin      = 1
restfreq  = 72000.
deltafreq = 0
bandwidth = 800
swmode    = "tp_nocal"
swtype    = "none"
swper     = 0.2
swfreq    = 0, 0
tint      = 2.0
vlow      = 0.
vhigh     = 0.
vframe    = "lsrk"
vdef      = "Radio"
pol       = "Linear"
nchan  =  "high"
spect.levels = 3
"""
# KFPA + VEGAS
"""
receiver = 'RcvrArray18_26'
beam = 'all'
obstype = 'Spectroscopy'
backend = 'VEGAS'
dopplertrackfreq = 23694.47
swmode = "tp"
swtype = "none"
swper = 0.5
swfreq =0.0,0.0
tint = 1.0
broadband = 0
vlow = 0
vhigh = 0
vframe = "lsrk"
vdef = "Radio"
noisecal = "lo"
pol = "Circular"
vegas.vpol='self'
vegas.subband = 8
nchan = "low"
bandwidth = 23.44
deltafreq = 0
restfreq = 23694.47, 23722.63, 23870.13, 24139.42, 24532.99, 24506.28, 24515.00, 23780.92
"""

# H2CO 1-0 72.83795
# H2CO 514-515 72.4091
# H213CO 1-0 71.02478
# H2C18O 1-0 69.41542
# H213CO 514-515 68.86456

myconfig = """
receiver  = 'Rcvr68_92'
beam      = 'B12'
obstype   = 'Spectroscopy'
backend   = 'VEGAS'
restfreq  = 69000., 70000., 71000., 72500.
dopplertrackfreq = 72837.95
deltafreq = 0
bandwidth = 1500 # usable = 1250
nchan     = "high"
swmode    = "tp_nocal"
swtype    = "none"
swper     = 0.2
swfreq    = 0, 0
tint      = 1.0
vlow      = 0.
vhigh     = 0.
vframe    = "lsrk"
vdef      = "Radio"
pol       = "Linear"
"""

Configure(myconfig)
Balance()
