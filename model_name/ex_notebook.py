# Databricks notebook source
# Check for latest version in this location
!pip install '/Volumes/dsa/dependencies/datascope/datascope-1.2.0-py3-none-any.whl'

# COMMAND ----------

from datascope.config import (
  CREDENTIALS, DELTA, DB
)
