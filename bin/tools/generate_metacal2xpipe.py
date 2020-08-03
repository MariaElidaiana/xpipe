import h5py as h
import numpy as np

# Read the master file
#f = h.File('/project/projectdirs/des/www/y3_cats/Y3_mastercat_5_24_19_subsampled.h5', 'r')
f = h.File('/data/des81.b/data/mariaeli/y3_cats/full/Y3_mastercat_03_31_20.h5', 'r')


#Apply the metacal cuts
select_idx = f['index/select'][:] #for subsampled catalog
#select_idx = f['index/select_shape'][:]

#Getting the metacal data
ids = f['catalog/metacal/unsheared/coadd_object_id'][...][select_idx]
ra  = f['catalog/metacal/unsheared/ra'][...][select_idx]
dec = f['catalog/metacal/unsheared/dec'][...][select_idx]
g1  = f['catalog/metacal/unsheared/e_1'][...][select_idx]          
g2  = f['catalog/metacal/unsheared/e_2'][...][select_idx] 

R11 = f['catalog/metacal/unsheared/R11'][...][select_idx]
R22 = f['catalog/metacal/unsheared/R22'][...][select_idx]
R12 = f['catalog/metacal/unsheared/R12'][...][select_idx]
R21 = f['catalog/metacal/unsheared/R21'][...][select_idx]

g1sens        = R11
g2sens        = R22
g12sens       = (R12+R21)/2.
source_weight = np.ones(len(ids))                                            
z_mean        = f['catalog/bpz/unsheared/zmean_sof'][...][select_idx] 
z_sample      = f['catalog/bpz/unsheared/zmc_sof'][...][select_idx]

f.close()

print(len(ids))
print(min(z_mean), max(z_mean))
print(min(z_sample), max(z_sample))
print(np.count_nonzero(np.isnan(z_mean)))

mask = (~np.isnan(z_mean))&(~np.isnan(z_sample))&(z_mean>=0)&(ids!=0) #mask to remove z=NaNs, z<0 and IDs=0 

ids           = ids[mask]
ra            = ra[mask]
dec           = dec[mask]
g1            = g1[mask]
g2            = g2[mask]
g1sens        = g1sens[mask]
g2sens        = g2sens[mask]
g12sens       = g12sens[mask]
source_weight = source_weight[mask]
z_mean        = z_mean[mask]
z_sample      = z_sample[mask]

print(len(ids))
print(min(z_mean), max(z_mean))
print(min(z_sample), max(z_sample))
print(np.count_nonzero(np.isnan(z_mean)))

print("Saving ...")
#np.savetxt('/global/cscratch1/sd/mariaeli/Y3_DATA/Y3_mastercat_5_24_19_subsampled_metacal.dat',
np.savetxt('/data/des81.b/data/mariaeli/Y3_FULLDATA/Y3_mastercat_03_31_20_fullblind_metacal.dat',
           np.c_[ids, ra, dec, g1, g2, g1sens, g2sens, g12sens, source_weight, z_mean, z_sample], 
           fmt='%d %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f')




