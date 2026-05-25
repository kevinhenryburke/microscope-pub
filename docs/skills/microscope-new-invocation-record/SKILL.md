---
name: microscope-new-invocation-record
description: Create a single Invocation__mdt CMT record (Invocation.{InvocationCallName}.md-meta.xml) for a Microscope service method. Use when only the invocation metadata file is needed, without any accompanying Apex caller code.
---

# microscope-new-invocation-record: Create an Invocation CMT Record

## Core Responsibilities

Generate a single `Invocation__mdt` Custom Metadata record file for a Microscope service method, following all naming, field, and folder conventions exactly.

---

## Phase 1: Gather Information

If you are being called from another skill, all required inputs should already be known. Skip directly to Phase 2.

Otherwise gather the information in "Required Inputs" interactively:


### Step 1 — Knowledge Grounding

**Grounding**: Follow the grounding instructions in [../shared/CommonGrounding.md](../shared/CommonGrounding.md).

### Step 2 — Required Inputs

Collect the following before generating the file. Ask as a single grouped prompt if calling interactively:

| Input | Notes |
|---|---|
| `InvocationName` | The API name and label for the record. **Must be ≤ 25 characters.** |
| `InvocationCall` | The reference for the calling application. |
| `ServiceName` | Must match the `label` in the target `Service__mdt` record exactly. |
| `MethodName` | Must match `mscope__Method__c` in the target `Service_Method__mdt` record exactly. |
| `BusinessIteration` | Must match `mscope__Business_Iteration__c` on the Service_Method. Default `1.0`. |
| `ImplementationVersion` | Must match `mscope__Implementation_Version__c` on the Service_Implementation required. Leave blank if the user will always want the latest implementation version to run. Default `1.0`. |
| `InputDefinition` | Apex type string (e.g. `String`, `Map<String,Object>`). Must match Service_Method. |
| `OutputDefinition` | Apex type string. Must match Service_Method. |
| `InvocationBaseFolder` | The folder path in which to write the file. |
| `Bundle` | The bundle / package name for `mscope__Bundle__c`. |

### Step 3 — Optional Configuration

Ask the user whether any of the following differ from their defaults, and collect values only where they do:

| Field | Default |
|---|---|
| `mscope__Invocation_Mechanism__c` | `Sync` |
| `mscope__Audit_Invocation__c` | `AuditSync` |
| `mscope__Implementation_Version__c` | `1.0` (leave blank to always use latest) |
| `mscope__Invocation_Permission__c` | `xsi:nil="true"` (no custom permission) |
| `mscope__Bubble_Up_Errors__c` | `true` |
| `mscope__Use_Cache__c` | `false` |
| `mscope__External_Invocation__c` | `false` |
| `mscope__Business_Process__c` | `xsi:nil="true"` |

---

## Phase 2: Generate the Invocation CMT Record (Autonomous)

> **Shared conventions**: Apply the naming, metadata field, and cross-reference rules in [../shared/CommonSKILL.md](../shared/CommonSKILL.md).

### Rules

1. File name: `Invocation.{InvocationCallName}.md-meta.xml`
2. Place the file in `{InvocationBaseFolder}/`.
3. `<label>` must equal `{InvocationCallName}`.
4. `mscope__Invocation_Call__c` must equal `{InvocationCallName}` and **must not exceed 25 characters**.
5. `mscope__Invocation_Metadata_Type__c` = `Metadata Record`.
6. `mscope__Input_Creation_Class__c` must equal `mscope__Input_Definition__c`.
7. `mscope__Input_Definition_NS__c` and `mscope__Output_Definition_NS__c` are empty strings by default.
8. `mscope__Input_Creation_Class_NS__c` is an empty string by default.
9. Fields that take no value use `<value xsi:nil="true"/>` — never omit them.

