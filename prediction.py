from pyspark.mllib.linalg import Vectors
from pyspark.ml.regression import RandomForestRegressor
from pyspark.mllib.regression import LabeledPoint
from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession	
from pyspark.ml.classification import RandomForestClassifier
from pyspark.mllib.tree import RandomForestModel
from pyspark.mllib.tree import RandomForest
from pyspark.mllib.evaluation import MulticlassMetrics


sc = SparkContext()

spark = SparkSession(sc)

testing = spark.read.csv('s3://Bucket_name/ValidationDataset.csv',header='true', inferSchema='true', sep=';')



datardd= testing.rdd.map(lambda row: LabeledPoint(row[-1], Vectors.dense(row[0:-1])))

model = RandomForestModel.load(sc,"s3://Bucket_name/randomforestmodel.model/")


predictions = model.predict(datardd.map(lambda x: x.features))


labels_and_predictions = datardd.map(lambda x: x.label).zip(predictions)

acc = labels_and_predictions.filter(lambda x: x[0] == x[1]).count() / float(datardd.count())



metrics = MulticlassMetrics(labels_and_predictions)


f1 = metrics.fMeasure()




print("Model accuracy: %.3f%%" % (acc * 100))

print("F1 Score = %s" % f1)