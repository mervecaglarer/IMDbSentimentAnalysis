import os
import time
from nlp import Classifier

start_time = time.time()

os.system('python movies\spiders\movieLink.py')
os.system('python movies\spiders\getComments.py')

classifier = Classifier()
classifier.tokenizers()
classifier.modelling()
rate = classifier.fit()

elapsed_time = time.time() - start_time
print("Fully Elapsed: "+str(elapsed_time))
file = open("tmp/links.csv","r")
link = file.readline()
file.close()

print(link)
print("Movie Positive Rate: %{}".format(rate))