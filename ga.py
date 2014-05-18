import random
import ib
import math
from scipy import stats
#get the Summation of error according with weight
def costf(weight):
	sum=0
	for t in range(10):
		movie_file='training'+str(t)+'.csv'
		index_file='index'+str(t)+'.csv'
		test_file='testing'+str(t)+'.csv'
		index=ib.indexbuilder(weight,movie_file,index_file)
		movie=ib.vectorbuilder(test_file,index)
		for key in movie.keys():
			temp=es(movie[key][0:5],weight)
			if (temp!=0):
				sum+=(temp-movie[key][5] )*(temp-movie[key][5] )
	return sum

#The estimated value by movie's feature
def es(scores,weight):
	sum=0
	sum_weight=0
	for i in range(len(scores)):
		if (scores[i]!=0):
			sum+=scores[i]*weight[i]
			sum_weight+=weight[i]
	if sum_weight!=0:
		return sum/sum_weight
	else:
		return 0

#Generate bunches of weighs by GA
def ga_opt(domain,movie_file='csv_file.csv',index_file='index.csv',test_file='test.csv',costf=costf,popsize=50,step=0.01,
                    mutprob=0.2,elite=0.2,maxiter=100,):
  # Mutation Operation
  def mutate(vec):
    i=random.randint(0,len(domain)-1)
    if random.random()<0.5 and vec[i]-step>domain[i][0]:
      return vec[0:i]+[round(vec[i]-step,2)]+vec[i+1:]
    elif vec[i]+step<domain[i][1]:
      return vec[0:i]+[round(vec[i]+step,2)]+vec[i+1:]
    else:
      return vec

  # Crossover Operation
  def crossover(r1,r2):
    i=random.randint(1,len(domain)-2)
    return r1[0:i]+r2[i:]

  # Build the initial population
  pop=[]
# build a set to gurantee the weight in pop are different
  pop_set=set()
  for i in range(popsize):
    vec=[round( random.uniform(domain[i][0], domain[i][1]),2)
         for i in range(len(domain))]
    pop.append(vec)
    pop_set=pop_set.union([str(vec)])
  # How many winners from each generation?
  topelite=int(elite*popsize)-1
#build the scores_index to avoid calculate the summation of error for the same weight repeatly
  scores_index={}
  # Main loop
  for i in range(maxiter):
    scores=[]
    for v in pop:
        temp_s=str(v)
# if the weight is caculated, get in fro, scores_index
        if scores_index.has_key(temp_s):
            score=scores_index[temp_s]
# otherwise, calculate it
        else:
            score=costf(v)
            scores_index.update({temp_s:score})
        scores.append((score,v))
        scores.sort()
    ranked=[v for (s,v) in scores]

    # Start with the pure winners
    pop=ranked[0:topelite]
    pop_set=set()
    for p in pop:
        pop_set=pop_set.union([str(p)])

    # Add mutated and bred forms of the winners
    while len(pop)<popsize:
      if random.random()<mutprob:

        # Mutation
        c=random.randint(0,topelite)
        temp=mutate(ranked[c])
        if not( str(temp) in pop_set ):
            pop.append(temp)
            pop_set=pop_set.union([str(temp)])

      else:
        # Crossover
        c1=random.randint(0,topelite)
        c2=random.randint(0,topelite)
        temp=mutate(crossover(ranked[c1],ranked[c2]))
        if not( str(temp) in pop_set ):
            pop.append(temp)
            pop_set=pop_set.union([str(temp)])
    # Print current best score
#    print '-----------'
#    print pop
#    print scores[0][0],scores[0][1]
#    print i
#  print scores
#  ib.write_index(index,index_file=index_file)
  print scores[0][0],scores[0][1]
  return scores[0]