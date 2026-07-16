# Architect.new Continuous Evaluation Framework

## 1. Framework objective

Build a DeepEval-based quality framework that evaluates Architect.new continuously throughout the complete application-building lifecycle.

The framework must evaluate:

* whether Architect understood the user’s requirement;
* whether it generated the correct application structure;
* whether agents, prompts, tools, workflows, and knowledge sources were configured correctly;
* whether generated code and UI follow the approved design;
* whether preview and correction stages work;
* whether deployment succeeds;
* whether the completed application behaves correctly for end users.

The framework does not wait until the final application is ready.

---

# 2. Core evaluation principle

```text
Architect produces a stage output
                ↓
Framework captures the output
                ↓
DeepEval performs semantic evaluation
                +
Deterministic checks validate exact behaviour
                ↓
Quality gate produces:
Pass / Warning / Fail
                ↓
Architect continues, retries, or reports a defect
```

Every stage output is treated as an evaluable artefact.

---

# 3. Complete lifecycle

```text
User describes application
        ↓
Architect interprets requirements
        ↓
Evaluation Checkpoint 1:
Requirement Interpretation
        ↓
Architect generates application structure
        ↓
Evaluation Checkpoint 2:
Application Structure
        ↓
Agents, prompts, tools, workflows, and knowledge are configured
        ↓
Evaluation Checkpoint 3:
Configuration Quality
        ↓
Code and UI are generated
        ↓
Evaluation Checkpoint 4:
Generated Implementation
        ↓
Application is previewed
        ↓
Evaluation Checkpoint 5:
Preview Quality
        ↓
Errors are detected and corrected
        ↓
Evaluation Checkpoint 6:
Correction Quality
        ↓
Application is deployed
        ↓
Evaluation Checkpoint 7:
Deployment Quality
        ↓
End users interact with the application
        ↓
Evaluation Checkpoint 8:
Final Application Behaviour
```

---

# 4. Correct framework architecture

```text
Architect.new Continuous Evaluation Framework
│
├── 1. Lifecycle Stage Capture
│   ├── Original user requirement
│   ├── Interpreted requirement
│   ├── Generated application structure
│   ├── Agent configuration
│   ├── Prompt configuration
│   ├── Tool configuration
│   ├── Workflow configuration
│   ├── Knowledge configuration
│   ├── Generated code
│   ├── Generated UI specification
│   ├── Preview result
│   ├── Detected errors
│   ├── Applied corrections
│   ├── Deployment result
│   └── Final application responses
│
├── 2. Stage Adapters
│   ├── RequirementInterpretationAdapter
│   ├── ApplicationStructureAdapter
│   ├── ConfigurationAdapter
│   ├── GeneratedImplementationAdapter
│   ├── PreviewAdapter
│   ├── CorrectionAdapter
│   ├── DeploymentAdapter
│   └── FinalApplicationAdapter
│
├── 3. Evaluation Checkpoint
│   ├── Stage name
│   ├── Original requirement
│   ├── Previous approved artefact
│   ├── Current generated artefact
│   ├── Expected behaviour
│   ├── Metric profile
│   ├── Deterministic checks
│   └── Evaluation metadata
│
├── 4. DeepEval Semantic Evaluation Engine
│   ├── Answer Relevancy
│   ├── G-Eval
│   ├── Requirement completeness
│   ├── Requirement correctness
│   ├── Constraint preservation
│   ├── Structural suitability
│   ├── Configuration quality
│   ├── Instruction quality
│   ├── Correction quality
│   ├── RAG metrics
│   ├── Tool metrics
│   └── Agentic metrics
│
├── 5. Deterministic Validation Engine
│   ├── Required component exists
│   ├── Required agent exists
│   ├── Required tool is configured
│   ├── Required knowledge source is attached
│   ├── Output schema is valid
│   ├── Code compiles
│   ├── Type checks pass
│   ├── UI elements exist
│   ├── Preview loads
│   ├── Console has no critical errors
│   ├── Deployment succeeds
│   ├── Health checks pass
│   └── Required endpoint is reachable
│
├── 6. Stage Quality Gate
│   ├── Semantic score
│   ├── Deterministic check results
│   ├── Required metric failures
│   ├── Critical technical failures
│   ├── Pass
│   ├── Warning
│   └── Fail
│
├── 7. Evaluation Results and Traceability
│   ├── Stage being evaluated
│   ├── Input artefacts
│   ├── Generated artefact
│   ├── Metric scores
│   ├── Evaluation reasons
│   ├── Deterministic failures
│   ├── Defect category
│   ├── Build or version identifier
│   └── Previous-stage comparison
│
└── 8. Regression and Release Evaluation
    ├── Stage-level regression tests
    ├── Full lifecycle evaluation
    ├── Preview versus deployed comparison
    ├── Final application regression suite
    ├── Pass-rate tracking
    ├── Critical-stage quality gates
    └── Release readiness decision
```

