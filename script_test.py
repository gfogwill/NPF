import dmps

nuk_file = 'C:\\Users\\Ger\\Desktop\\GERMAN\\clasification_eventos.nuk'
data2017 = 'C:\\Users\\Ger\\Desktop\\GERMAN\\datos_2017\\DMPSmara_2017.dat'
odir = 'test.bin'

DMPSdata = dmps.DMPS()
DMPSdata.load_data_with_labels(nukfile=nuk_file, datafile=data2017)
DMPSdata.to_htk_format(outdir=odir)
odir = 'test.lab'
DMPSdata.gen_htk_labels(outdir=odir)
print('dsf')