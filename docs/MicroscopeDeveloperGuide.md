# Microscope Developer Guide

This guide covers the practical steps for developers building on the Microscope framework: creating service implementations, configuring invocations, handling I/O and errors, and testing. For architectural background see [Microscope Solution](MicroscopeSolution.md). For security configuration see [Microscope Security](MicroscopeSecurity.md).

---

## Prerequisites

- Microscope is installed. See [Installation](installation/MicroscopeInstallation.md).
- You have read the higher-level overview [Microscope Solution](MicroscopeSolution.md)
- You are familiar with Apex, Custom Metadata Types, and how to run Execute Anonymous.
- These examples cover Apex-invoked, Apex-implemented services. Flow invocation and implementation are covered in their own sections below.


---

## AI Skills

Most of the patterns in this guide can be implemented using the Microscope AI skills rather than manually. You can find links to these skills and how to download them to your developer set up in [Microscope Solution](MicroscopeSolution.md)

---

## Creating a Simple Service

### 1. Define Input and Output Types

Every service method needs typed input and output. For simple cases use Apex literals (`String`, `Integer`, etc.). For multiple parameters, create a dedicated class with named member variables and pass an instance as the single input argument.

### 2. Implement the Service Class

All Apex service implementations implement `mscope.IImplementation`, which exposes a single `dispatch` method:

```java
global inherited sharing class Client_getRating_1_1 implements mscope.IImplementation {

    global Object dispatch(mscope.InvocationDetails invocationDetails, Object inputData) {
        String inputDataCast = (String) inputData;
        return 'Rating: Good';
    }
}
```

The class replaces a method in a larger class with a single-method class. The `invocationDetails` parameter carries runtime context and is used for error reporting and business outcomes (see below).

### 3. Create the Configuration Records

Create these Custom Metadata records in order from Setup:

**Service**

- Label / Service Name: `Client`
- Description: (min 10 characters)

**Method Iteration**

- Label / Name: `Client_getRating_1` (max 25 characters)
- Service: `Client`
- Method: `getRating`
- Input Definition: `String`
- Output Definition: `String`

**Service Implementation**

- Label / Name: `Client_getRating_1_1`
- Method Iteration: `Client_getRating_1`
- Implementing Class: `Client_getRating_1_1`
- Implementation Version: `1`

**Invocation**

- Label / Name: `ExampleRating` (max 25 characters)
- Invocation Call: `ExampleRating`
- Service: `Client` / Method: `getRating` / Iteration: `1` / Implementation Version: `1`
- Input Definition: `String` / Output Definition: `String`
- Audit Invocation: `AuditSync`

### CMT Field Name Length Rules

*Microscope* enforces some restrictions on field lengths in some of its Custom Metata Records. This is so the values can be concenated to provide a meaningful implementing artifact names.


| CMT Record | Field | Rule |
|---|---|---|
| Service | Name | 4–7 characters |
| Service | Description | 10 characters minimum |
| Method Iteration | Name | 25 characters maximum |
| Invocation | Name | 25 characters maximum |

### 4. Invoke from Apex

```java
mscope.ServiceInvocation sinv = mscope.ServiceInvocation.initialize('ExampleRating');
String returnedValue = (String) sinv.invokeService('Superman');
```

If the org has a namespace you need to reference it in a 2 argument version of the method:

```java
mscope.ServiceInvocation sinv = mscope.ServiceInvocation.initialize('mscope', 'ExampleRating');
```

---

## Invocation Processing Phases

It probably helps to understand what the *Micrcoscope Framework* is doing behind the scenes with these calls.Every invocation passes through four phases. `initialize()` covers phases 1–2; `invokeService()` covers phases 3–4.

### Phase 1 — Retrieve Metadata

The framework retrieves the matching `Invocation__mdt` record using the Invocation Call value and populates `InvocationDetails` with fields including `InvocationName`, `InvocationCall`, `InvocationMechanism`, `InputDefinition`, `OutputDefinition`, and the Service/Method/Implementation references.

### Phase 2 — Validate

