# Microscope Worked Example: Creating a Simple Service

This guide walks you through the essential steps to implement an Apex service in the Microscope framework. We will build an example **Rating Service** that receives a client name and returns a rating. We will also cover how to utilize the `InvocationDetails` object to return business outcomes and handle errors robustly.

## Step 1: Define Input and Output Types

Every service requires predefined input and output types. For our simple Rating Service, we will use the Apex literal `String` for both input and output.

- **Input:** Client Name (String)
- **Output:** Output text containing the rating (String)

## Step 2: Create the Implementation Class

Next, create an Apex class that implements the `mscope.IImplementation` interface. This interface requires a single `dispatch` method.

In this class, we will evaluate the incoming `inputData`, set a `BusinessOutcome` summarizing the result, and demonstrate how to correctly raise an error if bad data is provided.

```java
global inherited sharing class Client_getRating_1_1 implements mscope.IImplementation {
    
    // Simple data structure for demonstration
    class RatingReply {
        String name;
        String rating;
    }

    static Map<String, RatingReply> RatingDB;
    
    static {
        RatingDB = new Map<String, RatingReply>();
        RatingReply ratingReply = new RatingReply();
        ratingReply.name = 'Superman'; 
        ratingReply.rating = 'Good'; 
        RatingDB.put(ratingReply.name, ratingReply);

        ratingReply = new RatingReply();
        ratingReply.name = 'Homer Simpson'; 
        ratingReply.rating = 'Poor'; 
        RatingDB.put(ratingReply.name, ratingReply);
    }

    static RatingReply queryRating(String name) {
        return RatingDB.get(name);
    }

    global Object dispatch(mscope.InvocationDetails invocationDetails, Object inputData) {
        String inputDataCast = (String) inputData;
        String returnValue;
        
        // Error Raising: Raise an error explicitly for known bad states
        if (inputDataCast == 'Bad Call') {
            // RatingSystemError must be defined as a Service_Error_Code__mdt Custom Metadata record
            mscope.ServiceError serviceError = invocationDetails.raiseError('RatingSystemError');
            invocationDetails.addErrorReference(serviceError, 'Invocation', invocationDetails.InvocationName);
            invocationDetails.addErrorReference(serviceError, 'Input', inputDataCast);
            return 'Not Relevant';
        }
        
        // Happy Path: Execute logic and set Business Outcomes
        RatingReply ratingReply = queryRating(inputDataCast);

        if (ratingReply != null) {
            if (ratingReply.rating == 'Poor') {
                invocationDetails.BusinessOutcome = 'Low-Rated Client';
            } else {
                invocationDetails.BusinessOutcome = 'High-Rated Client';
            }
            returnValue = 'Rating: ' + ratingReply.rating;
        } else {
            invocationDetails.BusinessOutcome = 'New Client';
            returnValue = 'No Rating Found';
        }
        
        return returnValue;
    }
}
```

## Step 3: Define Custom Metadata for the Service

To make this execution decoupled, create Custom Metadata Type (CMT) records in your Salesforce setup to configure the service. Do this in the following order:

### 1. Service CMT

- **Label:** Client
- **Service Name:** Client
- **Description:** Example Service for learning Microscope.

### 2. Method Iteration CMT

- **Label:** Client_getRating_1
- **Method Iteration Name:** Client_getRating_1
- **Service:** Client
- **Method:** getRating
- **Input Definition:** String
- **Output Definition:** String

### 3. Service Implementation CMT

- **Label:** Client_getRating_1_1
- **Service Implementation Name:** Client_getRating_1_1
- **Method Iteration:** Client_getRating_1
- **Implementing Class:** Client_getRating_1_1
- **Implementation Version:** 1

### 4. Service Error Code CMT
We used an error code in our Apex implementation above (`RatingSystemError`), which must exist in your org.

- **Label / Service Error Code Name:** RatingSystemError
- **State:** Rating System Error
- **Message:** Rating System Error
- **Severity:** Error
- **Error Category:** CustomServiceError

### 5. Invocation CMT
Create the Invocation configuration that callers will reference.

- **Label:** ExampleRating
- **Invocation Name:** ExampleRating
- **Invocation Call:** ExampleRating
- **Input Definition:** String
- **Output Definition:** String
- **Audit Invocation:** AuditSync
- **Service:** Client
- **Method:** getRating
- **Service Version:** 1
- **Iteration:** 1
- **Implementation Version:** 1

## Step 4: Invoke the Service and Handle Errors

With the framework configured, you can call the method and act on what `InvocationDetails` provides, such as `IsFail`, `State`, and `BusinessOutcome`.

```java
public inherited sharing class ExampleCallingCode {

    public static void callService(String inputName) {
        
        // Initialize invocation using the Invocation Call name given in CMT
        mscope.ServiceInvocation sinvRating = mscope.ServiceInvocation.initialize('ExampleRating');
        
        // Execute the invocation
        String returnedValueRating = (String) sinvRating.invokeService(inputName);
        
        // Retrieve InvocationDetails for post-execution state
        mscope.InvocationDetails invocationDetailsRating = sinvRating.getInvocationDetails();

        // 1. Error Handling
        if (invocationDetailsRating.IsFail) {
            System.debug('Service Execution Failed.');
            System.debug('State: ' + invocationDetailsRating.State);
            System.debug('Error Message: ' + invocationDetailsRating.ErrorMessage);
            return;
            // The process can then alert admins or route to a failure queue
        }

        // 2. Success and Business Outcomes
        if (invocationDetailsRating.IsSuccess) {
            System.debug('Service Returned: ' + returnedValueRating);
            System.debug('Business Outcome logic processing...');
            
            switch on invocationDetailsRating.BusinessOutcome {
                when 'High-Rated Client' {
                    System.debug('Route to Premium Services Queue.');
                }
                when 'Low-Rated Client' {
                    System.debug('Route to Risk Management Queue.');
                }
                when 'New Client' {
                    System.debug('Route to Sales Discovery Queue.');
                }
                when else {
                    System.debug('Route to Standard Support Queue.');
                }
            }
        }
    }
}
```

### Try It Out!
You can run this method in Execute Anonymous to see the outputs:
```
ExampleCallingCode.callService('Superman');      // Expects: High-Rated Client
ExampleCallingCode.callService('Homer Simpson'); // Expects: Low-Rated Client
ExampleCallingCode.callService('Unknown');       // Expects: New Client
ExampleCallingCode.callService('Bad Call');      // Expects: Failure & Error Details
```
