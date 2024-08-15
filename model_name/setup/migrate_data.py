# Databricks notebook source
# MAGIC %pip install --upgrade "mlflow-skinny[databricks]"
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# Check for latest version in this location
!pip install '/Volumes/dsa/dependencies/datascope/datascope-1.2.0-py3-none-any.whl'

# COMMAND ----------

from delta.tables import DeltaTable
from datascope.config import (
  DEV, TEST, PROD, ENVIRONMENT
)
from datascope.utils.database import Database
from datascope.config.sqlConfig import SqlConfig
import os

# COMMAND ----------

notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
repo_path = os.path.dirname(os.path.dirname(notebook_path))
model_name = repo_path.split('/')[-1]

def migrate_dl_tables(
  from_catalog: str = 'dev_dsa', 
  to_catalog: str = 'test_dsa',
  tables: tuple[str] = tuple(), 
) -> None:
  '''
  Migrate tables in reference schema between environments (<model-name>_reference)

  Args:
    from_catalog (str, optional): catalog to migrate data from
    to_catalog (str, optional): catalog to migrate data to
    tables (tuple[str], optional): list of table to migrate, empty will move all tables in schemas

  '''
  # Get tables names in schema
  if not tables: # If tables is empty, get all
    tables = [row[0] for row in spark.sql(f'SHOW TABLES IN {from_catalog}.{model_name}_REFERENCE').select('tableName').collect()]
  for table in tables:
    sdf = spark.table(f'{from_catalog}.{model_name}_REFERENCE.{table}')
    new_table = f'{to_catalog}.{model_name}_REFERENCE.{table}'
    (
      DeltaTable.createOrReplace(spark) 
        .tableName(new_table) 
        .addColumns(sdf.schema) 
        .property("delta.autoOptimize.optimizeWrite", "true") 
        .property("delta.autoOptimize.autoCompact", "true") 
        .property("quality", "silver") 
        .execute()
    )
    sdf.write.mode('overwrite').saveAsTable(new_table)

def migrate_db_tables(
  tables: tuple[str], 
  sqlConfig: SqlConfig = SqlConfig()
) -> None:
  '''
  Migrate tables in reference schema between environments

  Args:
    tables (tuple[str]): list of table to migrate from DSCOE to TWM

  '''
  db = Database(sqlConfig)
  for table in tables:
    db.copy_db_table(
      from_table = f'DSCOE.{table}',
      to_table = f'TWM.{table}',
      schemas_included = True,
      backup = True
    )

def migrate_model(
  model_uri: str, 
  from_catalog: str = 'dev_dsa', 
  to_catalog: str = 'test_dsa',
):
  '''
  Move the trained model artifact to a new catalog. The artifact should be registered in the '<repo_name>_insights' schema in the output catalog
  The function will migrate the model aliases as 'prod'. You can set the alias in the GUI or with MlflowClient: https://learn.microsoft.com/en-us/azure/databricks/machine-learning/manage-model-lifecycle/#set-and-delete-aliases-on-models

  Args: 
    model_uri (str): Universal resource id of the model (name in catalog.schema (models tab))
    from_catalog (str, optional): catalog to migrate data from
    to_catalog (str, optional): catalog to migrate data to

  '''
  import mlflow
  mlflow.set_registry_uri("databricks-uc")
  client = mlflow.tracking.MlflowClient()
  model_path = f'{from_catalog}.{model_name}_insights.{model_uri}'
  src_model_version = client.get_model_version_by_alias(model_path, "prod")
  src_model_uri = f"models:/{model_path}/{src_model_version}"
  dst_model_name = f'{to_catalog}.{model_name}_insights.{model_uri}'
  copied_model_version = client.copy_model_version(src_model_uri, dst_model_name)
    

# COMMAND ----------

# Tables in ECW (DSCOE schema) that need to be moved to TWM so they can be referenced in prod
dscoe_ecw_tables = [
  # CENSUS_TRACT_REF_EX,
  # MODEL_COEFS,
  # CUSTOM_CODE_SET_TABLE,
]

if ENVIRONMENT == DEV:
  pass
elif ENVIRONMENT == TEST:
  # TODO: You decide how you name your model, but you need to alias it's version with 'prod' 
  #       Then you need to copy the name here
  migrate_model(
    model_uri = '',
    from_catalog = 'dev_dsa',
    to_catalog = 'test_dsa',
  )
  migrate_dl_tables(
    'dev_dsa','test_dsa'
  )
elif ENVIRONMENT == PROD:
  migrate_db_tables(tables=dscoe_ecw_tables)
  migrate_dl_tables(
    'test_dsa','dsa'
  )
  # TODO: You decide how you name your model, but you need to alias it's version with 'prod' 
  #       Then you need to copy the name here
  # migrate_model(
  #   model_uri = '', 
  #   from_catalog = 'test_dsa',
  #   to_catalog = 'dsa',
  # )
