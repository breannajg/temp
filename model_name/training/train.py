# Databricks notebook source
# MAGIC %md # Setup

# COMMAND ----------

# Check for latest version in this location
!pip install '/Volumes/dsa/dependencies/datascope/datascope-1.2.0-py3-none-any.whl'

# COMMAND ----------

# MAGIC %md ## Imports

# COMMAND ----------

from datascope.config import (
  CREDENTIALS, DELTA, DB
)

# COMMAND ----------

# MAGIC %md ## Schema Setup

# COMMAND ----------

spark.sql(f'USE CATALOG {DELTA.CATALOG.DEFAULT}')

# COMMAND ----------

# MAGIC %md # Model Training

# COMMAND ----------

# TODO: Build a model
