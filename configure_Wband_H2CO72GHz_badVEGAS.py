# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# 4mm line setup FL1 72GHz
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# To use a different configuration, overwrite the file configure_Wband_H2CO72GHz


# H2CO 1-0 72.83795
# H2CO 514-515 72.4091
# H213CO 1-0 71.02478
# H2C18O 1-0 69.41542     (70000-1250/2 = 69375)
# H213CO 514-515 68.86456 (can't be done simultaneous with H2CO 1-0 without great risk)

myconfig = """
receiver  = 'Rcvr68_92'
beam      = 'B12'
obstype   = 'Spectroscopy'
backend   = 'VEGAS'
restfreq  = 72000., 72500.
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
vegas.vpol='self'
"""

Configure(myconfig)
Balance()
