---
name: microscope-refactor-invocable-action-apex
description: Refactor an Agentforce Apex invocable action into a Microscope service invocation pattern. Use when an Apex class with @InvocableMethod should be migrated into Microscope architecture.
---

# microscope-refactor-invocable-action-apex: Refactor Agentforce Apex Actions into Microscope Service Invocations

## Core Responsibilities

Acquire your grounding and take instructions from the human user to refactor an Agentforce Apex Action (an Apex class containing an `@InvocableMethod`) to run as a Microscope service method. Use this skill if someone is looking to implement an Agentforce Action in Apex and wants to follow Microscope architectural patterns.

---

## Phase 1: Gather Information (Interactive)

### Step 1 — Knowledge Grounding

**Grounding**: Follow the grounding instructions in [../shared/CommonGrounding.md](../shared/CommonGrounding.md).
Read the Human level documentation for this particular functionality at ./README.md

### Step 2 — Establish User Request

Ask the user to provide the **name or file path** of the Apex Class containing the `@InvocableMethod` that they would like to refactor. If only a name is provided, search the codebase to locate the file.

### Step 3 — Identify Invocable Method

Locate the method annotated with `@InvocableMethod` within the identified class. If multiple exist, ask the user which one to refactor.

### Step 4 — Establish Folders and Namespace

Proceed to establish the Service Base Folder, Invocation Base Folder, and Invocation Namespace by following the interactive steps defined in [../microscope-refactor-method/SKILL.md](../microscope-refactor-method/SKILL.md).

---

## Phase 2: Generate Artefacts (Autonomous — follow rules exactly)

When you are aware of the class, method, and folder locations:

1.  **Read and apply** all naming, folder-structure, metadata, implementation-class, test-class, and validation rules defined in [../shared/CommonSKILL.md](../shared/CommonSKILL.md).
2.  **Invoke Base Skill**: Apply the skill `/skill/microscope-refactor-method` to the identified `@InvocableMethod`.
3.  **Ensure Entry Point Integration**: Verify that the base skill correctly updates the body of the `@InvocableMethod` to use the `mscope.ServiceInvocation` pattern, while maintaining the `@InvocableMethod` annotation and parameter signature required for Agentforce.

---

## Phase 3: Post-Generation Review (Interactive)

### Review and Demo

Follow the post-generation steps in [../microscope-refactor-method/SKILL.md](../microscope-refactor-method/SKILL.md) to:
1. Clarify invocation configuration (namespace, sync/async, auditing, etc.).
2. Provide a Demo script in the `demo/force-app/scripts` folder.

---

## Self-Validation Checklist (verify before presenting output)

Run the full [../shared/SelfValidationChecklist.md](../shared/SelfValidationChecklist.md) and additionally verify:

- [ ] The `@InvocableMethod` is retained as the entry point for Agentforce.
- [ ] Core logic has been moved to a Microscope Service implementation.
- [ ] Caller code follows the canonical `ServiceInvocation` pattern.
