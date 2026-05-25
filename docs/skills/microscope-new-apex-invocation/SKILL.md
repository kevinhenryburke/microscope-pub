---
name: microscope-new-apex-invocation
description: Set up caller-side Apex code and invocation metadata for a Microscope service method. Use when wiring calling code to invoke a Microscope service through the framework.
---

# microscope-new-apex-invocation: Setup a new Service Invocation

## Core Responsibilities

Acquire your grounding and take instructions from the human user to setup caller-side code and metadata for a Microscope Service method invocation.

---

## Phase 1: Gather Information (Interactive)

### Step 1 — Knowledge Grounding

**Grounding**: Follow the grounding instructions in [../shared/CommonGrounding.md](../shared/CommonGrounding.md).
Read the Human level documentation for this particular functionality at ./README.md

### Step 2 — Establish User Request

If you are being called from another AI Skill you may infer some of this information. If the calling skill has created the Service Side metadata for example you will have the answers to a lot of these questions.

If the user has requested a specific name for the *Invocation Call* they want to use, then use it, otherwise generate a meaningful name. 

Ask the user to provide the name of the Service, Method and iteration that they would like to invoke. Ask for any specific input parameters required by the invocation.

Ask the user if they want the invocation to always use the latest implementation of the method or a specific version.  

### Step 3 — Establish Invocation Base Folder

Ask the user to provide the path to the folder in which to create the sample caller-side code and invocation metadata. You can suggest something that seems logical to you and offer the option to agree with your suggestion by typing "Yes" or to input their own folder choice.

### Step 4 — Establish Invocation Namespace

Ask the user for the namespace to use in the `ServiceInvocation.initialize()` call in the caller-side code. This is the first argument passed to `initialize()`. Default to an empty string (`''`) if the user does not specify one, but always ask. For example, if the invocation is from the `mscope` namespace, the call would be `mscope.ServiceInvocation.initialize('mscope', '{InvocationCallName}')`.

---

## Phase 2: Generate Artefacts (Autonomous — follow rules exactly)

When you are aware of the invocation details and folder locations, generate all artefacts following the rules below precisely.

> **Shared conventions**: Read and apply all naming, folder-structure, metadata, implementation-class, test-class, and validation rules defined in [../shared/CommonSKILL.md](../shared/CommonSKILL.md).

### Step 2a — Create the Invocation CMT Record

You must now follow the rules defined in [../microscope-new-invocation-record/SKILL.md](../microscope-new-invocation-record/SKILL.md) to create the `Invocation__mdt` metadata file.

Pass through all inputs already gathered in Phase 1:
- `InvocationCallName` — use the name agreed with the user (must be ≤ 25 characters)
- `ServiceName`, `MethodName`, `BusinessIteration`
- `InputDefinition`, `OutputDefinition` — from the method signature
- `InvocationBaseFolder` — from Step 3 above
- `Bundle` — from context or ask if not yet known
- Any optional fields (audit, mechanism, permission, etc.) confirmed in Phase 1

Do not re-ask questions already answered. The invocation record skill should run fully autonomously using the gathered context.

### Rules for Updating the Original Method (Caller-Side Invocation)

Update the body of the method the user wants to refactor to invoke the new service via the Microscope framework. The caller-side code MUST follow this exact pattern:

```apex
// CANONICAL caller-side invocation pattern
public static String originalMethod(String arg1, Integer arg2) {

    // 1. Construct the input (Map for multiple args, direct type for single arg)
    Map<String,Object> inputMap = new Map<String,Object>{
        'arg1' => arg1,
        'arg2' => arg2
    };

    // 2. Initialize the ServiceInvocation using namespace and invocation call name
    mscope.ServiceInvocation sinv = mscope.ServiceInvocation.initialize('', '{InvocationCallName}');

    // 3. Invoke the service
    Object outputData = sinv.invokeService(inputMap);

    // 4. Get InvocationDetails to check outcome
    mscope.InvocationDetails invocationDetails = sinv.getInvocationDetails();

    // 5. ALWAYS check IsSuccess before using the output
    if (invocationDetails.IsSuccess) {
        Map<String,Object> outputMap = (Map<String,Object>) outputData;
        return (String) outputMap.get('result');
    } else {
        System.debug('Service invocation failed: ' + invocationDetails.ErrorMessage);
        return null;
    }
}
```

For single-argument methods where the input type is `String`:
```apex
public static String originalMethod(String input) {
    mscope.ServiceInvocation sinv = mscope.ServiceInvocation.initialize('', '{InvocationCallName}');
    Object outputData = sinv.invokeService(input);
    mscope.InvocationDetails invocationDetails = sinv.getInvocationDetails();
    
    if (invocationDetails.IsSuccess) {
        return (String) outputData;
    } else {
        System.debug('Service invocation failed: ' + invocationDetails.ErrorMessage);
        return null;
    }
}
```

---

## Phase 3: Post-Generation Review (Interactive)

### Clarify Invocation Configuration

After the artefacts have been created, inform the user the files are ready to deploy but tell them that they can instruct you to make changes to the metadata files. Tell the user to inform you if they wish to change things like the following and make the appropriate changes to the metadata files:

- the namespace of the package from which the service will be invoked.
- if there is a Business Bundle that should be referenced in the Service metadata.
- if the method we are refactoring is a synchronous or asynchronous method call. By default assume synchronous.
- if the invocation should be audited and should it be synchronous or asynchronous. By default assume synchronous.
- if there is a particular custom permission that a user needs to have against their user record to use this particular invocation. By default assume no custom permission is required.

### Provide a Demo Script

Create a sample ExecuteAnonymous Apex script to demonstrate the usage of the service in the `demo/force-app/scripts` folder. Include error handling and logging as in the examples and query Invocation Details fields to show the outcome of the invocation. Tell the user how they can run the script after deploying the code to test the invocation.

---

## Self-Validation Checklist (verify before presenting output)

Run the full [../shared/SelfValidationChecklist.md](../shared/SelfValidationChecklist.md) and additionally verify:

- [ ] Caller code uses `ServiceInvocation.initialize()` and checks `IsSuccess` before using output
