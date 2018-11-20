import numpy as np
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import accuracy_score, classification_report  

excellent = np.random.randint(85, 100,(100))  #np.random.RandomState(0)
print 'excellent:', excellent

good = np.random.randint(60, 84, (100))
print 'good:', good

bad = np.random.randint(0, 59, (100))
print 'bad:', bad

y1 = np.array([1]*100)
#print 'y1:', y1
y2 = np.array([2]*100)
#print 'y2:', y2
y3 = np.array([3]*100)
#print 'y3:', y3
y = np.hstack((y1, y2, y3)) #.reshape(1, 3)
print 'y:', y.shape


# X = rng.rand(3, 3)
# print 'X:', X
# y = rng.binomial(1, 0.5, 100)
# print 'y:', y
# X_test = rng.rand(5, 10)
# print 'X_test', X_test

X = np.hstack((excellent, good, bad)).reshape(300, 1)

#print X.shape

X_test = np.array([39.9, 98, 70]).reshape(3, 1)


print 'X_test:', X_test, X_test.shape
clf = SVC(probability=True)
#clf = OneVsRestClassifier(estimator=SVC(gamma='scale', random_state=0))
print '=====', clf.fit(X, y) #.predict_proba(X_test)
#clf.set_params(kernel='linear').fit(X, y)
#clf.predict(X_test)

my_logreg_proba = clf.predict_proba(X_test)  
my_logreg_pred = clf.predict(X_test)

print X_test, my_logreg_pred
#print(accuracy_score(X_test, my_logreg_pred))  
# print(classification_report(X_test, my_logreg_pred))

for index in range (3):  
    print(my_logreg_proba[index])  
    print("Predict label:", my_logreg_pred[index])  
    print("Correct label:", X_test[index])

b=np.loadtxt('training_dataset.txt', 'S5', delimiter=',', converters={0: lambda s: s.replace(' ', '_')} )
print 'b:', b
print 'b.shape:', b.shape, b[:,0]


text_clf = Pipeline([('vect', CountVectorizer(stop_words='english', token_pattern='\w+')),
                    ('text_clf', TfidfTransformer(norm ='l1')),
                    ('clf', SVC(kernel='linear', C=5, class_weight='balanced', probability=True)),
                    ])

text_clf.fit(b[:,0], b[:,1])
#text_clf.fit_transform(b[:,0], b[:,1])
print '$$$$$$$$$', text_clf.predict(['jason'])