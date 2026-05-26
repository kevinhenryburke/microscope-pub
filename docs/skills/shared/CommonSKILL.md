# Common Skill Conventions

Shared conventions, naming rules, folder structures, metadata templates, and validation checklists used by all Microscope skills.

---

## Naming Convention (MUST follow exactly)

| Artefact | File name pattern | Label value |
|---|---|---|
| Service metadata | `Service.{ServiceName}.md-meta.xml` | `{ServiceName}` |
| Service_Method metadata | `Service_Method.{ServiceName}_{method}_{businessIteration}.md-meta.xml` | `{ServiceName}_{method}_{businessIteration}` |
| Service_Implementation metadata | `Service_Implementation.{ServiceName}_{method}_{businessIteration}_{techVersion}.md-meta.xml` | `{ServiceName}_{method}_{businessIteration}_{techVersion}` |
| Implementation class | `{ServiceName}_{method}_{businessIteration}_{techVersion}.cls` | — |
| Test class | `{ServiceName}_{method}_{businessIteration}_{techVersion}_Test.cls` | — |
| Invocation metadata | `Invocation.{InvocationCallName}.md-meta.xml` (Note: `{InvocationCallName}` must be <= 25 characters) | `{InvocationCallName}` |

## Artefact name length restrictions

*Microscope* enforces some restrictions on field lengths in some of its Custom Metata Records

Service Name 4-7 characters
Service Description 10 characters minimum
Method Name 25 characters maximum
Invocation Name 25 characters maximum

## Folder Hierarchy

```
{service-base-folder}/
  service-{ServiceName}/
    Service.{ServiceName}.md-meta.xml
    method-{method}-{businessIteration}/
      Service_Method.{ServiceName}_{method}_{businessIteration}.md-meta.xml
      impl-{techVersion}/
        Service_Implementation.{ServiceName}_{method}_{businessIteration}_{techVersion}.md-meta.xml
        {ServiceName}_{method}_{businessIteration}_{techVersion}.cls
        {ServiceName}_{method}_{businessIteration}_{techVersion}.cls-meta.xml
        {ServiceName}_{method}_{businessIteration}_{techVersion}_Test.cls
        {ServiceName}_{method}_{businessIteration}_{techVersion}_Test.cls-meta.xml
```

---

## Metadata Cross-Reference Rules

These referential links **MUST** be consistent across all generated metadata:

| Parent field | Must match |
|---|---|
| `Service_Method.mscope__Service__c` | The `label` value in the Service metadata |
| `Service_Implementation.mscope__Service_Method__c` | The `label` value in the Service_Method metadata |
| `Invocation.mscope__Service_Name__c` | The `label` value in the Service metadata |
| `Invocation.mscope__Method__c` | The `mscope__Method__c` value in the Service_Method metadata |
| `Service_Implementation.mscope__Implementing_Class__c` | The exact Apex class name of the implementation class |

## Namespace Prefix Rules

- **Service, Service_Method, Service_Implementation, and Invocation metadata** fields use the `mscope__` namespace prefix (e.g. `mscope__Description__c`, `mscope__Service__c`)

---

## Rules for Service Metadata

Create a `Service.{ServiceName}.md-meta.xml` using the patterns in the provided examples. Required fields:

- `mscope__Description__c` — a meaningful description of the service
- `mscope__Downable__c` — default to `false`
- `mscope__Managed_by_Namespace__c` — default to `false`
- `mscope__Bundle__c` — ask the user or derive from context
- `mscope__Service_Permission__c` — default to `xsi:nil="true"`
- `mscope__Service_Version__c` — default to `1.0`
- `mscope__Supports_Absent_Connection__c` — default to `false`

## Rules for Service_Method Metadata

Create a `Service_Method.{ServiceName}_{method}_{businessIteration}.md-meta.xml`. Required fields include `mscope__Service__c`, `mscope__Method__c`, `mscope__Input_Definition__c`, `mscope__Output_Definition__c`, `mscope__Business_Iteration__c`, and `mscope__Description__c`. Default `mscope__Variation_Enabled__c` to `false`.

## Rules for Service_Implementation Metadata

Create a `Service_Implementation.{ServiceName}_{method}_{businessIteration}_{techVersion}.md-meta.xml`. Required fields:

- `mscope__Implementing_Class__c` — must exactly match the Apex class name
- `mscope__Implementing_Flow__c` — set to `xsi:nil="true"` (Apex-only)
- `mscope__Service_Method__c` — must match Service_Method label
- `mscope__Implementation_Version__c` — default to `1.0`

## Rules for Invocation Metadata

Create `Invocation.{InvocationCallName}.md-meta.xml` in the invocation base folder. Use the invocation examples as a reference. 

**Defaults** (unless the user specifies otherwise):

- `mscope__Invocation_Mechanism__c` = `Sync`
- `mscope__Audit_Invocation__c` = `AuditSync`
- `mscope__Invocation_Metadata_Type__c` = `Metadata Record`
- `mscope__Invocation_Call__c` = the label value (same as the metadata record name), **MUST NOT EXCEED 25 CHARACTERS**
- `mscope__Invocation_Permission__c` = `xsi:nil="true"`
- `mscope__Bubble_Up_Errors__c` = `true`
- `mscope__Use_Cache__c` = `false`
- `mscope__Implementation_Version__c` = `1.0`
- `mscope__Business_Iteration__c` = `1.0`

