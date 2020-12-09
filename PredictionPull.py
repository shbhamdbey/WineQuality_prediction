#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pyspark.mllib.linalg import Vectors
from pyspark.ml.regression import RandomForestRegressor
from pyspark.mllib.regression import LabeledPoint
from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession	
from pyspark.ml.classification import RandomForestClassifier
from pyspark.mllib.tree import RandomForestModel
from pyspark.mllib.tree import RandomForest
from pyspark.mllib.evaluation import MulticlassMetrics
#import numpy as np
#from sklearn.metrics import f1_score


# In[ ]:

sc = SparkContext()
spark = SparkSession(sc)


# In[ ]:

model = RandomForestModel.load(sc,"randomforestmodel.model/")



# In[ ]:


training = spark.read.csv('/file/*.csv',header='true', inferSchema='true', sep=';')


# In[ ]:


data= training.rdd.map(lambda row: LabeledPoint(row[-1], Vectors.dense(row[0:-1])))


# In[ ]:


predictions = model.predict(data.map(lambda x: x.features))


# In[ ]:


labels_and_predictions = data.map(lambda x: x.label).zip(predictions)

accu = labels_and_predictions.filter(lambda x: x[0] == x[1]).count() / float(data.count())


# In[ ]:


#import pandas as pd



# In[ ]:


#ConvertedDf = labels_and_predictions.toDF()
#df_new = ConvertedDf.toPandas()
#df_new.columns = ["label", "prediction"]


# In[ ]:


#label_new = df_new[['label']].to_numpy()
#prediction_new = df_new[['prediction']].to_numpy() 


# In[ ]:


#f1 = f1_score(label_new, prediction_new , average='micro')


# In[ ]:


#print("F1 Score = %s" % f1)


# In[ ]:
metrics = MulticlassMetrics(labels_and_predictions)

f1 = metrics.fMeasure()



print("Model accuracy: %.3f%%" % (accu * 100))

print("F1 Score = %s" % f1)




