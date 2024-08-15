# Databricks notebook source
# MAGIC %md # Prepare Environments
# MAGIC This notebook is provides as a place to write custom code that needs to run when moving to a test/ produciton environment. It will run automatically when you pull request into staging or master. Some utilities are already provided in schema setup and migrate data to easily move data from DSCOE to TWM in ECW and between Catalogs in the deltalake. These are entirely optional.

# COMMAND ----------

# MAGIC %run ./schemas

# COMMAND ----------

# MAGIC %run ./migrate_data

# COMMAND ----------

# Check for latest version in this location
!pip install '/Volumes/dsa/dependencies/datascope/datascope-1.2.0-py3-none-any.whl'

# COMMAND ----------

from datascope.config import (
  DEV, TEST, PROD, ENVIRONMENT
)

# COMMAND ----------

if ENVIRONMENT == DEV:
  print('you are here')
elif ENVIRONMENT == TEST:
  # TODO
  pass
elif ENVIRONMENT == PROD:
  # TODO
  pass
