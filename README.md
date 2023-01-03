# Repository of paper Model-Driven Verification of Data Science Pipelines Execution

This is the repository of paper presented for conference CAISE '23 edition.

## In this repository you can find:
1. **DataProcessing_PMML.use file**: This file define the Conceptual Metamodel described in section 3.1
2. **library directory**: In this directory are located the Library of Transformations described in section 3.3
3. **parser directory**: In this directory are located the parser that allow us generate the .soil files (models files for USE tool) through .pmml and .csv files.
4. **validation_example_23 directory**: In this directory are located the python pipeline described in section 4. that correspond with the replicability of project [Model data set](https://hub.knime.com/-/spaces/-/latest/~SFKjghagXCJNpEN_/), implemented on KNIME.
__4.1. **python_pipeline**: In this directory are located the replicated pipeline, "Model dataset with metanode.ipynb" correspond with the initial replication of pipeline and "Model dataset with metanode_without_bugs.ipynb" correspond with the replication pipeline after solve the bugs detected with the process of verification.
__4.2 **python_pipeline_validation**: In this directory are located the .soil files needed for verify each transformation of the pipeline and its corresponding .csv and .pmml files of corresponding input and output datasets of each transformation.

## For verificate each transformation you need:
1. **Execute USE Tool:** Open terminal and execute command: *"./use"*.
2. **Open DataProcessing_PMML.use** through USE UI Tool.
3. **Verify input_model.soil:** In terminal execute command: *"open [path of trasformation]/input_model.soil"*. Which correspond with input DataDictionary of transformation.
4. **Verify output_model.soil:** In terminal execute command: *"open [path of trasformation]/output_model.soil"*. Which correspond with output DataDictionary of transformation.
5. **Verify transformation:** In terminal execute command *"open [path of transformation]/[name of transformation].soil"*. Which correspond with the transformation.

## Example of verification:
For verify transformation "rowFilter" of pipeline you need:
1. Open terminal window as root folder and execute command: *"./use"*.
2. Open DataProcessing_PMML.use through USE UI Tool: In Hide Menu select *"File > Open Specification"* and select the DataProcessing_PMML.use file.
3. Through terminal window execute command: *"open ./validation_example_23/python_pipeline_validation/transformations/2-rowFilter/9-row_filter_init_span/input_model.soil"*.
4. Through terminal window execute command:*"open output_model.soil"* (because the tool save the last directory used).
5. Through terminal window execute command: *"open 9-row_filter_init_span.soil"*.
