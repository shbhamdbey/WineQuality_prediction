#creation of model using mllib 
from pyspark.mllib.linalg import Vectors
from pyspark.ml.regression import RandomForestRegressor
from pyspark.mllib.regression import LabeledPoint
from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession	
from pyspark.ml.classification import RandomForestClassifier
from pyspark.mllib.tree import RandomForest


sc = SparkContext()


spark = SparkSession(sc)


training = spark.read.csv('s3://Bucket_name/TrainingDataset.csv',header='true', inferSchema='true', sep=';')


featureColumns = [c for c in training.columns if c != 'quality']



transformed_data= training.rdd.map(lambda row: LabeledPoint(row[-1], Vectors.dense(row[0:-1])))


model = RandomForest.trainClassifier(transformed_data,numClasses=10,categoricalFeaturesInfo={}, numTrees=50, maxBins=64, maxDepth=20, seed=33)


model.save(sc,"s3://Bucket_name/randomforestmodel.model")

