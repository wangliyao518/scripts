import numpy as np
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import accuracy_score, classification_report  

#b=np.loadtxt('training_dataset.txt', 'S5', delimiter=',', converters={0: lambda s: s.replace(' ', '_')} )
#print 'b:', b
#print 'b.shape:', b.shape, b[:,0]

b = np.recfromcsv('training_dataset.txt', delimiter=',', filling_values=np.nan, case_sensitive=True, deletechars='', replace_space=' ', dtype=None)
#b = numpy.recfromcsv('training_dataset.txt', delimiter=',' case_sensitive=True, deletechars=',', replace_space='_')

print 'b:', b, type(b)
#print 'b[:,0]', b[:,0]
#text_clf = Pipeline([('vect', CountVectorizer(stop_words='english', token_pattern='\w+')),
#                    ('text_clf', TfidfTransformer(norm ='l1')),
#                    ('clf', SVC(kernel='linear', C=5, class_weight='balanced', probability=True)),
#                    ])

#text_clf.fit(b[:,0], b[:,1])
#print 'predict result:', text_clf.predict(['qq'])