Configuration is checked for correctness — does the implementing class exist, does it satisfy required interfaces, etc. Key fields set:

- `ConfigurationValid` — if false, `invokeService()` will not run
- `ConfigurationHasWarning` — runnable but not ideal
- `ConfigurationState` / `ConfigurationErrorMessage` — summary of validation

### Phase 3 — Execute

The implementation's `dispatch` method runs. Fields set by the implementation:

- `State` — set to `"SUCCESS"` for success; any other value signals a processing failure. Use the error raising API rather than setting this directly (see below).
- `BusinessOutcome` — optional; a business-meaningful string the invoker can use to route processing without parsing output data (see below).
- `IsSuccess` / `IsFail` — convenience booleans derived from `State`.
- `ErrorMessage` / `ErrorCode` — populated by the error raising API.

### Phase 4 — Audit

If `Audit Invocation` is configured on the Invocation CMT record, the framework saves `InvocationDetails` plus serialized input/output to the Audit table. Retrieve `InvocationDetails` after the call:

```java
mscope.InvocationDetails invocationDetails = sinv.getInvocationDetails();
System.debug('IsSuccess: ' + invocationDetails.IsSuccess);
System.debug('State: '     + invocationDetails.State);
System.debug('ErrorMessage: ' + invocationDetails.ErrorMessage);
```

### Audit Linking Fields

- `InitiatingContextTrackingId` — links all audit records from the same execution context.
- `InvocationPositionList` — hierarchical position of this invocation within the context. First top-level call is `[1]`; an embedded child is `[1,1]`; a second top-level call is `[2]`, etc.
- `InvocationGUID` — flattening of the two fields above, delimited by `.`.

---

## Raising Errors

### Define a Service Error Code CMT Record

Create a `Service_Error_Code__mdt` record:

- **Label / Name**: e.g. `RatingSystemError`
- **State**: the value written to `InvocationDetails.State` on error
- **Message**: the value written to `InvocationDetails.ErrorMessage`
- **Severity**: `Error` (aborts processing) or `Warning` (continues with warning)
- **Error Category**: `CustomServiceError` for Apex service errors
- **Business Bundle**: the package that owns this error

Error records live alongside the implementation in each package's folder structure. All packages' error codes are visible to administrators at runtime in one place.

### Raise the Error in Code

```java
ServiceError serviceError = invocationDetails.raiseError('RatingSystemError');
invocationDetails.addErrorReference(serviceError, 'Invocation', invocationDetails.InvocationName);
invocationDetails.addErrorReference(serviceError, 'Input', inputDataCast);
```

`raiseError` sets `State`, `ErrorMessage`, and `ErrorCode` from the CMT record and adds the error to `InvocationDetails.Errors`. `addErrorReference` appends key/value context to the error message.

### Unit Test Error Raising

```java
Assert.isTrue(invocationDetails.IsFail, 'bad input should fail');
Assert.areEqual('RatingSystemError', invocationDetails.ErrorCode, 'wrong error code');
```

### Bubbling Errors from Sub-Invocations

The *Bubble Up Errors* field on the Invocation CMT controls whether errors in embedded child invocations propagate to the parent. When checked (the default for synchronous invocations), child errors are recorded on the parent. When unchecked, or for asynchronous invocations, child errors are ignored by the parent.

---

## Business Outcomes

`BusinessOutcome` is a string set by the implementation to communicate a business-meaningful result without requiring the invoker to parse output data. It is especially useful in Flow, where checking a string field is far simpler than inspecting a data structure.

Design outcomes around the decision points in the business process. Example:

```java
if (ratingReply.rating == 'Poor') {
    invocationDetails.BusinessOutcome = 'Low-Rated Client';
} else {
    invocationDetails.BusinessOutcome = 'High-Rated Client';
}
```

Callers in Apex switch on the outcome:

```java
switch on invocationDetails.BusinessOutcome {
    when 'Sensitive Client' { /* route to Sensitive Clients Team */ }
    when 'New Client'       { /* route to Sales Team */ }
    when 'Standard Client'  { /* check rating next */ }
    when else               { /* alert Admin */ }
}
```

