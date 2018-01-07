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

twenty_train = datasets.load_files("bydata-train")
twenty_test = datasets.load_files("bydata-test")


print "\n".join(twenty_train.data[0].split("\n")[:3])
print twenty_train.target_names[twenty_train.target[0]]
print twenty_train.target[:10]


count_vect = CountVectorizer(stop_words="english",decode_error='ignore')
X_train_counts = count_vect.fit_transform(twenty_train.data)
print 'X_train_counts.shape:', X_train_counts.shape


tf_transformer = TfidfTransformer(use_idf = False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
print 'X_train_tf.shape', X_train_tf.shape


## one step
# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
# X_train_tfidf.shape


clf = MultinomialNB().fit(X_train_tf, twenty_train.target)

#docs_new = ['God is love','OpenGL on the GPU is fast']


X_new_counts = count_vect.transform(twenty_test.data)
X_new_tfidf = tf_transformer.transform(X_new_counts)
print 'X_new_tfidf:', X_new_tfidf.shape

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(X_new_counts, predicted):
     print("%r => %s") %(doc,twenty_train.target_names[category])
