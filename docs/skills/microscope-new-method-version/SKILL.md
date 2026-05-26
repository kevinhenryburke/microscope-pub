---
name: microscope-new-method-version
description: Create a new version of an existing Microscope service method by cloning the latest method artifacts and incrementing the method version. Use when revising a service method while preserving prior versions.
---

# microscope-new-method-version: Create a new version of an existing Method Iteration 

## Core Responsibilities

Acquire your grounding and take instructions from the human user to create a new version of an existing Microscope Method Iteration. This involves cloning the highest existing iteration, incrementing the method iteration number, and ensuring all references (class names, metadata) are updated accordingly.

---

## Phase 1: Gather Information (Interactive)

### Step 1 — Knowledge Grounding

**Grounding**: Follow the grounding instructions in [../shared/CommonGrounding.md](../shared/CommonGrounding.md).
Read the Human level documentation for this particular functionality at ./README.md

### Step 2 — Identify Service and Method

Ask the user to provide the name of the Service, the Method, and the Signature Version for which they want to create a new method version.

### Step 3 — Locate Existing Implementation

Search the codebase to find the existing implementations for the specified Service and Method. Use the folder structure and naming conventions defined in [../shared/CommonSKILL.md](../shared/CommonSKILL.md).

1.  Identify the highest `{businessIteration}` currently existing by looking at the `method-{method}-{businessIteration}` folders under the appropriate `service-{ServiceName}/` directory.
2.  If multiple Signature Versions exist, ask the user which one they wish to use as the base for the new version.

Do not modify or delete any previous versions of the service method or implementation.


### Step 4 — Establish New Version Number

Increment the highest existing `{businessIteration}` by `1`. For example, if the current version is `1.1`, the new version will be `1.2`. If the version is `1`, the new version will be `2`.

### Step 5 — Ask what has changed in the method signature

List out the input parameters, names, and data types for the selected previous method version. Ask the user what has changed in the method signature for the new version. 

Similarly, list out the return type and ask if this needs to change.

---

## Phase 2: Generate Artefacts (Autonomous — follow rules exactly)

When you have identified the source version and the new method Signature Version version number, generate all artefacts following the rules below precisely. 

> **Shared conventions**: Read and apply all naming, folder-structure, metadata, implementation-class, test-class, and validation rules defined in [../shared/CommonSKILL.md](../shared/CommonSKILL.md).

### Rules for Generating the New Method Version

1.  **New Folders**: Create a new `method-{method}-{newBusinessIteration}/` directory and a subfolder `impl-1/` under the appropriate `service-{ServiceName}/` directory.
2.  **Method Iteration metadata**:
    *   Clone the `Service_Method.{ServiceName}_{method}_{businessIteration}.md-meta.xml` file into the new `method-{method}-{newBusinessIteration}/` folder.
    *   Rename the file and the `<label>` to `{ServiceName}_{method}_{newBusinessIteration}`.
    *   Update `mscope__Business_Iteration__c` to the new `{newBusinessIteration}`.
    *   Update `mscope__Input_Definition__c` and `mscope__Output_Definition__c` based on the user's answers from Step 5.
3.  **Implementation Class**:
    *   Clone the `.cls` file from the previous version's implementation into the new `impl-1/` folder.
    *   Rename the class to `{ServiceName}_{method}_{newBusinessIteration}_1`.
    *   Update all internal references to the class name (e.g., in constructors or static references).
    *   **Remove all of the business logic** in the `implementationBody` method and inform the user that they will need to add the business logic back in. Return `null` or an empty object from `implementationBody`.
4.  **Test Class**:
    *   Clone the `_Test.cls` file from the previous version into the new `impl-1/` folder.
    *   Rename the class to `{ServiceName}_{method}_{newBusinessIteration}_1_Test`.
    *   Update any references to the implementation class being tested.
    *   Clear any existing test methods from this test class, leaving only the basic setup.
5.  **Service_Implementation Metadata**:
    *   Create a new `Service_Implementation.{ServiceName}_{method}_{newBusinessIteration}_1.md-meta.xml` file in the `impl-1/` folder.
    *   Update the `mscope__Implementing_Class__c` to match the new class name.
    *   Update the `mscope__Implementation_Version__c` to `1.0`.
    *   Ensure `mscope__Service_Method__c` correctly points to the new Service_Method label: `{ServiceName}_{method}_{newBusinessIteration}`.

---

## Phase 3: Post-Generation Review (Interactive)

### Verify and Deploy

Inform the user that the new method version has been created.

1.  List the new files and their locations.
2.  Remind the user to deploy the new artefacts to the Salesforce org after they have implemented the business logic in the new implementation class.

---

## Self-Validation Checklist (verify before presenting output)

Run the full [../shared/SelfValidationChecklist.md](../shared/SelfValidationChecklist.md) and additionally verify:

- [ ] The new Signature Version version is strictly incremented from the highest existing version.
- [ ] The new tech version is strictly `1.0`.
- [ ] The new `Service_Method` metadata has been created and updated correctly.
- [ ] The implementation class and test class have been correctly renamed and use the `{newBusinessIteration}`.
- [ ] The `Service_Implementation` metadata points to the new class, has the correct version number, and links to the new `Service_Method`.
- [ ] The business logic has been cleared from the implementation class, as instructed.