The `BusinessOutcome` field is also stored on the Audit record for reporting.

---

## Invoking from Apex

### By Invocation Call (recommended)

Use when multiple invocation records may exist for the same call (pilots, permission overrides, etc.):

```java
mscope.ServiceInvocation sinv = mscope.ServiceInvocation.initialize('ExampleRating');
```

Or with a namespace:

```java
mscope.ServiceInvocation sinv = mscope.ServiceInvocation.initialize(invocationNamespace, invocationCall);
```

Or via directive for full control:

```java
mscope.InvocationDirective d = new mscope.InvocationDirective();
d.invocationCall = 'ExampleRating';
mscope.ServiceInvocation sinv = mscope.ServiceInvocation.initializeFromDirective(d);
```

### By Invocation Name (direct)

Use when there are no pilots or permission overrides:

```java
mscope.InvocationDirective d = new mscope.InvocationDirective();
d.specifiedInvocationNamespace = invocationNamespace;
d.invocationName = 'ExampleRating';
mscope.ServiceInvocation sinv = mscope.ServiceInvocation.initializeFromDirective(d);
```

For the full permission-based selection algorithm see [Invocation Permission Selection](InvocationPermissionSelection.md).

---

## Input and Output

### Apex to Apex

Prefer typed Apex classes over `Map<String, Object>`. Use interfaces at strict package boundaries; use concrete classes for services that never cross package boundaries or are used in Flows.

| Context | Recommendation |
|---|---|
| Apex to Apex, same package | Apex class |
| Apex to Apex, cross-package | Apex interface |
| Single value | Apex literal (`String`, etc.) |
| Standard SObject (standard fields only) | SObject is safe |
| Apex to Flow / OmniStudio | `Map<String, Object>` with Map Validation |

### Map Input/Output Validation

For `Map<String, Object>` I/O, attach a `IMultiArgMap` implementation to the Method Iteration CMT to validate that all expected keys are present at runtime. Set `Check Map Input Field Validity` on the Invocation CMT to enable input checking; output checking is mandatory for Flow implementations.

- The forbidden key `invocationDetails` must not appear in any map validation keyset — it raises `MULTI_ARG_MAP_FORBIDDEN_KEY`.
- Scratch Stubs and Pilots are subject to the same map validation checks.

---

## Invoking from Flow

Microscope provides **Standard Invocation Actions** in the *Microscope Actions* category in Flow Builder. Each action handles a specific input/output type pair (e.g. `ActionStringString`, `ActionSObjectSObject`).

An Invocation Action:
- Takes an `InvocationName` String plus typed business input as `@InvocableVariable` parameters.
- Returns `InvocationDetails` plus typed business output.

The flow uses `InvocationDetails.State` and `InvocationDetails.BusinessOutcome` in Decision gates to route processing. Exceptions are always caught by the framework — there is no Fault path from Invocation Actions. The Decision gate's first outcome should always check `State != "SUCCESS"` to handle all processing errors.

The list of Standard Invocation Actions is in [serviceBase/force-app/Framework/classes/flow/actions/reusable/](../serviceBase/force-app/Framework/classes/flow/actions/reusable/).

If a bespoke input/output type is required, create a new Invocation Action class following the same pattern (inner `InputFromFlow` / `OutputToFlow` classes, `@InvocableMethod` execute method).

**Versioning**: provided the input/output signature of the Apex Action does not change, the Flow does not need updating when the underlying service implementation changes — only the Invocation CMT metadata record needs to point to the new version.

---

## Implementing a Service with a Flow

Set the Service Implementation CMT record to:
- `Implementation Type` = `Flow`
- `Implementing Flow` = the API name of the Autolaunched Flow

### Input

Flow expects `Map<String, Object>` input. The Invocation CMT `Input Definition` should be `Map<String,Object>`. Use Map Input Validation on the Method Iteration to enforce expected keys.

### Output

