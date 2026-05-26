---
name: microscope-new-implementation-version
description: Create a new version of an existing Microscope service implementation by cloning the latest implementation artifacts and incrementing the implementation version. Use when evolving an implementation without changing the service method contract.
---

# microscope-new-implementation-version: Create a new version of an existing Implementation

## Core Responsibilities

Acquire your grounding and take instructions from the human user to create a new implementation of an existing Microscope *Method Iteration*. This involves cloning the highest existing *Implementation* version, incrementing the Implementation Version, and ensuring all references (class names, metadata) are updated accordingly.

---

## Phase 1: Gather Information (Interactive)

### Step 1 — Knowledge Grounding

**Grounding**: Follow the grounding instructions in [../shared/CommonGrounding.md](../shared/CommonGrounding.md).
Read the Human level documentation for this particular functionality at ./README.md

### Step 2 — Identify Service and Method

Ask the user to provide the name of the Service and Method for which they want to create a new implementation version.

### Step 3 — Locate Existing Implementation

Search the codebase to find the existing implementations for the specified Service and Method. Use the folder structure and naming conventions defined in [../shared/CommonSKILL.md](../shared/CommonSKILL.md).

1.  Identify the highest `{techVersion}` currently existing for the `{ServiceName}_{method}_{businessIteration}` pattern.
2.  If multiple Signature Versions exist, ask the user which one they wish to version.

Do not modify or delete any previous versions of the service method or implementation.

### Step 4 — Establish New Version Number

Increment the highest existing `{techVersion}` by `1`. For example, if the current version is `1.1`, the new version will be `1.2`. If the version is `1`, the new version will be `2`.

---

## Phase 2: Generate Artefacts (Autonomous — follow rules exactly)

When you have identified the source version and the new version number, generate all artefacts following the rules below precisely.

> **Shared conventions**: Read and apply all naming, folder-structure, metadata, implementation-class, test-class, and validation rules defined in [../shared/CommonSKILL.md](../shared/CommonSKILL.md).

### Rules for Cloning the Implementation

1.  **New Folder**: Create a new folder `impl-{newTechVersion}/` under the appropriate `method-{method}-{businessIteration}/` directory.
2.  **Implementation Class**:
    *   Clone the `.cls` file from the previous version.
    *   Rename the class to `{ServiceName}_{method}_{businessIteration}_{newTechVersion}`.
    *   Update all internal references to the class name (e.g., in constructors or static references).
    *   **Keep all business logic identical** to the source version unless the user has specific change requests.
3.  **Test Class**:
    *   Clone the `_Test.cls` file from the previous version.
    *   Rename the class to `{ServiceName}_{method}_{businessIteration}_{newTechVersion}_Test`.
    *   Update any references to the implementation class being tested.
4.  **Metadata**:
    *   Create a new `Service_Implementation.{ServiceName}_{method}_{businessIteration}_{newTechVersion}.md-meta.xml` file.
    *   Update the `mscope__Implementing_Class__c` to match the new class name.
    *   Update the `mscope__Implementation_Version__c` to the new version number.
    *   Ensure `mscope__Service_Method__c` correctly points to the existing Service_Method label.

---

## Phase 3: Post-Generation Review (Interactive)

### Verify and Deploy

Inform the user that the new implementation version has been created.

1.  List the new files and their locations.
2.  Remind the user to deploy the new artefacts to the Salesforce org.
3.  Suggest running the tests for the new implementation version using the created test class.

---

## Self-Validation Checklist (verify before presenting output)

Run the full [../shared/SelfValidationChecklist.md](../shared/SelfValidationChecklist.md) and additionally verify:

- [ ] The new tech version is strictly incremented from the highest existing version.
- [ ] The implementation class and test class have been correctly renamed.
- [ ] The `Service_Implementation` metadata points to the new class and has the correct version number.
- [ ] All other code and logic is identical to the cloned version.
