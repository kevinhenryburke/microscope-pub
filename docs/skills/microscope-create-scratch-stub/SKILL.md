---
name: microscope-create-scratch-stub
description: Create a Scratch Stub setting, its mock class, and the script needed to activate it in Microscope. Use when you need a scratch or temporary stub implementation for service behavior.
---

# microscope-create-scratch-stub: Setup a Scratch Stub

## Core Responsibilities

Acquire your grounding and take instructions from the human user to create a Scratch Stub setting, its associated mock class, and the script to execute it.

---

## Phase 1: Gather Information (Interactive)

### Step 1 — Knowledge Grounding
**Grounding**: Follow the grounding instructions in `skills/shared/CommonGrounding.md`.
Read the Human level documentation for this particular functionality at ./README.md

### Step 2 — Establish User Request
Prompt the user for the following required information:

- The `Artefact Name` (the Invocation's DeveloperName) for the Scratch Stub. The user will understand this as the name of the Invocation call they want to create a stub for so use that when talking to the user.
- The name of the Apex class that will implement the Scratch Stub functionality.
- Whether they want you to help get the mock Apex class created, the custom setting script written, or both.

---

## Phase 2: Generate Artefacts (Autonomous)

Once you have gathered the required information, generate the artefacts:

### 1. Apex Stub Class
If requested, generate the Apex class that acts as the Scratch Stub returning the expected payload for the given context. If generating this for a unit test, ask the user if they'd like it annotated with `@IsTest`.

The generated stub class should have an implementationBody that matches the types expressed as the input and output types in the invocation, taking namespacing into account.

### 2. Execution Script
Generate a script (e.g., in `scripts/apex/createScratchStub.apex`) with the following code using `StubUtil`:
```apex 
// Setup a Scratch Stub Setting
String invocationName = '{ProvidedInvocationName}';
String stubClassName = '{ProvidedStubClassName}';

Boolean success = mscope.StubUtil.createScratchStub(invocationName, stubClassName);
if (success) {
    System.debug('Successfully created scratch stub for ' + invocationName);
} else {
    System.debug('Failed to create scratch stub for ' + invocationName);
}
```

---

## Phase 3: Post-Generation Review (Interactive)

1. Inform the user that the generated Apex class and/or scripts are ready.
2. Provide instructions for them to deploy the class and run the Apex script in their selected test or dev environment.
