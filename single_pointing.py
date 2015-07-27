
execfile('/users/aginsbur/GBT15A-446/configure_Wband_H2CO72GHz.py')
catp = Catalog("/users/aginsbur/GBT15A-446/w51.cat")
Slew('W51-Main')
Nod("W51-Main", "1", "2", 60)
