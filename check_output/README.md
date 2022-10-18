## check_output

### JSON schemas
This repository contains the "definition" of the validation output, in the form of two JSON Schema instances.
+ `error_report_schema.json` is the JSON Schema representing the **output of the _whole validation process_**, i.e. an **array of objects**, each of which represents an error and its details.
+ `single_validation_output_schema.json` is the JSON Schema representing the **output of _any single validation function_** inside the whole process, i.e. an **object** representing an error and its details.

### Validating the output of the validation
In the repository there is also a Python script to validate the output of the whole process, or of a single function, against the respective schema: `check_validation_output.py`.
This has been written with the aim of making sure that any output from the validation steps is what we expect it to be, i.e. complies with its representation as it is defined in the JSON schemas.
The script contains a function that chooses the relevant schema between the two and checks the conformity of the output of the validation - given as a parameter - with this schema. 

#### External dependencies:
+ [jsonschema](https://pypi.org/project/jsonschema/)

