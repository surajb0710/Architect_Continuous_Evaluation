# Run Exploratory mode
> python main.py

Produces:

- DeepEval scores
- Deterministic results
- Reasons
- PASS / WARNING / FAIL
- Run summary 





# Run the regression test

From the project root:
> deepeval test run tests/test_requirement_interpretation.py

You can also run the full test directory:
> deepeval test run tests

For a specific checkpoint:
> deepeval test run tests/test_requirement_interpretation.py -k REQ-001

Produces:

- Automated test cases
- Checkpoint-level test identification
- Deterministic assertions
- Semantic assertions
- Process-level pass/fail result
