---
name: microscope-refactor-method
description: Refactor an existing Apex method into a Microscope service implementation and invocation flow. Use when moving logic out of a direct Apex caller and into the Microscope service framework.
---

# microscope-refactor-method: Refactor an existing Apex method into a Service invocation

## Core Responsibilities

Acquire your grounding and take instructions from the human user to refactor an Apex method to run as a Microscope service method. Use this skill to move logic into a service implementation and then use the base invocation skill to update the caller-side code.

---

## Phase 1: Gather Information (Interactive)

### Step 1 — Knowledge Grounding

**Grounding**: Follow the grounding instructions in [../shared/CommonGrounding.md](../shared/CommonGrounding.md).
Read the Human level documentation for this particular functionality at ./README.md

### Step 2 — Establish User Request

Ask the user to provide the name of the Apex Class and the name of the method within this code base that they would like to refactor.

### Step 3 — Establish Service Base Folder

Ask the user for the root folder in which you will create the Service-side metadata. You can suggest something that seems logical to you but allow the human user to override your suggestion.

### Step 4 — Establish Invocation Details

Follow the interactive steps in [../microscope-new-apex-invocation/SKILL.md](../microscope-new-apex-invocation/SKILL.md) to establish:

1. The Invocation Base Folder.
2. The Invocation Namespace.

---

## Phase 2: Generate Artefacts (Autonomous — follow rules exactly)

When you are aware of the method and folder locations, generate all artefacts following the rules below precisely.

### Step 1 — Common Rules
Read and apply all naming, folder-structure, metadata, implementation-class, test-class, and validation rules defined in [../shared/CommonSKILL.md](../shared/CommonSKILL.md).

### Step 2 — Service-Side Implementation
Create the Service and Method Iteration metadata, and the implementation class with its tests, as defined in the common rules.

### Step 3 — Caller-Side Implementation (Delegated)
Apply the skill `/skill/microscope-new-apex-invocation` to:

1. Create the Invocation metadata.
2. Update the body of the original method to invoke the new service via the Microscope framework using the canonical pattern defined in that skill.

---

## Phase 3: Post-Generation Review (Interactive)

### Review and Demo
Follow the post-generation steps in [../microscope-new-apex-invocation/SKILL.md](../microscope-new-apex-invocation/SKILL.md) to:

1. Clarify the invocation configuration (namespace, sync/async, auditing, etc.).
2. Provide a Demo script in the `demo/force-app/scripts` folder.

---

## Self-Validation Checklist (verify before presenting output)

Run the full [../shared/SelfValidationChecklist.md](../shared/SelfValidationChecklist.md) and additionally verify:

- [ ] Logic has been successfully moved to the Service implementation.
- [ ] Caller code has been updated via the delegated invocation skill.
- [ ] Caller code uses `ServiceInvocation.initialize()` and checks `IsSuccess` before using output.