Flow output must be retrieved by name. Set `Output_Map_Data_Validation_Class` on the Method Iteration (mandatory for Flow implementations) — Microscope iterates the keyset to collect output variables and returns them as a `Map<String, Object>`.

### Invocation Details in the Flow

Add a flow variable:
- API Name: `invocationDetails` / Type: Apex-Defined / Apex Class: `mscope__InvocationDetails` / Available for input: checked

At the end of the flow, add the *Microscope: Flow Update Invocation* action and map `invocationDetails` to it. This action also accepts `businessOutcome`, `errorCode`, and `errorReferences` (a collection of `mscope__ServiceErrorReference`).

### Concurrent Flow Versions

Flows only allow one active version. To support concurrent service versions, version the flow as a new flow (new API name) rather than a new flow version, and update the Service Implementation CMT record.

---

## Service and Method Static Parameters

Use `Service_Method_Static__mdt` records to store configuration values that should not be hardcoded — remote URLs, timeout values, per-environment credentials, etc.

**Golden rule**: CMT records are the same across all environments. When a value must differ between environments, set `Parameter Value` as the default and set `Custom Setting` to the name of an `Environment_Setting__c` record whose value overrides it in that environment. Environment Managers are responsible for ensuring Custom Setting records are present in each environment that needs them.

### Setting Up a Parameter

| Field | Purpose |
|---|---|
| Parameter Name | Key used in code to retrieve the value |
| Level | `Service` (shared across all methods) or `Method` (specific to one Method Iteration) |
| Service / Business Method | Lookup to the relevant CMT, depending on Level |
| Parameter Value | Default value, used in all environments unless overridden |
| Custom Setting | Name of `Environment_Setting__c` record that overrides the default in specific environments |
| Value from Invocation | If checked, allows the invoking code to pass this parameter value directly |

Passing values via invocation is supported but not preferred — use input data for service behavioural parameters where possible.

### Reading a Parameter in an Implementation

```java
String paramValue = invocationDetails.getStaticParameter('paramName');
```

If the parameter name is not configured, a `UNKNOWN_PARAMETER_REQUESTED` warning is recorded on the invocation.

### Passing a Parameter from Invoking Code

```java
mscope.ServiceInvocation sinv = mscope.ServiceInvocation.initialize('ExampleRating');
sinv.getInvocationDetails().addStaticParameter('paramName', 'value');
String returnedValue = (String) sinv.invokeService('Superman');
```

---

## Namespaces

### Explicit Namespaces (developer-provided)

Provide namespace explicitly for:
- Input and Output Definitions (Invocation and Method Iteration CMT)
- Input and Output Map Data Validation classes
- Platform Events used by the framework

Leave blank for standard platform artefacts or structures with no namespace.

### Implicit Namespaces (must match hosting package)

Processing classes and flows must share the namespace of the CMT record that references them:

| CMT Field | Must match namespace of |
|---|---|
| Invocation → Absent Service Stub Class | Invocation CMT record |
| Method Iteration → Down Method Iteration | Method Iteration CMT record |
| Method Iteration → Absent Connection Stub | Method Iteration CMT record |
| Service Implementation → Implementing Class | Service Implementation CMT record |
| Service Implementation → Implementing Flow | Service Implementation CMT record |
| Service Implementation → Variant Determining Class | Service Implementation CMT record |

The invocation side does not need to know the namespace of the service implementation.

---

## Validating Invocation Configuration

Add a unit test for each local invocation to validate its metadata setup:

```java
@IsTest
public static void ExampleRating_CheckInvocationValidation() {
    String invocationName = 'ExampleRating';
    List<mscope__Invocation_Validation__c> results =
        mscope.InvocationMetadata_Test.runInvocationValidationTest(invocationName);

    Assert.areEqual(1, results.size(), 'Invocation ' + invocationName + ' is not valid');
    Assert.areEqual('SUCCESS', results[0].Validation_State__c, 'Invocation ' + invocationName + ' is not valid');
}
```

Only test **local** invocations this way. Non-local invocations may run different code in different environments (due to stubs), so their validation should be covered by functional tests tailored to the specific case.

