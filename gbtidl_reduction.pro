cd,'/users/aginsbur/GBT15A-446/spectra/'


offline,'AGBT15A_446_02'

calseq_man_gains,19,20,21,gains
wnod,24,gains=gains,ifnum=1
write_ascii,'W51_scan24_session2'

calseq_man_gains,95,96,97,gains
wnod,98,gains=gains,ifnum=1
write_ascii,'W51_scan98_session2'
;scan 139 looks broken

calseq_man_gains,100,101,102,gains
wnod,202,gains=gains,ifnum=1
; probably bad
write_ascii,'W51_scan202_session2'



offline,'AGBT15A_446_03'

calseq_man_gains,60,61,62,gains
wnod,63,gains=gains,ifnum=1
write_ascii,'W51_scan63_session3'
wnod,74,gains=gains,ifnum=1
write_ascii,'W51_scan74_session3'
wnod,76,gains=gains,ifnum=1
write_ascii,'W49N_scan76_session3'

calseq_man_gains,117,118,119,gains
wnod,120,gains=gains,ifnum=1
write_ascii,'W49N_scan120_session3'
wnod,132,gains=gains,ifnum=1
write_ascii,'W49N_scan132_session3'



offline,'AGBT15A_446_04'

calseq_man_gains,21,22,23,gains
wnod,24,gains=gains,ifnum=1
write_ascii,'W51_scan24_session4'

calseq_man_gains,69,70,71,gains
wnod,72,gains=gains,ifnum=1
write_ascii,'W51_scan72_session4'
