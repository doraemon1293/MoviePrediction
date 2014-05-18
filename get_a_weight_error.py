import ga
import string
f=open('weight.txt','rb')
line= f.readline()
w=[string.atof(s) for s in line.split(', ')]
f.close()
print ga.costf(w)