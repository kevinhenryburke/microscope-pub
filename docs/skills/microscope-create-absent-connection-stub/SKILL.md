---
name: microscope-create-absent-connection-stub
description: Create an Absent Connection stub for a Microscope service method, including the mock Apex class, metadata updates, and execution script. Use when a service should return stubbed behavior for an absent connection.
---

# microscope-create-absent-connection-stub: Setup an Absent Connection Stub

## Core Responsibilities
Acquire your grounding and take instructions from the human user to create an Absent Connection (Stubbed Status) Stub setting, and generating any associated mock classes or execution scripts.

---

## Phase 1: Gather Information (Interactive)

### Step 1 — Knowledge Grounding
**Grounding**: Follow the grounding instructions in `skills/shared/CommonGrounding.md`.
Read the Human level documentation for this particular functionality at ./README.md

### Step 2 — Establish User Request
Prompt the user for the following required information:
- The method name and iteration of a Method Iteration record.
- Whether they want you to help get the mock Apex class created, the custom setting script written, or both.
- If creating the mock Apex class, offer to also amend the Service metadata file to add the name of the newly created stub class.

---

## Phase 2: Generate Artefacts (Autonomous)

Once you have gathered the required information, generate the artefacts:

### 1. Apex Stub Class (If Required)
If requested, generate the Apex class that will act as the mock implementation for the disconnected resource, returning payload shapes expected by the caller.

### 2. Service Metadata
The Service's *Supports_Absent_Connection__c* field needs to be checked. Update the metadata file to reflect this.

### 3. Method Iteration Metadata
The Method Iteration field *Method_Alternate* needs to be populated with the name of the Apex class that will run when the Service's *Supports_Absent_Connection__c* is checked. Update the metadata file to reflect this.

### 4. Execution Script
Generate a script (e.g., in `scripts/apex/createAbsentConnectionStub.apex`) with the following logic:
```apex
// Configure an Absent Connection Stub Status Custom Setting
String serviceMethodName = '{ProvidedServiceMethodName}';

mscope.StubUtil.createAbsentConnectionStub(serviceMethodName);
```

---

## Phase 3: Post-Generation Review (Interactive)
1. Inform the user that the generation is complete.
2. Provide instructions for them to run the created Apex script and review the configured metadata.
3. Outline where the newly created Apex stub classes have been stored.
