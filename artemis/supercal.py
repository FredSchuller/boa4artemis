# A super-function for great reduction of the best calibration scans ever. Really.
#
def supercal(snum,band=450,radius=-2.):
    tmp = redpnt(snum,band=band,weak=1,bright=1,showNEFD=1)
    if tmp != -1:
        data.doMap(system='eq',oversamp=5,noPlot=1)
        snr = copy.deepcopy(data.Map)
        snr.Data *= sqrt(data.Map.Weight)
        data.flagSource(model=snr,threshold=10.)
        data.flattenFreq(below=0.5,hiref=0.8)
        data._DataAna__statistics()
        data.computeWeight()
        data.unflag(flag=8)
        data.doMap(oversamp=9,sizeX=[-50,50],sizeY=[-50,50],noPlot=1)
        data.Map.smoothBy(data.BolometerArray.BeamSize / 3.)
        data.solvePointingOnMap(radius=-5)
        res = data.PointingResult
        x0 = res['gauss_x_offset']['value']
        y0 = res['gauss_y_offset']['value']
        data.solvePointingOnMap(radius=radius,plot=1,Xpos=x0,Ypos=y0)
        if data.PointingResult != -1:
            meas_flux = data.PointingResult['gauss_peak']['value']
        else:
            meas_flux = 0.
            
        source_name = data.ScanParam.Object
        if source_name in ['Uranus','Neptune','Mars']:
            astrotime,astrodate=getAstroDate(data)
            if band == 350:
                beam = 7.65   # after 1/3-beam smoothing
	        freq = 865.
            else:
                beam = 9.95   # after 1/3-beam smoothing
	        freq = 666.
            expect_flux = PlanetFlux(source_name,astrotime,astrodate,str(beam),str(freq))
            
        else:
            if band == 350:
                calibFluxes = calibF350
            else:
                calibFluxes = calibF450
            if calibFluxes.has_key(string.upper(source_name)):
                expect_flux = calibFluxes[string.upper(source_name)]
            else:
                expect_flux = -1.
        
    percent = 100.0*meas_flux/expect_flux
    print "-----------------------------------------------------------"
    print "FLUX %s:  %7.2f [expected: %7.2f, %6.2f percent]"%(source_name,meas_flux,expect_flux,percent)
    print "-----------------------------------------------------------"
    return meas_flux/expect_flux
