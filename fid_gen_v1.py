#script for generating massive amounts of simulated nus spectra
#read in schedule files as text
#read in fully sampled cartesian .fid file
#write out simulated nus .fid files

import nmrglue as ng
import pylab
import numpy
import matplotlib

#use vector to specify schedule names
use=[]
i=0
while i < 500:
     use.append(i)
     i+=1

#function to read and store nus sampling sched  
def readfile(datafile):
     data=file(datafile,'r')
     contents=data.readlines()
     data.close()
     for x in range(len(contents)):
          contents[x]=int(contents[x])
     return contents

#generate data
fid_arr=['001','002','004']
arr=['16p','25p','32p','40p','56p','64p']
points_arr=['296']

for points in points_arr:
    print points
    for z in arr:
        print z
        #set data paths
        #schedules

        if z == '40p':
            nussched1='/Users/joannagiang/data_science_wandlab/schedules/'+points+'/'+z+'/lists/nus.0.'+z[0:1]+'.'+'304'+'.'
        else:        
            nussched1='/Users/joannagiang/data_science_wandlab/schedules/'+points+'/'+z+'/lists/nus.0.'+z[0:2]+'.'+'304'+'.'

        #cartesian data 
        datapath='/Users/joannagiang/data_science_wandlab/fid/'+points+'fid/'
        #output
        outpath='/Users/joannagiang/data_science_wandlab/sim_fid/'+points+'/'+z+'/'
        #output reference size
        refpath='/Users/joannagiang/data_science_wandlab/sim_fid/'+points+'/'+z+'/id.txt'

        for y in fid_arr:
            print y
            i=0
            temp2=[]
            while i < len(use):
                 if i == 0 or i == 499:
                     print i 
                 dic,dataref=ng.pipe.read(datapath+'test'+y+'.fid')

                 nussched=nussched1+str(use[i])
                 #nussched=nussched1
                 nus=readfile(nussched)
                 temp=[]
                 #identify complex pairs to keep
                 for x in range(len(nus)):
                      temp.append(nus[x]*2)
                      temp.append(nus[x]*2+1)
                 datae=dataref
                 #eliminate all other complex pairs
                 for x in range(len(datae)):
                      if x not in temp:
                           datae[x]=0
                 nz=(datae==0).any(1)
                 final=datae[nz==0,:]
                 temp2.append(len(final))
                 #write out
                 ng.pipe.write(outpath+y+'nustest'+str(use[i])+'.fid',dic,final,overwrite='True')
                 temp=[]
                 i+=1
            i=0
            #write text file of file names for automated batch processing in nmrpipe
            refsize=open(refpath,'w')
            for x in range(len(use)):
                 refsize.write(str(use[x]))
                 refsize.write('\n')
            refsize.close()




