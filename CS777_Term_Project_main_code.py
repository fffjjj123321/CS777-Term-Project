import sys
import re
import numpy as np
from operator import add
from numpy import dot
from numpy.linalg import norm
from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import SQLContext

spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()

fields = [StructField('date', DateType(), False), StructField('county', StringType(), False), StructField('state', StringType(), False),
            StructField('cases', IntegerType(), False), StructField('deaths', IntegerType(), False),StructField('fips', StringType(), False),]
schema = StructType(fields)

rddList = spark.sparkContext.textFile('Covid_Data.txt')
rddListArray = rddList.map(lambda  x: x.split('\t'))
rddRow = rddListArray.map(lambda p: Row(datetime.strptime(p[0], '%Y-%m-%d'), p[1], p[2], int(p[3]), int(p[4]), (p[5])))

shemaUsInfo = spark.createDataFrame(rddRow, schema)
shemaUsInfo.createOrReplaceTempView("usInfo")

df = shemaUsInfo.groupBy("date").agg(func.sum("cases"), func.sum("deaths")).sort(shemaUsInfo["date"].asc())

df1 = df.withColumnRenamed("sum(cases)", "cases").withColumnRenamed("sum(deaths)", "deaths")
df1.repartition(1).write.json("result1.json")
df1.createOrReplaceTempView("ustotal")

df2 = spark.sql("select t1.date,t1.cases-t2.cases as caseIncrease,t1.deaths-t2.deaths as deathIncrease from ustotal t1,ustotal t2 where t1.date = date_add(t2.date,1)")
df2.sort(df2["date"].asc()).repartition(1).write.json("result2.json")

df3 = spark.sql("select date,state,sum(cases) as totalCases,sum(deaths) as totalDeaths,round(sum(deaths)/sum(cases),4) as deathRate from usInfo  where date = to_date('2022-04-18','yyyy-MM-dd') group by date,state")
df3.sort(df3["totalCases"].desc()).repartition(1).write.json("result3.json")
df3.createOrReplaceTempView("eachStateInfo")

df4 = spark.sql("select date,state,totalCases from eachStateInfo  order by totalCases desc limit 10")
df4.repartition(1).write.json("result4.json")

df5 = spark.sql("select date,state,totalDeaths from eachStateInfo  order by totalDeaths asc limit 10")
df5.repartition(1).write.json("result5.json")

df6 = spark.sql("select 1 as sign,date,'USA' as state,round(sum(totalDeaths)/sum(totalCases),4) as deathRate from eachStateInfo group by date union select 2 as sign,date,state,deathRate from eachStateInfo").cache()
df6.sort(df6["sign"].asc(), df6["deathRate"].desc()).repartition(1).write.json("result6.json")





