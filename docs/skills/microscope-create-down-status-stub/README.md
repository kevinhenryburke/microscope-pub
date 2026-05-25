# microscope-create-down-status-stub

## Down Status Stub Pattern

We want a way to mark a service as **Down** for appropriate handling of incidents and scheduled downtime. This use case is very often forgotten in frameworks and custom developments, with failing connections making countless futile calls to external services, jobs timing out and reporting back to end users with generic messages technical exception information.

*Microscope* handles this situation by following a very similar pattern to the *Absent Connection Stub* pattern. We allow for each method that is part of a Service that might experience downtime to have defined alongside it a method that is called whenever the the service is marked as temporarily down. 

By adding a custom setting, alternative (Down Alternate) implementations will run for *Method Iterations*. Administrators can add these via the setup menu or implementations can be written so that the setting is created programmatically when certain conditions are met. This latter option is particularly useful for LLM interactions where low safety scores might be a business reason to trigger a shutdown of the interface.

### How to use the Pattern

To prepare the pattern:
* For each related *Method Iteration* record that should have alternative processing when the service is down, set the field *Down_Service_Implementing_Class__c* with the name of a method to run when the Service is marked as Down. 
* Write the *Down_Service_Implementing_Class__c* method. This method will need to implement the input and output definitions specified by the *Method Iteration* as it will need to run in its place.
* In the *Service CMT* Record for the Service, set the field *Downable__c* to true.

When required in production, an administrator creates a **Service Runtime** referencing the Service and setting the field *mscope__String_Value__c* in this case to **Down**.

```
mscope__Environment_Setting__c svcRuntimeDown = new mscope__Environment_Setting__c();
svcRuntimeDown.Name = '<Service Name>.Status' ;
svcRuntimeDown.mscope__Property__c = 'Status' ;
svcRuntimeDown.mscope__Artefact_Name__c = '<Service Name>' ;
svcRuntimeDown.mscope__Artefact_Scope__c = 'Service' ;
svcRuntimeDown.mscope__String_Value__c = 'Down'; 
svcRuntimeDown.mscope__Return_Type__c = 'String';
insert svcRuntimeDown;
```

There is also a convenience method on the *StubUtil* class that can be used to create these records programmatically.

```
StubUtil.createDownStatusStub('Down');
```

### Use Cases

**Maintenance period / Unexpected outages** - If a service is down for maintenance or due to an unexpected outage, then processing can switch to the Down Method to prevent errors from being returned to the user until the issue is resolved. In the casae of an unexpected outage, the custom setting might be inserted manually by the admin or programmatically in the *Method Iteration*. 

**Untrustworthy Gen AI models** - If a model is producing toxic or hallucinated content, then processing can switch to the Down Method to prevent inappropriate content from being returned to the user until the issue is resolved.

**Preventing Data Loss** - If auditing is configured for errors on invocations of the Service, no data is lost during this period. The alternative implementation could also provide a bespoke mechanism to capture requests during these periods.


#### Technical Notes

The *Service Runtime* custom setting is only checked if one to the *Supports_Absent_Connection__c* or *Downable__c* is checked

The logic for Down Status Stubs is that the Service CMT *Downable__c* field determines if we need to check for Service Runtime record. If the setting indicates that Down Status Stubs should run then and the *Method Iteration* has its *Down_Service_Implementing_Class__c* field set then that method will be run instead of the real method.

Pro-tip: If you want to have some configurable text in a Down message, then reference a custom setting in the Down Method. The envionment mananger can then keep users updated by changing that text custom setting.

# About the Skill

In your AI Code Generator terminal, ask the tool to "run the instructions for the AI Code Generator in the file `skills/microscope-create-down-status-stub/SKILL.md` to set up a Down Status Stub in this code base." Be attentive to answer the resulting questions accurately.

## Documentation
This skill assists developers in configuring a Down Status Stub, allowing testing scenarios to verify fault tolerance when a Service is entirely unavailable or down.

It involves:
- Prompting for the method name and iteration of a Method Iteration.
- Asking the user whether they want help getting the specific Apex class created, the custom setting script written, or both.
- If creating the Apex class, offering to amend the Service metadata file to add the name of the newly created stub class.
- Generating an Execute Anonymous script to create the custom setting ensuring the artefact registers as "Down" via `StubUtil.createDownStatusStub()`.

## How to Test this Skill
To test this skill, you can open an AI Code Generator chat and ask it to run the skill. For example:
"Run the `microscope-create-down-status-stub` skill to set up a Down Status Stub."
Verify that the AI prompts you for the necessary information and successfully generates the expected boilerplate Apex implementation and Execute Anonymous script.
