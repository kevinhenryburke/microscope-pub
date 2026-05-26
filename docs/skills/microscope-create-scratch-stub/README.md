# microscope-create-scratch-stub

## Scratch Stub Pattern

In Enterprise-scale development and test phases, it can be beneficial to work in partial environments. For example, a team might want to build a screen component or Flow in a Scratch or Developer Org without requiring complex integrations or large managed packages that will be part of the final solution to be present. The component can be developed and tested much more easily without full solution, and the dependencies it brings being present. 

### Early Stage Development Scenario

It might even be the case that the full solution has not even been developed at this point. The developer/architect has created an *Invocation CMT* record for the invocation but there is no implementation as yet to call or a Service to call.

The developer can create a Custom Setting Record manually in the org that references a stub class she has written. Unless there is a need to persist the stub class in the repository (for example to support unit tests), in some cases neither the Custom Setting nor the stub class are checked into the code repository, at least not as a permanent part of the repo (checking into a feature branch and deleting before merge is ok).

The Custom Setting record has the type *mscope__Environment_Setting__c* and is populated as follows for an Invocation with Developer Name *Tab_Packaging_3* and implementation class *Tab_Packaging_3_Scratch_Stub*:

```
mscope__Environment_Setting__c scratchStub = new mscope__Environment_Setting__c();
scratchStub.Name = 'Tab_Packaging_3.ScratchStub' ; // <Invocation DeveloperName>.ScratchStub
scratchStub.mscope__Property__c = 'ScratchStub' ; // hard coded
scratchStub.mscope__Artefact_Scope__c = 'Invocation' ; // hard coded
scratchStub.mscope__Return_Type__c = 'String' ; // hard coded
scratchStub.mscope__String_Value__c = 'Tab_Packaging_3_Scratch_Stub' ; // name of the stub class to run
insert scratchStub;
```

There is also a convenience method on the *StubUtil* class that can be used to create these records programmatically.

```
StubUtil.createScratchStub('Tab_Packaging_3', 'Tab_Packaging_3_Scratch_Stub');
```


*Scratch Stubs* take precedence over not just the invocation but all other stub and override patterns too. 

As an example of the flexibility this pattern can give developments, LWC Controller Methods and Invocable Methods can be implemented just as references to Invocations. Service Decoupling reduces dependencies on other artefacts and combined with the toggleable *Absent Service Implementing Class* allows developers to work in small, independent environments.

### Unit Test Scenario

Scratch Stubs help ensure consistent execution of an invocation across all environments even when the *real* invocation might be different due to environmental differences.

* The developer/architect creates the *Invocation CMT* record for the invocation which is called in their Apex code.
* The developer creates a Custom Setting Record as above to act as a Scratch Stub in the unit test setup code, and this references an implementing class to use in tests. 

These steps ensure that every run of the test will be executed the same wherever it is run.

> Some notes on this use case
> 
> * An implementing class used only in unit test scenarios should be decorated as *@IsTest*. Any such class will of course need to be checked in to the repository as it forms part of the test suite. This implementing class may also be an inner class of the test class holding the unit test, these are decisions for the developer to take on a case by case basis.
> 
> * We note that in a more complex test it is possible that we may wish to stub invocations that are not directly called by the test but are potentially some way down the call stack. Having convenience setup methods for heavily used Scratch Stubs for invocations that developers can reuse in their test methods might be beneficial. 

## About the Skill
In your AI Code Generator terminal, ask the tool to "run the instructions for the AI Code Generator in the file `skills/microscope-create-scratch-stub/SKILL.md` to set up a Scratch Stub in this code base." Be attentive to answer the resulting questions accurately.

## Documentation
This skill assists developers in configuring a Scratch Stub. Scratch Stubs are useful in early-stage development to mock features before a real implementation is available, or to guarantee consistent execution within Unit Tests. 

It involves:

- Prompting for the service method name and the intended stub class name.
- Asking the user whether they want help getting the stub Apex implementation class created, the custom setting script written, or both.
- Generating an Execute Anonymous script to create the custom setting enabling the Scratch Stub for the specific service method by calling `StubUtil.createScratchStub()`.

## How to Test this Skill
To test this skill, you can open an AI Code Generator chat and ask it to run the skill. For example:
"Run the `microscope-create-scratch-stub` skill to set up a Scratch Stub."
Verify that the AI prompts you for the necessary information and successfully generates the expected boilerplate Apex implementation and Execute Anonymous script.
