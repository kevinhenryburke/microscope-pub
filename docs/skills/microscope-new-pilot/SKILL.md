---
name: microscope-new-pilot
description: Create a new pilot implementation and pilot invocation from an existing Microscope invocation, including a custom permission and new implementation version. Use when rolling out a service implementation to a limited pilot audience.
---

# microscope-new-pilot: Create a new pilot implementation from an existing Invocation

## Core Responsibilities

Acquire your grounding and take instructions from the human user to create a new pilot for an existing Microscope Service-side implementation. This involves reading an existing Invocation record, creating a new implementation version for the referenced service method, creating a Custom Permission, and creating a new pilot Invocation record.

---

## Phase 1: Gather Information (Interactive)

### Step 1 — Knowledge Grounding

**Grounding**: Follow the grounding instructions in [../shared/CommonGrounding.md](../shared/CommonGrounding.md).
Read the Human level documentation for this particular functionality at ./README.md

Read the example files in `assets/` to understand the differences between a standard Invocation and a Pilot Invocation:

- Original Invocation: `Invocation.Tab_Pilots_1.md-meta.xml`
- Pilot Invocation: `Invocation.Tab_Pilots_1_Pilot.md-meta.xml`

### Step 2 — Identify Invocation

Ask the user to provide the name of an existing Invocation record that they wish to add a pilot to. 

### Step 3 — Locate Existing Invocation and Identify Context

Search the codebase to find the existing Invocation metadata file provided by the user (e.g. `Invocation.{InvocationName}.md-meta.xml`).
Read this file to extract the existing Service (`mscope__Service_Name__c`), Method (`mscope__Method__c`), and the original `mscope__Invocation_Call__c` value.

---

## Phase 2: Create New Implementation Version (Autonomous)

### Step 4 — Run implementation version skill

You must now follow the rules defined in [../microscope-new-implementation-version/SKILL.md](../microscope-new-implementation-version/SKILL.md) to create a new implementation version of the existing service method that was referenced by the Invocation.
This includes:

- Finding the highest existing `{techVersion}` for the identified Service and Method.
- Establishing a new version number by incrementing by `1`.
- Cloning the `.cls`, `_Test.cls`, and `.md-meta.xml` artifacts and updating class names and version numbers accordingly.

---

## Phase 3: Create Pilot Artifacts (Autonomous)

### Step 5 — Create Custom Permission

Create a new Custom Permission to be used for the pilot. 

- Create a file `force-app/main/default/customPermissions/{Pilot_Name_Custom_Permission}.customPermission-meta.xml`
- Replace `{Pilot_Name_Custom_Permission}` with an appropriate name derived from the Service/Method or Invocation name.
- It should have a basic structure suitable for a Custom Permission metadata file.

### Step 6 — Create New Pilot Invocation

Create a new Invocation record based on the original Invocation, updated to point to the new Implementation Version and protected by the Custom Permission.

1. **New File**: Create a new metadata file `Invocation.{OriginalInvocationName}_Pilot.md-meta.xml` in the same directory as the original Invocation.
2. **Updates compared to original**:
   - Change `<label>` to add `_Pilot` to the end.
   - Change the `mscope__Invocation_Metadata_Type__c` field to `<value xsi:type="xsd:string">Permission Override</value>`.
   - Ensure the `mscope__Invocation_Call__c` field remains exactly the same as the original Invocation record.
   - Set the `mscope__Invocation_Permission__c` field to `<value xsi:type="xsd:string">{Pilot_Name_Custom_Permission}</value>` using the API name of the Custom Permission created in Step 5.
   - Update the `mscope__Implementation_Version__c` field to the new version number generated in Step 4.

---

## Phase 4: Post-Generation Review (Interactive)

### Verify and Deploy

Inform the user that the new pilot invocation and supporting artifacts have been created.

1. List the new files and their locations (Implementation artifacts, Custom Permission, and Pilot Invocation). Ask the user if they would like the files to be moved to other locations.
2. Remind the user to deploy the new artefacts to the Salesforce org.
3. Suggest assigning the new Custom Permission to users who should be part of the pilot.

---

## Self-Validation Checklist (verify before presenting output)

- [ ] A new implementation version was created following the standard implementation version skill.
- [ ] A Custom Permission was created in the correct folder layout.
- [ ] The new Pilot Invocation metadata file name ends with `_Pilot`.
- [ ] Pilot Invocation `<label>` ends with `_Pilot`.
- [ ] Pilot Invocation `mscope__Invocation_Metadata_Type__c` is set to `Permission Override`.
- [ ] Pilot Invocation `mscope__Invocation_Call__c` matches the original Invocation.
- [ ] Pilot Invocation `mscope__Invocation_Permission__c` references the new Custom Permission's API name.
- [ ] Pilot Invocation `mscope__Implementation_Version__c` points to the new implementation version number.
