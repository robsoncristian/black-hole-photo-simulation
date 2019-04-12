import numpy as np
import ehtim as eh

obs = eh.obsdata.load_uvfits('./data/sgraimage.uvfits')

obs.plotall('u','v', conj=True)

obs.plotall('uvdist', 'amp')

obs.plot_bl('SMA','ALMA', 'phase')

obs.plot_cphase('LMT', 'SPT', 'ALMA')

##

npix = 128 
fov = 200 * eh.RADPERUAS

##

dbeam = obs.dirtybeam(npix,fov)
dbeam.display()

##

cbeam = obs.cleanbeam(npix,fov)
cbeam.display()

##

dim = obs.dirtyimage(npix, fov)
dim.display()

##

beamparams = obs.fit_beam()
res = obs.res()

##

zbl = 2.5
prior_fwhm = 100*eh.RADPERUAS
gaussparams = (prior_fwhm, prior_fwhm, 0.0)
emptyprior = eh.image.make_square(obs, npix, fov)
gaussprior = emptyprior.add_gauss(zbl, gaussparams)
gaussprior.display()

##

out = eh.imager_func(obs, gaussprior, gaussprior, zbl, d1="vis", alpha_d1=50, s1="gs",maxit=100)

##

outblur = out.blur_gauss(beamparams, 0.5)
out = outblur
outblur = eh.imager_func(obs, out, out, zbl, d1="vis", alpha_d1=10 , s1="gs", maxit=150)