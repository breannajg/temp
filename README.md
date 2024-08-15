# Introduction
This is a template repository for predictive models that will need to be loaded to the Predictive Analytics output table 'CBDW.CBDW_MBR_PRDCT_INSIGHTS'
It provides template notebooks for using user credentials the same way as the batch account, and has som validation code to test outputs. It also provides code to initialize schemas and migrate data when moving between dev, staging, and production.

# Organization
```
/template
|
├── /docs
│   ├── Peer Review.md # Template for peer reviewer
│   └── Documentation.md # Other documentation (most documentation about a use case should be in a DevOps ticket)
|
├── /model_name
│   ├── /inference # For the production pipeline
|   |   ├── score # Template notebook for final scoring code
|   |   └── write_to_insights # Short notebook to write to the insights table
│   ├── /setup # For setup initializaion scripts
|   |   ├── 01_schema_setup # Script to initialize some schemas to use
|   |   ├── 02_migrate_data # This is run as part of the deployment pipeline. It can be modified to move necessary artifacts between environments
|   |   └── prepare_environments # Single notebook that calls the other two
│   ├── /training # For model training
|   |   └── train # Template starting point for model training
|
└── ex_notebook # A starter notebook that defines credentials to use
```

# Config files
There are three primary configuration files that control deployment behaviour. If you use the template as is, you only have to fill out one: `dscoe-config.json` in the root folder

## dscoe-config.json
This file needs to be filled out with model metadata that will eventually be used as reference information for you model in the database. See the `USRCTL.CBDW_MBR_PRDCT_MODEL_REF` and `USRCTL.CBDW_MBR_PRDCT_MODEL_VAL_REF` in the databases for example fields. These control the final view `CBDW.CBDW_MBR_PRDCT_INSIGHTS`.

## databricks.yml
This controls the Job deployment and production schedule. You can build a workflow in the GUI and copy the yaml configuration into this file if you want to customize your workflow. By default, it will schedule `/inference/score` to run Thursday at 5.

```