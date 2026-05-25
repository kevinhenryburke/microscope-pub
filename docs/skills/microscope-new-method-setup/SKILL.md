---
name: microscope-new-method-setup
description: Set up a new Microscope service-side configuration with Service metadata, Method Iteration metadata, Implementation metadata and artifaces, and tests. Use when introducing a brand-new service method into the Microscope architecture.
---

# microscope-new-method-setup: Setup a new Service method

## Core Responsibilities

Acquire your grounding and take instructions from the human user to setup a new Microscope Service method and implementation class with test class.

---

## Phase 1: Gather Information (Interactive)

### Step 1 — Knowledge Grounding

**Grounding**: Follow the grounding instructions in [../shared/CommonGrounding.md](../shared/CommonGrounding.md).
Read the Human level documentation for this particular functionality at ./README.md

### Step 2 — Establish User Request

Ask the user to provide the name and description of the Service and Method that they would like to setup as a Microscope Service method. Ask for the name and data type of the input parameters and the data type of the output.

### Step 3 — Establish Service Base Folder

Ask the user for the root folder in which you will create the Service-side metadata. You can suggest something that seems logical to you but allow the human user to override your suggestion.

---

## Phase 2: Generate Artefacts (Autonomous — follow rules exactly)

When you are aware of the method and folder locations, generate all artefacts following the rules below precisely.

> **Shared conventions**: Read and apply all naming, folder-structure, metadata, implementation-class, test-class, and validation rules defined in [../shared/CommonSKILL.md](../shared/CommonSKILL.md).

### Rules for Generating Service Side Artefacts

For the service side work, you must create:
1. `Service` metadata
2. `Service_Method` metadata
3. The underlying Apex Class or Flow implementation
4. `Service_Implementation` metadata linking the method to the implementation
5. A Test Class for the Apex implementation

---

## Phase 3: Post-Generation Review (Interactive)

### Clarify Service Configuration

After the artefacts have been created, inform the user the files are ready to deploy but tell them that they can instruct you to make changes to the metadata files. Tell the user to inform you if they wish to change things like the following and make the appropriate changes to the metadata files:

- if there is a Business Bundle that should be referenced in the Service metadata.
- if the method we are refactoring is a synchronous or asynchronous method call. By default assume synchronous.

---

## Self-Validation Checklist (verify before presenting output)

Run the full [../shared/SelfValidationChecklist.md](../shared/SelfValidationChecklist.md) and verify the generated artifacts align with the requested service and method configuration.
