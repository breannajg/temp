# Databricks notebook source
# MAGIC %md # Schema Setup
# MAGIC This notebook is provided to create the default set of schemas to use. Use the naming convention below when storing data relavent to this model.

# COMMAND ----------

# Check for latest version in this location
!pip install '/Volumes/dsa/dependencies/datascope/datascope-1.2.0-py3-none-any.whl'

# COMMAND ----------

def _make_schemas():
  '''
  Hidden function to create schemas if not exists. Hidden to keep a tidy namespace when running with %run
  '''
  from datascope.config import (
    CREDENTIALS, DELTA, DB
  )
  import os

  notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
  repo_path = os.path.dirname(os.path.dirname(notebook_path))
  model_name = repo_path.split('/')[-1]

  workspace = f'{DELTA.CATALOG.DEFAULT}.{model_name}_workspace'
  features = f'{DELTA.CATALOG.DEFAULT}.{model_name}_features'
  reference = f'{DELTA.CATALOG.DEFAULT}.{model_name}_reference'
  output = f'{DELTA.CATALOG.OUTPUT}.{model_name}_insights'

  spark.sql(f'USE CATALOG {DELTA.CATALOG.DEFAULT}')
  # Workspace is designed for non permanent, working files, that don't need to be monitored for drift
  spark.sql(f'CREATE DATABASE IF NOT EXISTS {workspace}')
  # Feature tables that change with each run. Tables here should be monitored for drift
  spark.sql(f'CREATE DATABASE IF NOT EXISTS {features}')
  # Static tables that are used in the data pipeline, and don't need to be updated.
  # These tables will automatically be migrated to test/ prod on a pull request
  spark.sql(f'CREATE DATABASE IF NOT EXISTS {reference}')
  # Tables that will be consumed by end users
  spark.sql(f'CREATE DATABASE IF NOT EXISTS {output}')
  return (workspace, features, reference, output)

WORKSPACE_SCHEMA, FEATURES_SCHEMA, REFERENCE_SCHEMA, OUTPUT_SCHEMA = _make_schemas()