### XML Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CustomMetadata xmlns="http://soap.sforce.com/2006/04/metadata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <label>{InvocationCallName}</label>
    <protected>false</protected>
    <values>
        <field>mscope__Invocation_Metadata_Type__c</field>
        <value xsi:type="xsd:string">Metadata Record</value>
    </values>
    <values>
        <field>mscope__Invocation_Call__c</field>
        <value xsi:type="xsd:string">{InvocationCallName}</value>
    </values>
    <values>
        <field>mscope__Allowed_Quiddity__c</field>
        <value xsi:nil="true"/>
    </values>
    <values>
        <field>mscope__Audit_Errors_Only__c</field>
        <value xsi:type="xsd:boolean">false</value>
    </values>
    <values>
        <field>mscope__Audit_Invocation__c</field>
        <value xsi:type="xsd:string">{AuditInvocation}</value>
    </values>
    <values>
        <field>mscope__Audit_Service__c</field>
        <value xsi:nil="true"/>
    </values>
    <values>
        <field>mscope__Bubble_Up_Errors__c</field>
        <value xsi:type="xsd:boolean">{BubbleUpErrors}</value>
    </values>
    <values>
        <field>mscope__Business_Iteration__c</field>
        <value xsi:type="xsd:double">{BusinessIteration}</value>
    </values>
    <values>
        <field>mscope__Description__c</field>
        <value xsi:type="xsd:string">{Description}</value>
    </values>
    <values>
        <field>mscope__Documentation_Link__c</field>
        <value xsi:nil="true"/>
    </values>
    <values>
        <field>mscope__External_Invocation__c</field>
        <value xsi:type="xsd:boolean">{ExternalInvocation}</value>
    </values>
    <values>
        <field>mscope__Input_Audit_Override_Class__c</field>
        <value xsi:nil="true"/>
    </values>
    <values>
        <field>mscope__Input_Creation_Class_NS__c</field>
        <value xsi:type="xsd:string"></value>
    </values>
    <values>
        <field>mscope__Input_Creation_Class__c</field>
        <value xsi:type="xsd:string">{InputDefinition}</value>
    </values>
    <values>
        <field>mscope__Input_Definition_NS__c</field>
        <value xsi:type="xsd:string"></value>
    </values>
    <values>
        <field>mscope__Input_Definition__c</field>
        <value xsi:type="xsd:string">{InputDefinition}</value>
    </values>
    <values>
        <field>mscope__Invocation_Mechanism__c</field>
        <value xsi:type="xsd:string">{InvocationMechanism}</value>
    </values>
    <values>
        <field>mscope__Invocation_Permission__c</field>
        <value xsi:nil="true"/>
    </values>
    <values>
        <field>mscope__Method__c</field>
        <value xsi:type="xsd:string">{MethodName}</value>
    </values>
    <values>
        <field>mscope__Output_Audit_Override_Class__c</field>
        <value xsi:nil="true"/>
    </values>
    <values>
        <field>mscope__Output_Definition_NS__c</field>
        <value xsi:type="xsd:string"></value>
    </values>
    <values>
        <field>mscope__Output_Definition__c</field>
        <value xsi:type="xsd:string">{OutputDefinition}</value>
    </values>
    <values>
        <field>mscope__Bundle__c</field>
        <value xsi:type="xsd:string">{Bundle}</value>
    </values>
    <values>
        <field>mscope__Service_Name__c</field>
        <value xsi:type="xsd:string">{ServiceName}</value>
    </values>
    <values>
        <field>mscope__Absent_Service_Implementing_Class__c</field>
        <value xsi:nil="true"/>
    </values>
    <values>
        <field>mscope__Implementation_Version__c</field>
        <value xsi:type="xsd:double">{ImplementationVersion}</value>
    </values>
    <values>
        <field>mscope__Use_Cache__c</field>
        <value xsi:type="xsd:boolean">{UseCache}</value>
    </values>
</CustomMetadata>
```

> If `mscope__Invocation_Permission__c` has a value, replace `xsi:nil="true"` with `xsi:type="xsd:string">{PermissionApiName}</value>`.
> If `mscope__Business_Process__c` has a value, add the `<values>` block immediately after `mscope__Bundle__c`.
> If `mscope__Implementation_Version__c` is left blank (always use latest), omit the field block entirely.

---

## Phase 3: Handoff

Return the following to the calling skill or present to the user:

- The path of the created file.
- The `InvocationCallName` that was used.
- Any fields that differ from their defaults (for the calling skill or user to verify).

---

## Self-Validation Checklist (verify before presenting output)

- [ ] Record name is ≤ 25 characters
- [ ] `mscope__Invocation_Call__c` is ≤ 25 characters
- [ ] `mscope__Service_Name__c` matches the Service metadata `label` exactly
- [ ] `mscope__Method__c` matches `mscope__Method__c` on the Service_Method record exactly
- [ ] `mscope__Input_Definition__c` matches `mscope__Input_Creation_Class__c`
- [ ] `mscope__Input_Definition__c` and `mscope__Output_Definition__c` match the Service_Method record
- [ ] All nil fields use `<value xsi:nil="true"/>` — none are omitted
- [ ] All namespace-prefixed fields use `mscope__`
- [ ] File is placed in the correct `{InvocationBaseFolder}/`
