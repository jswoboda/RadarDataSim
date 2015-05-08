#!/usr/bin/env python
"""
Created on Tue Apr 21 11:09:42 2015

@author: John Swoboda
"""
import ConfigParser,os,inspect
import scipy as sp
import const.sensorConstants as sensconst
from beamtools.bcotools import getangles
from utilFunctions import make_amb
from const.physConstants import v_C_0
import json
import pdb
import pickle
def makeconfigfile(fname,beamlist,radarname,simparams):

    cfgfile = open(fname,'w')
    Config = ConfigParser.ConfigParser()
    Config.add_section('SensorParameters')
    Config.set('SensorParameters','radarname',radarname)
    Config.set('SensorParameters','beamlist',beamlist)

    Config.add_section('SimParameters')
    for ikey in simparams.keys():
        Config.set('SimParameters',ikey,simparams[ikey])

    Config.write(cfgfile)
    cfgfile.close()
def makepicklefile(fname,beamlist,radarname,simparams):
    pickleFile = open(fname, 'wb')
    pickle.dump([{'beamlist':beamlist,'radarname':radarname},simparams],pickleFile)
    pickleFile.close()
def readconfigfile(fname):

    ftype = os.path.splitext(fname)[-1]
    if ftype=='.ini':

        Config = ConfigParser.ConfigParser()
        Config.read(fname)
        simpms = ConfigSectionMap(Config,'SensorParameters')
        beamlist = json.loads(simpms['beamlist'])
        angles = getangles(beamlist,simpms['radarname'])
        ang_data = sp.array([[iout[0],iout[1]] for iout in angles])
        sensdict = sensconst.getConst(simpms['radarname'],ang_data)
        simparamstemp = ConfigSectionMap(Config,'SimParameters')
        simparams = {}
        simparams['amb_dict'] = make_amb(sensdict['fs'],simparams['ambupsamp'],
            sensdict['t_s']*len(pulse),len(pulse))
        simparams['angles']=angles
        simparams['dtype'] = eval('sp.complex'+simparams['nbits'])
        simparams['species']=eval(simparams['species'])
        rng_lims = simparams['RangeLims']
        rng_gates = sp.arange(rng_lims[0],rng_lims[1],sensdict['t_s']*v_C_0*1e-3)
        simparams['Timevec']=sp.arange(0,time_lim,simparams['Fitinter'])
        simparams['Rangegates']=rng_gates
    elif ftype=='.pickle':
        pickleFile = open(fname, 'rb')
        dictlist = pickle.load(pickleFile)
        pickleFile.close()
        angles = getangles(dictlist[0]['beamlist'],dictlist[0]['radarname'])
        ang_data = sp.array([[iout[0],iout[1]] for iout in angles])
        sensdict = sensconst.getConst(dictlist[0]['radarname'],ang_data)

        simparams = dictlist[1]
        time_lim = simparams['TimeLim']
        pulse  = simparams['Pulse']
        simparams['amb_dict'] = make_amb(sensdict['fs'],simparams['ambupsamp'],
            sensdict['t_s']*len(pulse),len(pulse))
        simparams['angles']=angles
        rng_lims = simparams['RangeLims']
        rng_gates = sp.arange(rng_lims[0],rng_lims[1],sensdict['t_s']*v_C_0*1e-3)
        simparams['Timevec']=sp.arange(0,time_lim,simparams['Fitinter'])
        simparams['Rangegates']=rng_gates

    return(sensdict,simparams)


def ConfigSectionMap(Config,section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def main():
    curpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    testpath = os.path.join(os.path.split(curpath)[0],'testdata')


if __name__== '__main__':
    main()