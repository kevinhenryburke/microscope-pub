# Self-Validation Checklist (verify before presenting output)

Before presenting the generated artefacts to the user, verify each of these:

- [ ] Service_Method `mscope__Service__c` field matches the Service metadata `label`
- [ ] Service_Implementation `mscope__Service_Method__c` field matches the Service_Method `label`
- [ ] Invocation `mscope__Service_Name__c` matches Service `label`
- [ ] Invocation `mscope__Method__c` matches Service_Method `mscope__Method__c`
- [ ] Invocation `mscope__Invocation_Call__c` (API Name) is <= 25 characters
- [ ] `mscope__Implementing_Class__c` exactly matches the implementation Apex class name
- [ ] Implementation class uses `global inherited sharing` and `implements mscope.IImplementation`
- [ ] `dispatch()` delegates to `@TestVisible private implementationBody()`
- [ ] Test class uses `mscope.InvocationDetails_Test.createEmptyInvocationDetails()` and calls `dispatch()`
- [ ] Caller code uses `ServiceInvocation.initialize()` and checks `IsSuccess` before using output
- [ ] Folder hierarchy follows `service-{Name}/method-{method}-{iter}/impl-{ver}/` pattern
- [ ] Input/Output type is consistent across Service_Method, Invocation, and implementation class
- [ ] Invocation `mscope__Input_Definition__c` matches `mscope__Input_Creation_Class__c`
- [ ] All namespace prefixed fields use `mscope__` where required
