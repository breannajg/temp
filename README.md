# Introduction
This is a template repository for predictive models that will need to be loaded to the Predictive Analytics output table 'CBDW.CBDW_MBR_PRDCT_INSIGHTS'
It provides template notebooks for using user credentials the same way as the batch account, and has som validation code to test outputs. It also provides code to initialize schemas and migrate data when moving between dev, staging, and production.

o	This template has two important yml files (and I’m currently on the update_datascope_version branch)
o	databricks.yml, which can control what jobs are configured, and its behavior can changed based on the target (databricks bundle -t <target> …)
o	.azuredevops/azure-pipelines.yml, which calls the bundle from azure devops using the databricks cli (it calls it with different ‘targets’ if it is a pr to staging vs release)
o	Authentication is set in this library variable group: Library - Pipelines (azure.com) 
o	The following are notable items in the template repo
    	/model_name/inference/score template
      •	 Shell of scoring code that defines constants, credentials to be used in the pipeline
      •	Unit tests at the end that make sure the table could be loaded to the CBDW_MBR_PRDCT_MODEL table
    	/dscoe-config.json
      •	A template of model and output descriptions that can be used to update the USRCTL tables that control the CBDW_MBR_PRDCT_INSIGHTS table
    	/model_name /ex_notebook
      • Minimalist notebook that defines and describe constants variables.
    	/model_name /setup/migrate_data
      •	Notebook that could be called in the CI/CD pipeline to copy tables/ artifacts between dl catalogs or schemas in ECW.
    	/model_name /setup/prepare_enviroments
      •	Placeholder for code the developer might want to run during migration, that could be called by a ci/cd pipeline.
    	/model_name /setup/schemas
      •	Notebook that creates dl schemas and defines them as constants.
    	/tests/unit_tests
      •	Template code for defining/calling unit tests that can be called by the ci/cd pipeline.
    	/tests/test_dummy.py
      •	Example of single test called in unit_tests
    	/training/train
      •	Placeholder for training code
      •	I didn’t yet, but I wanted to add example code for registering a model to MLflow here

•	The create new repo pipeline
  o	This actually uses a different repo: azure-pipelines.yml - Repos (branch pa_utilities) and clones the template repo with some changes
  o	 In theory, you could install cookiecutter and do the same workflow you do locally, but using variables set within Devops

