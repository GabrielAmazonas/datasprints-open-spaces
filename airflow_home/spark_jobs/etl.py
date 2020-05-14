import configparser
import os
import sys

from pyspark.sql import SparkSession


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_deputies_data(spark, input_data, output_data):
    deputies_data = input_data + "deputies_dataset.csv"
    df = spark.read.csv(deputies_data, header=True, inferSchema=True)

    deputies_table = df.select('deputy_id', 'deputy_name').distinct()

    deputies_table.write.mode('overwrite').parquet(output_data + 'deputies')


def check_results(spark, output_data):
    df = spark.read.parquet(output_data + 'deputies')
    df.select('deputy_id', 'deputy_name')


def main():
    if len(sys.argv) == 3:
        # aws cluster mode - Here we could read an offset Date passed by the Airflow Runtime
        input_data = sys.argv[1]
        output_data = sys.argv[2]
    else:
        # local mode
        config = configparser.ConfigParser()
        config.read('./dl.cfg')

        os.environ['AWS_ACCESS_KEY_ID'] = config['AWS']['AWS_ACCESS_KEY_ID']
        os.environ['AWS_SECRET_ACCESS_KEY'] = config['AWS']['AWS_SECRET_ACCESS_KEY']

        input_data = config['DATALAKE']['INPUT_DATA']
        output_data = config['DATALAKE']['OUTPUT_DATA']

    spark = create_spark_session()

    process_deputies_data(spark, input_data, output_data)
    check_results(spark, output_data)


if __name__ == "__main__":
    main()
