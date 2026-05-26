---
name: microscope-create-down-status-stub
description: Create a Down Status stub configuration for a Microscope service resource. Use when a service resource should be marked unavailable through stubbed status settings.
---

# microscope-create-down-status-stub: Setup a Down Status Stub

## Core Responsibilities
Acquire your grounding and take instructions from the human user to create a Down Status setting representing an unavailable Service resource.

---

## Phase 1: Gather Information (Interactive)

### Step 1 — Knowledge Grounding
**Grounding**: Follow the grounding instructions in `skills/shared/CommonGrounding.md`.
Read the Human level documentation for this particular functionality at ./README.md

### Step 2 — Establish User Request
Prompt the user for the following required information:

- The name of a Service-side *Method Iteration* record.
- Whether they want you to help get the specific Apex class created for this scenario, the custom setting script written, or both.
- If creating the Apex class, offer to also amend the Service metadata file to add the name of the newly created stub class.

---

## Phase 2: Generate Artefacts (Autonomous)

Once you have gathered the required information, generate the artefacts:

### 1. Apex Stub Class
If requested, generate the Apex class mimicking the exact failure payloads required by the system.

### 2. Execution Script
Generate a script (e.g., in `scripts/apex/createDownStatusStub.apex`) with the following logic:
```apex
// Configure a Down Status Custom Setting
String serviceMethodName = '{ProvidedServiceMethodName}';


Boolean success = mscope.StubUtil.createDownStatusStub(serviceMethodName);
if (success) {
    System.debug('Successfully created down status stub for ' + serviceMethodName);
} else {
    System.debug('Failed to create down status stub for ' + serviceMethodName);
}


```

---

## Phase 3: Post-Generation Review (Interactive)

1. Inform the user that the script is created
2. Outline how they can run the Apex script to immediately replicate down behaviour in their org data. Offer to run it for them if this is within your allowed permissions.
