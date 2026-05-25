# microscope-create-absent-connection-stub

## Absent Connection Stub Pattern

How to test in environments which are not fully configured is a key challenge for Enterprises. In these cases the org has a *full-code* deployment, but the landscape is incomplete. This might due to a missing integration or a complex service or data source that is not fully configured (think large managed package or like a RAG data source). It is also a challenge for Developers' unit tests, as Apex Unit Tests can never make callouts to external services.

Method Alternates can specify alternative processing in test environments where the real implementation cannot be used.  The *Method Alternate* is the name of an Apex class configured on the Method Iteration Metadata record. 

Adding a Custom Setting referencing the *Service* redirects processing of all invocations of the Service's methods to the alternative implementation of the method where they are provided. Note that this setting is at the *Service* level, not the *Method Iteration* level and therefore applies to all methods of the service.

### How to use the Pattern

Whenever a Service is identified that needs special treatment in any test environment it must have its  **Service CMT** record field *Supports_Absent_Connection__c* checked. This informs the framework that the Service's methods are potentially stubbable and to look for custom settings that determine if the stubs should be used.

For each related *Method Iteration* that needs alternative processing we populate the **Method Iteration CMT** record field *Method_Alternate* with the name of the method to run instead of the real method. This method will need to the same signature as the real method as it will be called in its place.

Finally we need to add a **Service Runtime** Custom Setting record to tell *Microscope* to run the alternative processing. The Custom Setting record has the type *mscope__Environment_Setting__c* and is scripted like this:

```
mscope__Environment_Setting__c svcRuntimeStubbed = new mscope__Environment_Setting__c();
svcRuntimeStubbed.Name = '<Service Name>.Status' ;
svcRuntimeStubbed.mscope__Property__c = 'Status' ;
svcRuntimeStubbed.mscope__Artefact_Name__c = '<Service Name>' ;
svcRuntimeStubbed.mscope__Artefact_Scope__c = 'Service' ;
svcRuntimeStubbed.mscope__String_Value__c = 'Absent Connection'; // in an org there is no more than one Service Runtime setting per Service and it should be set to 'Absent Connection' or 'Down'
svcRuntimeStubbed.mscope__Return_Type__c = 'String' ;
insert svcRuntimeStubbed;
```

There is also a convenience method on the *StubUtil* class that can be used to create these records programmatically.

```
StubUtil.createAbsentConnectionStub('<Service Name>');
```

An Environment Manager should be able to easily create and maintain a load script of *Service Runtime* records for each environment to signify which services are stubbed.

### Use Cases

**Missing Integrations** - Stub Methods may emulate the behaviour of the service in a simple or sophisticated way, for example the could do anything from pushing back the same response to all queries or trying to act functionally like the real integration to give a good feel for testing or user training.

**Limited data in an org or Data 360** - if users are developing in smaller orgs which may be lacking in full reference data a stub could be used as an alternative.

**Unit Tests** - Apex Unit tests can never make callouts to external services. Developers can insert a *Service Runtime Custom Setting* record to force the *Method Alternate* to be run in unit tests, even if the connection is actually available in the runtime environment.  

#### Technical Notes

* The *Service Runtime* custom setting is only checked if one to the *Supports_Absent_Connection__c* or *Downable__c* fields (the Down service equivalent, we'll see this soon) is checked. 

The logic for Absent Connection Stubs is that the Service Supports_Absent_Connection__c field determines if we need to check for Service Runtime record. If the setting indicates that the Service should run Absent Connection Stubs then if the *Method Iteration* has its *Method_Alternate* field set then that method will be run instead of the real method.

# About the Skill
In your AI Code Generator terminal, ask the tool to "run the instructions for the AI Code Generator in the file `skills/microscope-create-absent-connection-stub/SKILL.md` to set up an Absent Connection Stub in this code base." Be attentive to answer the resulting questions accurately.

## Documentation
This skill assists developers in configuring an Absent Connection Stub, primarily used to stub non-existing artefacts and external integrations in test environments.

It involves:
- Prompting for the name and iteration of a Method Iteration.
- Asking the user whether they want help getting the stub class created, the custom setting script written, or both.
- If creating the Apex class, offering to amend the Service metadata file to add the name of the newly created stub class.
- Generating an Execute Anonymous script to create the custom setting ensuring the service method is treated as an absent connection via `StubUtil.createAbsentConnectionStub()`.

## How to Test this Skill
To test this skill, you can open an AI Code Generator chat and ask it to run the skill. For example:
"Run the `microscope-create-absent-connection-stub` skill to set up an Absent Connection Stub."
Verify that the AI prompts you for the necessary information and successfully generates the expected boilerplate Apex implementation and Execute Anonymous script.
