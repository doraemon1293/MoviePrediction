import ga
import ib
import time

#domain = [(5.0,20.0),(5.0,20.0),(5.0,20.0),(2.0,10.0),(1.0,1.0)]
domain = [(3.0,6.0),(0.5,1.5),(3.0,7.0),(0.5,2.0),(0.5,0.5)]

#domain = [(1,1)]*5
times=10
t0=time.time()
temp=ga.ga_opt(domain,maxiter=70,step=0.05,popsize=50)
#optimised weight
w=temp[0]
# k-fold cross-validation error
error=temp[1]
t1=time.time()
#running time
c=t1-t0
f=open('result.txt','w')
f.write(str(w)+'\n')
f.write(str(error)+'\n')
f.write(str(c)+'\n')
f.close()
