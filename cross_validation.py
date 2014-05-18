import random
def crossvalidate(movie_file='csv_file.csv'):
		u=set(range(1,1001))
		s=[]
		for i in range(9):
			s.append(set(random.sample(u,100)))
			u-=s[i]
		s.append(u)

		for k in range(10):
			f=open(movie_file,'rb')
			f1=open('training'+str(k)+'.csv','w')
			f2=open('testing'+str(k)+'.csv','w')
			f1.write('imdb_id,title,rating,directors,writers,actors,budget,gross,financial score,score\n')
			f2.write('imdb_id,title,rating,directors,writers,actors,budget,gross,financial score,score\n')
			testing_set=set()
			training_set=set()
			for i in range(10):
				if i==k:
					testing_set=testing_set.union(s[i])
				else:
					training_set=training_set.union(s[i])
			for count,line in enumerate(f):
				if count in testing_set:
					f2.write(line.strip('\r'))
				if count in training_set:
					f1.write(line.strip('\r'))
			f1.close()
			f2.close()
			f.close()
#generate the trainingset and testing set for crossvalidating
crossvalidate()