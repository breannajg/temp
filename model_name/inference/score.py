# Databricks notebook source
# MAGIC %md # Setup

# COMMAND ----------

# Check for latest version in this location
!pip install '/Volumes/dsa/dependencies/datascope/datascope-1.2.0-py3-none-any.whl'

# COMMAND ----------

# MAGIC %md ## Imports

# COMMAND ----------

from datascope.config import (
  CREDENTIALS, DB, ENVIRONMENT
)
import datascope.utils.helpers as H
from datetime import date
from pyspark.sql.types import (
  StructType, StructField, StringType, IntegerType, DateType
)
import pyspark.sql.functions as F
from datascope.utils.paModel import PaModel, Insights
import os
import json

# COMMAND ----------

# MAGIC %md ## Variables

# COMMAND ----------

dbutils.widgets.text('run_date', date.today().isoformat())
RUN_DATE = dbutils.widgets.get('run_date')

# COMMAND ----------

# MAGIC %md # Inference

# COMMAND ----------

# MAGIC %run ../setup/schemas

# COMMAND ----------

# TODO: Build a scoring pipeline based on the run date using these schemas when necessary
print(WORKSPACE_SCHEMA, FEATURES_SCHEMA, REFERENCE_SCHEMA, OUTPUT_SCHEMA, sep=', ')

# COMMAND ----------

# MAGIC %md ## Load to Output Table

# COMMAND ----------

if False: # Edit when you are ready to test the full inference pipeline
  # Edit this json in root with information about your model
  with open('../../dscoe-config.json', 'r') as f:
    model_metadata = json.load(f)['model-metadata']
  assert(model_metadata['name'] != 'TEST01') # Make sure to actually edit dscoe-config.json
  
  pa_model = PaModel.getOrCreate(model_metadata)
  model_key = pa_model.key
  notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
  repo_path = os.path.dirname(os.path.dirname(notebook_path))
  # Model Name from repository name (note, if you change the folder structure, also change this code to get the repo name)
  model_name = repo_path.split('/')[-1]

  output_schema = StructType([
    StructField("MBR_NO", StringType(), True),
    StructField("GRP_NO", StringType(), True),
    StructField("MODEL_VALUE_KEY", IntegerType(), False), # Key that maps to output set in dscoe-config.json
    StructField("MBR_PROFILE_VALUE", StringType(), True), # Value (like a probability or driver)
  ])

  sdf = spark.createDataFrame(..., schema = output_schema)

  sdf = (
    sdf
      .withColumn("MODEL_KEY", F.lit(model_key))
      .withColumn("MBR_PROFILE_DT", F.lit(date.fromisoformat(RUN_DATE)))
  )

  sdf = sdf.select(
    "MBR_NO", "GRP_NO", "MODEL_KEY", "MBR_PROFILE_DT", "MODEL_VALUE_KEY", "MBR_PROFILE_VALUE"
  )

  # This validates that the table will be able to be loaded to the database.
  insights = Insights()
  insights.validate(sdf)

  # Maintain this naming convention for downstream tests to work. Create these schemas automatically in /setup/01_schema_setup
  H.load_dl_table(
    sdf, 
    schema = f'', # TODO
    table = model_name,
    mode = 'overwrite'
  )
  dl_output_table = f'.{model_name}' # TODO
  sdf = spark.table(dl_output_table)

  insights.write(sdf, mode=ENVIRONMENT)

