Spectral Lines
==============

from astroquery.splatalogue import Splatalogue
Splatalogue.LINES_LIMIT = 1e6
lines = Splatalogue.query_lines(67*u.GHz, 74*u.GHz, energy_max=200, energy_type='eu_k')
lines.write("all_lines_67to74GHz.fits", format='fits', clobber=True)
lines['Species', 'Chemical Name', 'Freq-GHz', 'Meas Freq-GHz', 'Resolved QNs', 'CDMS/JPL Intensity', 'E_L (K)', 'E_U (K)',].pprint()
h2co = Splatalogue.query_lines(67*u.GHz, 74*u.GHz, energy_max=200, energy_type='eu_k', chemical_name='Formaldehyde')
h2co.write("h2co_67to74GHz.fits")
h2co['Species', 'Chemical Name', 'Freq-GHz', 'Meas Freq-GHz', 'Resolved QNs', 'CDMS/JPL Intensity', 'E_L (K)', 'E_U (K)',].pprint()

    Species Chemical Name Freq-GHz Meas Freq-GHz     Resolved QNs    CDMS/JPL Intensity  E_L (K)   E_U (K)
    ------- ------------- -------- ------------- ------------------- ------------------ --------- ---------
     H213CO  Formaldehyde       --      68.86455       5(1,4)-5(1,5)            -4.2852  61.27903  64.58399
     H213CO  Formaldehyde       --      68.86455       5(1,4)-5(1,5)            -4.2852  61.27903  64.58399
     H213CO  Formaldehyde 68.86456      68.86455       5(1,4)-5(1,5)                0.0   61.2786  64.58355
       HDCO  Formaldehyde 69.14252            --       8(2,6)-9(1,9)            -6.4636  140.9671  144.2854
       HDCO  Formaldehyde  69.2673            --       8(2,6)-9(1,9)            -6.5165 140.96638 144.29067
     H2C18O  Formaldehyde 69.41542      69.41544       1(0,1)-0(0,0)                0.0       0.0    3.3314
     H2C18O  Formaldehyde       --      69.41544       1(0,1)-0(0,0)            -4.2414       0.0    3.3314
     H2C18O  Formaldehyde       --       69.4168       1(0,1)-0(0,0)            -4.2406       0.0   3.33146
     H213CO  Formaldehyde 71.02478      71.02479       1(0,1)-0(0,0)                0.0       0.0   3.40863
     H213CO  Formaldehyde       --      71.02479       1(0,1)-0(0,0)            -4.2115       0.0   3.40863
     H213CO  Formaldehyde       --      71.02479       1(0,1)-0(0,0)            -4.2115       0.0   3.40863
       D2CO  Formaldehyde 71.42132            --       9(2,7)-9(2,8)                0.0 147.28387 150.71153
       D2CO  Formaldehyde 71.42133            --       9(2,7)-9(2,8)            -4.3526 147.28373 150.71139
       D2CO  Formaldehyde 71.42134            --       9(2,7)-9(2,8)            -4.3525 147.28403 150.71169
       H2CO  Formaldehyde 72.40906            -- 5(1,4)-5(1,5),F=4-4            -4.8146   62.4522  65.92727
       H2CO  Formaldehyde 72.40909            -- 5(1,4)-5(1,5),F=6-6            -4.6494   62.4522  65.92727
       H2CO  Formaldehyde       --      72.40909       5(1,4)-5(1,5)            -4.2326   62.4522  65.92727
       H2CO  Formaldehyde       --      72.40909       5(1,4)-5(1,5)            -4.2329   62.4522  65.92727
       H2CO  Formaldehyde 72.40909            -- 5(1,4)-5(1,5),F=5-5            -4.7392   62.4522  65.92727
       H2CO  Formaldehyde  72.4091       72.4091       5(1,4)-5(1,5)                0.0  62.45263   65.9277
       H2CO  Formaldehyde       --      72.83795       1(0,1)-0(0,0)            -4.1789       0.0   3.49565
       H2CO  Formaldehyde       --      72.83795       1(0,1)-0(0,0)            -4.1792       0.0   3.49565
       H2CO  Formaldehyde 72.83795      72.83795       1(0,1)-0(0,0)                0.0       0.0   3.49565