---

# 5. Evaluation checkpoint model

The checkpoint is the central concept of the framework.

It represents one Architect stage that must be evaluated.

```text
EvaluationCheckpoint
│
├── checkpoint_id
├── stage
├── original_requirement
├── source_artefacts
├── actual_artefact
├── expected_behaviour
├── semantic_metrics
├── deterministic_checks
├── result
└── metadata
```

Example:

```text
Stage:
Requirement Interpretation

Original requirement:
Build a customer-support agent that answers only from uploaded
policy documents and clearly states when information is unavailable.

Actual artefact:
Architect's interpreted requirement document.

Expected behaviour:
The interpretation must preserve the knowledge-grounding restriction,
missing-information behaviour, and customer-support purpose.
```

The same checkpoint structure can later evaluate application structure, configuration, generated implementation, correction, deployment, or final behaviour.

---

# 6. Stage-specific evaluations

## Checkpoint 1 — Requirement interpretation

### Inputs

* Original user requirement
* Architect’s interpreted requirement

### DeepEval checks

* Requirement completeness
* Requirement correctness
* Constraint preservation
* Unsupported assumptions
* Ambiguity handling
* Functional requirement coverage
* Non-functional requirement coverage

### Deterministic checks

* Interpreted requirement is not empty
* Required sections exist
* Explicit constraints are present
* Named integrations are preserved

---

## Checkpoint 2 — Application structure

### Inputs

* Original requirement
* Approved interpretation
* Generated application structure

### DeepEval checks

* Architecture suitability
* Requirement-to-component coverage
* Structural completeness
* Component relevance
* Unnecessary complexity
* Data-flow consistency

### Deterministic checks

* Required components exist
* Required agents exist
* Required workflow exists
* Required knowledge layer exists
* Component references are valid

---

## Checkpoint 3 — Configuration quality

### Inputs

* Approved requirement interpretation
* Approved application structure
* Agent, prompt, tool, workflow, and knowledge configurations

### DeepEval checks

* Agent role suitability
* Agent goal alignment
* Prompt instruction quality
* Responsibility separation
* Tool suitability
* Knowledge grounding quality
* Workflow consistency
* Safety and failure behaviour

### Deterministic checks

* Required tools are assigned
* Required knowledge sources are attached
* Prompt fields are not empty
* Required output schemas exist
* Agent identifiers are valid
* Workflow connections are complete

---

## Checkpoint 4 — Generated code and UI

### Inputs

* Approved structure
* Approved configuration
* Generated code
* Generated UI specification

### DeepEval checks

* Requirement coverage
* UI-to-requirement alignment
* Workflow implementation alignment
* Generated feature completeness
* Semantic consistency with approved design

### Deterministic checks

* Build succeeds
* Type checks pass
* Linting passes
* Required pages exist
* Required components exist
* Required APIs exist
* No critical dependency failures

---

## Checkpoint 5 — Preview quality

### Inputs

* Approved implementation
* Preview application
* Preview execution results

### DeepEval checks

* Preview behaviour matches the requirement
* AI responses follow configured prompts
* User workflows achieve their intended outcome
* Generated content remains consistent with the approved design

### Deterministic checks

* Preview loads
* Required routes work
* Buttons and forms work
* APIs respond successfully
* No critical browser console errors
* No critical network failures

---

## Checkpoint 6 — Correction quality

### Inputs

* Detected error
* Failed artefact
* Correction applied
* Updated artefact

### DeepEval checks

* Root-cause alignment
* Correction relevance
* Requirement preservation
* Regression risk
* Correction completeness
* Repeated ineffective correction detection

### Deterministic checks

* Original failure now passes
* No new critical checks fail
* Build remains successful
* Previous approved functionality remains available

---

## Checkpoint 7 — Deployment quality

### Inputs

* Approved preview
* Deployment logs
* Deployment result
* Deployed application

### DeepEval checks

DeepEval has a limited role here. It can compare the deployed application’s behaviour with the approved preview or expected behaviour.

### Deterministic checks

* Deployment completed
* Correct environment was used
* Deployment URL is available
* Health check passes
* Required environment variables exist
* APIs are reachable
* Deployed version matches the approved build
* Smoke tests pass

