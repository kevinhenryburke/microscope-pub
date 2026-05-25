# microscope-create-absent-service-stub

## Absent Service Stub Pattern

In the documentation of [Scratch Stubs](/skills/microscope-create-scratch-stub/README.md) we talked about the benefits of working in partial environments and how to meet the needs of developers in managing the build dependencies. 

The *Scratch Stub* pattern is quick and lightweight, does not impact on metadata and is perfect for early stage development of a feature in a partial environment. But it does require the developer to create a custom setting for each invocation that references a service that is not present in the org. This can become an overhead each time a developer creates a scratch org if there are many such invocations. 

**Absent Service Stubs** are a more permanent variation of the *Scratch Stub* pattern that can be used when the *Service* that an *Invocation* references is not present in the org. This pattern uses the Invocation CMT field *Absent Service Implementing Class* to specify an alternative implementation class that can produce correctly formatted results for the calling component in these circumstances. When an invocation runs in an environment where the referenced Service CMT record is not present in the org, the *Absent Service Implementing Class* is automatically substituted as the implementation.

*Absent Service Stubs* help developers work in small environments and support Salesforce DX packaging by allowing development orgs to be created very quickly, free from the burden of full-code org dependencies.

## How it works

This pattern is based on **Service Presence** in an org which does not have the full code base. At runtime *Microscope* checks to see if the Service referenced in an *Invocation CMT record* is present in the org. 

* If the Service CMT record is present then we run that *real* implementation and the *Absent Service Implementing Class* value is ignored
* If it is not, *Microscope* will pick up the name of the Apex class stored in the field *Absent Service Implementing Class* of the *Invocation CMT Record* and run this instead. 

### How to use the Pattern

Populate an Invocation's *Absent Service Implementing Class* field with the name of an Apex Class that will should run instead of the real referenced *Method Iteration* whenever the service is not present in the org.

Then switch on the feature using an *Environment Setting* boolean record. This can be done at three levels of granularity — any enabled level independently activates stub processing for the matching invocation:

| Level | Setting name | Scope |
|---|---|---|
| **Org-wide** | `partialOrgProcessing` | All invocations in the org |
| **Invocation Call** | `<InvocationCall>.AbsentStub` | All `Invocation__mdt` records sharing that Invocation Call value |
| **Invocation Name** | `<InvocationName>.AbsentStub` | A single specific `Invocation__mdt` record (finest grain) |

Use the convenience methods on the *StubUtil* class to create these settings programmatically:

```apex
// Org-wide
StubUtil.setPartialOrgProcessing(true);

// Per Invocation Call
StubUtil.createAbsentServiceStubForInvocationCall('MyInvocationName.myCall');

// Per Invocation Name
StubUtil.createAbsentServiceStubForInvocationName('MyInvocationName');
```

For partial environments where all invocations targeting the absent service need stub processing, the org-wide setting is the simplest choice. The per-call setting activates stub processing for all `Invocation__mdt` records sharing that call value. For the finest-grained control — for example in a unit test targeting a single Invocation CMT record — prefer the per-name setting.

### Notes and Considerations

* *Absent Service Stubs* should never be set to run in production or full code test environments. Full code environments that require alternative processing should do so at the *Method Iteration* level using [Absent Connection Stubs](/skills/microscope-create-absent-connection-stub/README.md).

* The *Absent Service Implementing Class* field value is a *permanent* setting that is available in all environments but is ignored when the service is present in the org.

* Care needs to be taken to ensure a consistent testing experience across all environments. If the Service is present in a higher environment the *Absent Service Stub* custom setting will be ignored so testing outcomes might be different in partial-code and full-code orgs. For this reason [Scratch Stubs](/skills/microscope-create-scratch-stub/README.md) are the right choice for unit testing.


# About the Skill
In your AI Code Generator terminal, ask the tool to "run the instructions for the AI Code Generator in the file `skills/microscope-create-absent-service-stub/SKILL.md` to set up an Absent Service Stub in this code base." Be attentive to answer the resulting questions accurately.

## Documentation
This skill assists developers in configuring an Absent Service Stub, which is useful when developing a feature within a partial environment (like a DX unlocked package or scratch org) where some required Services might not be present.

It involves:
- Prompting for the invocation name.
- Asking the user whether they want help getting the stub Apex implementation class created, the custom setting script written, or both.
- If creating the Apex class, offering to amend the invocation metadata file to add the name of the newly created stub class.
- Asking which activation level is required — org-wide, per Invocation Name, or per Invocation Call — and generating the appropriate Execute Anonymous script using `StubUtil`.
- Instructing the user to populate the `Absent_Service_Stub_Class__c` field on the corresponding `Invocation__mdt` record.

## How to Test this Skill
To test this skill, you can open an AI Code Generator chat and ask it to run the skill. For example:
"Run the `microscope-create-absent-service-stub` skill to set up an Absent Service Stub."
Verify that the AI prompts you for the necessary information and successfully generates the expected boilerplate Apex implementation and Execute Anonymous script.
