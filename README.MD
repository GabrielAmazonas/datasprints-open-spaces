
# Airflow - PySpark + S3 + EMR - Data Lake  



## Description
This project demonstrate how to process data stored in a data lake fashion, transforming it into an OLAP optimized structure by using PySpark. 

The PySpark Job runs on AWS EMR, and the Data Pipeline is orchestrated by Apache Airflow, including the whole infrastructure creation and the EMR cluster termination.

## Rationale

- Tools and Technologies:
    - Airflow: Data Pipeline organization and scheduling tool.
    Enables control and organization over script flows.
    - PySpark: Data processing framework. Enables Distributed processing of datasets
    with a easy to use interface
    - s3: Very reliable and scalable storage option.
        
- Proposed Updates:
    - For this kind of ETL Workload, either a daily or weekly update would make sense,
    based on the data structures of both data sources. 
    With the same project structure it would be possible to have updates down to the minute window,
    as long as the data arrives on s3 in that pace. (This would require tweaks on the etl.py file.)
    
- Possible Scenarios:
    - Data Increased by 100x: 
        The create_emr_cluster function can be updated to accommodate more robust EMR clusters,
         according to data processing speed needs.
    - Dashboard updated daily, by 7am, for example:
        As mentioned in the proposed updates section, the airflow dag can be updated to run on a daily scheduling fashion and the
        emr clusters can be scaled up to match data processing speed needs.
    - Database needs to be accessed by 100+ people:
        s3 data can be accessed, for example, by using Amazon Athena or Redshift Spectrum. Which both allow access control mechanisms.
        Many other tools allow s3 data fetching similarly.
- Data Model - Star Schema:
    
        

 ### Requirements:

 - Python 3.6 or greater.

 
### Running the project:
  
 -  Clone this repository
 - Edit the `dl.cfg` file with your AWS credentials and infrastructure configuration.
 `config.sh` is also available as a helper script to build your dl.cfg file
 -  `cd` into airflow-pyspark-emr
 > With Docker:

    docker build -t airflow:1 .
    docker run -i -p 8080:8080 -t airflow:1 /bin/bash 
    
 > Without Docker:
 - Create and activate a virtualenv, docs: [venv documentation](https://docs.python.org/3/library/venv.html)   , then:
 - (venv) $ pip install -r requirements.txt
 - Add AIRFLOW_HOME environment variable to ~/.bashrc, by adding the line:										

    export AIRFLOW_HOME=your_path_to/airflow-pyspark-emr/airflow_home 
    to the end of the ~/.bashrc file

 -  Run `airflow initdb`
 -  In another terminal, run `airflow scheduler`
 - In another terminal, run `airflow webserver`
 - Access Airflow UI in localhost:8080

In the UI, two DAG's should be available: 

 - songs_etl
 - terminate_emr_clusters

Turn them on and play with it.

### Main files:
 - airflow_home/plugins/spark_jobs - etl.py:
 
     - This file has the PySpark logic and usage.
 
 - airflow_home/plugins/aws_utils - emr_deployment.py:
 
    - This file has the logic to control the AWS infrastructure needed for the job to run.


## Data Lakes with PySpark, EMR and S3

### Concepts:

- Data Lake:

    A data lake is a system or repository of data stored in its natural/raw format, usually object blobs or files.
    
- Spark:

    Apache Spark is a unified analytics engine for big data processing, with built-in modules for streaming, SQL, machine learning and graph processing.

### Project:

https://www.kaggle.com/epattaro/brazils-house-of-deputies-reimbursements

Brazilian Deputies Expenses Data Pipeline