---

## Checkpoint 8 — Final application behaviour

### Inputs

* Deployed application
* Evaluation dataset
* User scenarios
* Retrieved context, tool calls, or traces when available

### DeepEval checks

* Answer relevancy
* Correctness
* Instruction following
* Completeness
* Hallucination
* Faithfulness
* Contextual precision and recall
* Tool correctness
* Task completion
* Plan adherence
* Conversation quality
* Safety

### Deterministic checks

* Required response schema
* Required number of results
* Required fields
* API response status
* UI state changes
* External action completion

---

# 7. Responsibilities of DeepEval

DeepEval is used when the question requires semantic judgement.

Examples:

```text
Did Architect preserve the user’s intent?

Does the application structure satisfy the requirement?

Are the generated agent instructions appropriate?

Did the correction solve the correct problem?

Does the deployed application answer accurately?

Did the workflow complete the intended task?
```

DeepEval should provide:

* semantic scores;
* reasons;
* evidence;
* threshold-based pass/fail;
* regression testing;
* stage-specific metric profiles.

---

# 8. Responsibilities of deterministic tools

Normal automation is used when the answer should be exact.

Examples:

```text
Does the required agent exist?

Is the knowledge base configured?

Does the generated code compile?

Does the preview page load?

Was the deployment successful?

Did the API return HTTP 200?

Was the external ticket actually created?
```

Possible tools include:

* Pytest
* Playwright
* API automation
* Static analysis
* Build tools
* Database checks
* Deployment health checks
* Security and performance tools

---

# 9. Combined quality-gate logic

A stage passes only when both semantic and deterministic requirements are satisfied.

```text
DeepEval semantic result
            +
Deterministic validation result
            ↓
Stage quality gate
```

Example:

```text
Requirement completeness: 0.92       Pass
Constraint preservation: 0.88        Pass
Unsupported assumptions: 0.84        Pass
Required KB configured:              Fail
Required tool configured:            Pass

Final stage result: Fail
```

A strong semantic score must not hide a missing technical component.

Likewise, technically valid output must not pass when it misunderstands the user requirement.

---

# 10. Defect classification

Failures should be classified by lifecycle stage.

```text
REQUIREMENT_INTERPRETATION_FAILURE
APPLICATION_STRUCTURE_FAILURE
AGENT_CONFIGURATION_FAILURE
PROMPT_CONFIGURATION_FAILURE
TOOL_CONFIGURATION_FAILURE
KNOWLEDGE_CONFIGURATION_FAILURE
GENERATED_CODE_FAILURE
GENERATED_UI_FAILURE
PREVIEW_FAILURE
CORRECTION_FAILURE
DEPLOYMENT_FAILURE
FINAL_AI_BEHAVIOUR_FAILURE
```

This makes root-cause analysis more precise than reporting every issue as a generated-application failure.

---

# 11. Version 1 scope

Version 1 should not automate every lifecycle stage immediately.

It should establish the checkpoint-based design and implement these first:

```text
1. Requirement interpretation evaluation
2. Application structure evaluation
3. Agent, prompt, tool, and knowledge configuration evaluation
4. Final application response evaluation
```

It should also define interfaces for:

```text
5. Generated implementation validation
6. Preview validation
7. Correction validation
8. Deployment validation
```

Those interfaces can initially accept manually captured or API-provided stage artefacts until direct Architect integrations are available.

---

# 12. Version 1 completion criteria

Version 1 is complete when:

1. The framework can represent different Architect lifecycle stages.
2. Each implemented stage is evaluated immediately after its artefact is generated.
3. Stage-specific DeepEval metric profiles exist.
4. Deterministic checks can be attached to a checkpoint.
5. A combined stage result is produced.
6. Failures identify the responsible lifecycle stage.
7. Regression tests can run for each implemented checkpoint.
8. Requirement interpretation, application structure, configuration, and final output are covered.
9. The framework does not require the final application to exist before earlier stages can be evaluated.
10. The setup and execution flow are documented.

---

# 13. Final agreed positioning

The framework is not merely:

```text
Architect application
        ↓
DeepEval
        ↓
Final response score
```

It is:

```text
Architect build lifecycle
        ↓
Evaluation after every meaningful stage
        ↓
DeepEval semantic checks
        +
Deterministic technical checks
        ↓
Stage-level quality gates
        ↓
Continuous Architect platform evaluation
```

The final application is one evaluation stage—not the only evaluation target.
