# -*- coding: utf8 -*-
import numpy as np
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
#from sklearn.weights_naive_bayes import MultinomialNB
from sample_weights import weights

# 获取权重
trainFilePath = "bydata-train_03"
sample_weights_array = weights(trainFilePath)
print(sample_weights_array)

# 读取文件
train = datasets.load_files("bydata-train_03")# 训练文件
test = datasets.load_files("bydata-test")# 测试文件

# print( "train target:", train.target_names[:])# target_names：类别名称
# print ("index:", train.target[:])# target：target_names：类别名称的索引

# 对文档分词，形成词汇表，然后对新文档就可以使用这个词汇表进行编码，
# 最终将会返回一个长度等于词汇表长度的向量，每个数字表示单词在文档中出现的次数
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(train.data)
# print ('X_train_counts:', X_train_counts.toarray())

## one step
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None).\
     fit(X_train_tfidf, train.target, sample_weight=np.array(sample_weights_array))# 分类器

X_new_counts = count_vect.transform(test.data)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)# 预测类型的索引
print('predicted:', predicted)

a=[]
b=[]
for file_name, category in zip(test.filenames, predicted):
     file_name = file_name.split('\\')
     a.append(file_name[1])
     b.append(train.target_names[category])
     print(("%r => %s") %(file_name[1], train.target_names[category]))

print()
print('Accuracy:', np.mean(np.array(b) == np.array(a)))
# print(clf.predict_log_proba(X_new_tfidf))
