import os
import sys
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

#reload(sys)
#sys.setdefaultencoding("utf-8")



#datasets.load_files(container_path, description=None, categories=None, load_content=True, shuffle=True, encoding=None, decode_error='strict', random_state=0)

#os.chdir("sklearn_exercise")

twenty_train = datasets.load_files("bydata-train_000")
twenty_test = datasets.load_files("bydata-test")

print(twenty_train.data[0])
print(len(twenty_train.data[0]), type(twenty_train.data[0]))
#print ("\n".join(twenty_train.data[0].split("\n")[:3]))
print ("train target:", twenty_train.target_names)  #[twenty_train.target[0]]
print (twenty_train.target[:10])


count_vect = CountVectorizer(decode_error='ignore') #token_pattern='\d.*\d.*\.*\d.*'
X_train_counts = count_vect.fit_transform(twenty_train.data)
print ('X_train_counts.shape:', X_train_counts.shape)


tf_transformer = TfidfTransformer(use_idf =True).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
###print 'X_train_tf.shape', X_train_tf.shape


## one step
# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
# X_train_tfidf.shape


clf = MultinomialNB().fit(X_train_tf, twenty_train.target)


X_new_counts = count_vect.transform(twenty_test.data)
X_new_tfidf = tf_transformer.transform(X_new_counts)
###print 'X_new_tfidf:', X_new_tfidf.shape

from sklearn import metrics
predicted = clf.predict(X_new_tfidf)
print ('predicted:', predicted, dir(clf))
for file_name, category in zip( twenty_test.filenames, predicted):
    print(type(file_name), type(twenty_train.target_names[category]))
    print(file_name, "=> ", twenty_train.target_names[category])


print ('-----', clf.predict_log_proba(X_new_tfidf))

# print(metrics.classification_report(twenty_test.target,predicted,
#                                    target_names = twenty_test.target_names))
