---
name: microscope-create-absent-service-stub
description: Create an Absent Service stub framework, related Apex stub class, and activation scripts for Microscope. Use when a service needs a stubbed implementation for full service absence scenarios.
---

# microscope-create-absent-service-stub: Setup an Absent Service Stub

## Core Responsibilities
Acquire your grounding and take instructions from the human user to create an Absent Service Stub execution framework, its associated stub class, and the necessary activation scripts.

---

## Phase 1: Gather Information (Interactive)

### Step 1 — Knowledge Grounding
**Grounding**: Follow the grounding instructions in `skills/shared/CommonGrounding.md`.
Read the Human level documentation for this particular functionality at ./README.md

### Step 2 — Establish User Request
Prompt the user for the following required information:
- The `DeveloperName` of the Invocation they want to create an Absent Service Stub for.
- The name of the Apex class that will implement the Absent Service Stub.
- Whether they want you to help get the mock Apex class created, the custom setting script written, or both.
- If creating the mock Apex class, offer to also amend the Invocation metadata file to add the name of the newly created stub class.
- At which level they want to activate the stub: **org-wide**, **per Invocation Call**, or **per Invocation Name**. Explain the trade-offs: org-wide is simplest for full-scratch-org scenarios where all absent services need stubbing; per-call activates the stub for all `Invocation__mdt` records sharing that call value; per-name targets a single specific record and is the finest-grained option, preferred for unit tests.

---

## Phase 2: Generate Artefacts (Autonomous)

Once you have gathered the required information, generate the artefacts:

### 1. Apex Stub Class
If requested, generate the Apex class that acts as the Absent Service Stub. Ensure that its signature matches the expected invocation implementation, returning the appropriate shape of data.

### 2. Invocation Metadata Update
If requested, update the Invocation metadata to include the name of the newly created stub class to the `Absent_Service_Stub_Class__c` field on the `Invocation__mdt` custom metadata record.

### 3. Execution Script
Generate an Execute Anonymous Apex script to activate absent service stubs using `StubUtil`, based on the activation level chosen by the user:

**Org-wide** (e.g., `scripts/apex/enableAbsentServiceStubsInOrg.apex`):
```apex
// Enable absent service stubs for all invocations in the org
mscope.StubUtil.setPartialOrgProcessing(true);
```

**Per Invocation Name** (e.g., `scripts/apex/enableAbsentServiceStub_<InvocationName>.apex`):
```apex
// Enable absent service stub for all calls under <InvocationName>
mscope.StubUtil.createAbsentServiceStubForInvocationName('<InvocationName>');
```

**Per Invocation Call** (e.g., `scripts/apex/enableAbsentServiceStub_<InvocationCall>.apex`):
```apex
// Enable absent service stub for the specific call <InvocationCall>
mscope.StubUtil.createAbsentServiceStubForInvocationCall('<InvocationCall>');
```

---

## Phase 3: Post-Generation Review (Interactive)
1. Inform the user that the generated Apex class (if any) and script are ready.
2. Provide instructions for them to run the Execute Anonymous script in their org.
3. Crucially, instruct the user to update the `Absent_Service_Stub_Class__c` field on the `Invocation__mdt` custom metadata record referencing the newly created Apex class name.