**Must be consistent with service-side metadata:**

- `mscope__Service_Name__c` must match Service label
- `mscope__Method__c` must match Service_Method `mscope__Method__c`
- `mscope__Input_Definition__c` must match Service_Method `mscope__Input_Definition__c`
- `mscope__Input_Creation_Class__c` must match `mscope__Input_Definition__c`
- `mscope__Output_Definition__c` must match Service_Method `mscope__Output_Definition__c`

---

## Rules for the Implementation Apex Class

The implementation class MUST follow this exact structure:

```apex
global inherited sharing class {ClassName} implements mscope.IImplementation {
 
    global Object dispatch(mscope.InvocationDetails invocationDetails, Object inputData) {
        // Cast inputData to the appropriate type (String, Map<String,Object>, etc.)
        {CastType} inputDataCast = ({CastType}) inputData;
        return implementationBody(invocationDetails, inputDataCast);
    }

    @TestVisible private {ReturnType} implementationBody(
            mscope.InvocationDetails invocationDetails, {CastType} inputDataCast) {
        // ALL business logic from the original method goes here
        // ... 
    }
}
```

### Critical Rules — DO NOT violate these

- DO NOT use `public` access modifier on implementation classes — they MUST be `global inherited sharing`
- DO NOT forget to implement `mscope.IImplementation` interface
- DO NOT put business logic in `dispatch()` — always delegate to `implementationBody()`
- The `dispatch()` signature MUST be exactly: `global Object dispatch(mscope.InvocationDetails invocationDetails, Object inputData)`
- The `implementationBody()` MUST be `@TestVisible private`

### Setting Outcomes and Raising Errors

- **Business Outcomes**: Set a concise categorizing string to `invocationDetails.BusinessOutcome` (e.g., `'Standard Client'`, `'Not Found'`) so calling processes can consume this directly via `switch on` statements.
- **Error Raising**: For known error states or unprocessable input, do not throw generic exceptions. Instead, raise a formalized error:
  ```apex
  mscope.ServiceError error = invocationDetails.raiseError('Specific_Error_Code_Recorded_In_MDT');
  invocationDetails.addErrorReference(error, 'Attribute', 'Value');
  ```


### Handling Multiple Input Arguments

If the method being refactored has multiple input arguments:

- The Service_Method `mscope__Input_Definition__c` must be `Map<String,Object>`
- The Invocation `mscope__Input_Definition__c` must be `Map<String,Object>`
- The implementation class `dispatch()` must cast `inputData` to `Map<String,Object>` and extract keys by name
- The caller-side code must construct a `Map<String,Object>` with named keys matching the original parameter names

Example of the dispatch method with multiple arguments:
```apex
global Object dispatch(mscope.InvocationDetails invocationDetails, Object inputData) {
    Map<String,Object> inputDataCast = (Map<String,Object>) inputData;
    return implementationBody(invocationDetails, inputDataCast);
}

@TestVisible private Map<String,Object> implementationBody(
        mscope.InvocationDetails invocationDetails, Map<String,Object> inputDataCast) {
    String productNumber = (String) inputDataCast.get('productNumber');
    Integer quantity = (Integer) inputDataCast.get('quantity');
    
    // original method logic here...
    
    Map<String,Object> outputMap = new Map<String,Object>();
    outputMap.put('result', 'Order Confirmed');
    return outputMap;
}
```

---

## Rules for the Test Class

Any pre-existing test classes for the Apex method being refactored should be rewritten as test classes for the new Service_Implementation class. If no test classes exist, write new ones. The test class must:

- Have the same name as the implementation class with the suffix `_Test`
- Reside in the same folder as the implementation class
- Use `mscope.InvocationDetails_Test.createEmptyInvocationDetails()` to create test InvocationDetails
- Instantiate the implementation class and call `dispatch()` directly
- Assert on `invocationDetails.IsSuccess` / `invocationDetails.IsFail`
- Assert on `invocationDetails.BusinessOutcome` for success scenarios, and `invocationDetails.ErrorCode` for failure scenarios to ensure accurate behavior representation.

Example test pattern:
```apex
@IsTest
public class {ClassName}_Test {

    @IsTest
    public static void dispatch() {
        {ClassName} impl = new {ClassName}();
        mscope.InvocationDetails invocationDetails = mscope.InvocationDetails_Test.createEmptyInvocationDetails();

        // set up test input (String or Map<String,Object>)
        {InputType} inputData = ...; 

        Test.startTest();
        impl.dispatch(invocationDetails, inputData);
        Test.stopTest();

        Assert.isTrue(invocationDetails.IsSuccess, 'Expected success');
    }
}
```

### Rules for invoking the service via code

- DO NOT skip the `invocationDetails.IsFail` or `IsSuccess` check before acting on the invocation response.
- If `invocationDetails.IsFail` is true, ALWAYS handle the failure and log `invocationDetails.State` and `invocationDetails.ErrorMessage` to understand the failure details.
- For business workflow handling (when `IsSuccess` is true), utilize `switch on invocationDetails.BusinessOutcome { ... }` to route logic correctly rather than solely relying on parsing the output data.
