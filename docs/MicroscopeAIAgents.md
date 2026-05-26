## Generative AI Benefits

> **Prerequisite reading**: This document covers how Microscope supports Generative AI use cases. It assumes familiarity with the core framework — the Service Model, Invocation Permissions, Stub Patterns, and Audit — all of which are described in [MicroscopeSolution.md](MicroscopeSolution.md).

This framework provides several benefits for calling Generative AI features from the core Salesforce platform.

### Gen AI Testing and Delivery

The architecture can help test generative AI processes within the Enterprise. 

#### Grounding for Testing

Prompt Templates are often grounded with data from the org, from *Data 360* or connected external systems, but in development and test orgs that data may not be available or rich enough to support realistic testing. Prompt quality may therefore be hard to evaluate. If the org does not have the data required for the retrieval part of a process, production-like data can be provided by an alternate implementation. 

The diagram below illustrates an implementation of a grounding retrieval for a Prompt Template which has a stub option (a [*Scratch Stub*](MicroscopeSolution.md#scratch-stubs) or [*Absent Service Stub*](MicroscopeSolution.md#absent-service-stubs)). The stub can be used to provide production-like grounding in partial code and partial data development and testing contexts.

![Production Data Grounding and LLM Processing](images/media/ProductionDataGroundingandLLMProcessing.png)


#### Deterministic Responses for Testing

The non-deterministic nature of LLMs also makes business processes harder to validate because traditional "expected vs actual" pattern-matching is no longer sufficient. Sometimes teams want to test the process, not the LLM response. If **deterministic output** is needed for business-process testing, an alternate implementation can replace the variable LLM response by use of an [*Absent Connection Stub*](MicroscopeSolution.md#absent-connection-stub).

![Alternate Methods for Testing Gen AI](images/media/AlternateMethodsforTestingGenAI.png)

Note that using this technique can also **reduce token consumption** in test environments, with a material cost saving for the Enterprise.

#### Prompt Service

This solution runs Prompt Templates in Apex through a dedicated **Prompt Service**, rather than calling them directly from Agentforce Actions or Flows.

The flow is simple:

1. The caller references an *Invocation Call*.
2. The *Invocation CMT* record identifies which Prompt Template should be used.
3. That Invocation points to a reusable Method on the Prompt Service.
4. The Prompt Service runs the configured template.

For example, an Agentforce Action can call a reusable Apex Action that references an *Invocation Call*. A Flow can use the same pattern. This gives Prompt Templates the same governance, auditing, failover, and environment controls as any other service.

**How to Implement**: If you wish to implement this pattern, you can either run the relevant AI skill or check out the documentation that comes with the skill.

* **Refactor an Agentforce Apex Action**: [AI Skill](https://kevinhenryburke.github.io/microscope-pub/skills/microscope-refactor-invocable-action-apex/SKILL) | [Documentation](https://kevinhenryburke.github.io/microscope-pub/skills/microscope-refactor-invocable-action-apex/)

![Running Prompts via Standard Apex Action](images/media/RunningPromptsviaStandardApexAction.png)

#### Generative AI Governance and Security

All of the framework features for Security, Runtime, Governance, Release and Environment Management and Analysis are accessible via this mechanism.

#### Generative AI Prompt Safety Data Auditing

The framework can be configured to automatically create Audit records. For Prompt Templates, those records can also include Trust Layer-enhanced information about the health of the response and how toxic, abusive, or biased it might be, in addition to the user context, input, and output.

- Benefit (Generative AI Prompt Safety) : Real-time, realtime, in-context storage of Einstein Trust Layer scores against individual calls to LLMs inside the org. Flow and Apex triggers can act on these and Administrators can report on these records.

#### Generative AI Prompt Change Management

Because test environments may be limited both in data richness and system integrations, and because some businesses need to change Prompts very quickly, prompts may need to be tested in production environments within some Enterprises. [Invocation Permission-Based Variants](MicroscopeSolution.md#invocation-permission-based-processing) can be used to make those upgrades safer.

If a Prompt Template is live and a new version has been written, Enterprises typically upgrade the prompt in situ for all users. Without user testing, this risks making the service worse for at least some users.

Using Invocation Permissions, the process is as follows:

1.  Permission Overrides can be deployed alongside the default Invocation Metadata for the call to the Prompt Template. The override is identical to the default except that it references a (short-lived) Invocation Permission and references the newer Prompt Template.

2.  A group of Pilot Users is assigned the Invocation Permission and these will run the newer version of the Prompt Template. The majority of users without the permission continue to use the older version.

3.  When the pilot is deemed successful, the Invocation Permission and the Permission Override  record are removed and the default *Invocation CMT* record is altered to reference the newer Prompt Template.

Benefits include:

- Benefit (A/B Testing and Safe Upgrades of LLM interactions) : Groups of users assigned a Custom Permission can be pointed to updated Prompt Templates, while those without the permission continue to use the default template. Once all users have the permission, the default changes to the new template and the permission is removed.

#### Generative AI Role-Based Processing

Prompt Templates and Agentforce Actions provide a single implementation for all users in an org. Users from different roles, divisions or countries in an Enterprise can require both custom prompts and custom grounding for those prompts.

Using Permission Overrides for an Invocation Call that uses the Prompt Service, and assigning different custom permissions to groups of users, can run different Prompt Templates for them.

The example below shows a scenario with specific custom permissions for users in Spain and Germany, with users from those countries taken to their own specific prompt templates via Permission Overrides, shown in yellow. All other users, who do not have either permission, are routed via the default Invocation metadata record to an implementation which in this example does not interface to an LLM.

![Regional Custom Permissions for Prompt Variations](images/media/RegionalCustomPermissionsforPromptVariations.png)

- Benefit (Generative AI Role-Based) : Allow different LLMs (or no LLM) to be used in different jurisdictions to conform to regional legislation.

- Benefit (Generative AI Role-Based) : Agentforce Actions and Prompt Templates can run different implementations dynamically for different groups of users, based on job role, region or other business-meaningful criteria.

#### Generative AI Prompt Safety

Enterprises must protect their users and customers from unexpected or toxic responses from models. The Einstein Trust Layer calculates a safety score for every run of a Prompt Template which can be used to provide a range of protective functionalities.

The functionality is configurable in three main ways:

##### 1. Threshold-based responses

The Prompt Service can be configured by the admin with three decimal-valued environment parameters between 0 and 1. These thresholds determine what should happen when a Prompt Template returns a Safety Score.

  1.  *PromptFatalThreshold* - A Safety Score less than this value will cause a Method Alternate to run and block future attempts to run this Prompt Template. The Prompt Service creates a Custom Setting record programmatically which is checked by all future runs and, if found, directs processing to a [Down Alternate](MicroscopeSolution.md#alternate-processing-when-external-is-down). The block can be cleared by an Admin by removing the Custom Setting record.

  2.  *PromptErrorThreshold* - A Safety Score less than this value (but \> *PromptFatalThreshold*) will cause a Method Alternate to run but the Prompt Template remains accessible to future calls.

  3.  *PromptWarnThreshold* - A Safety Score less than this value will return the LLM response to the end user, however the Audit Record created will include an Error Code indicating that a suboptimal response was returned by the model. Note that *PromptWarnThreshold* \> *PromptErrorThreshold*.

##### 2. Prompt failover

Each Invocation that calls the Prompt Service can be configured to fail over. In this scenario, more than one Prompt Template is specified in the *Invocation CMT* record. The Prompt Templates are run in sequence until one returns a Safety Score higher than *PromptErrorThreshold*. The configured list may include prompts that call different models, increasing the chance that at least one template is safe at runtime.

##### 3. Prompt selection strategy

When an Invocation is configured for failover, the framework can also choose the order in which templates should run. The available algorithms are:

  1.  "Given Order" - Prompt Templates are run in the order they are listed in the Invocation Metadata configuration.

  2.  "Recent Safest" - A query is run against the Audit table calculating the mean Safety scores of recent runs of the configured Prompt Templates. The templates are then run in the returned order (safest first).

  3.  "Run All Return Safest" - all of the configured templates are run and the response from the template with the safest score is returned to the caller.

The first diagram shows two runs when the *Prompt Service* is not configured to Failover. In the first case a safe response is received (Safety \> *PromptWarnThreshold*), followed by a run where an unsafe response (Safety \< *PromptErrorThreshold*) is returned by the model.

![Prompt Handling Without Failover Configuration](images/media/PromptHandlingWithoutFailoverConfiguration.png)

The next diagram shows an Invocation configured to Failover with two Prompt Templates specified. It shows the functioning when an unsafe LLM response is received by the first template and the second is run as a failover.

![Prompt Handling with Configured Failover Processing](images/media/PromptHandlingwithConfiguredFailoverProcessing.png)

The next diagram shows the functionality when an invocation is configured to return the Recent Safest Prompt Template from a list.

![Processing Returning the Safest Prompt Template](images/media/ProcessingReturningtheSafestPromptTemplate.png)

Benefits include:

- Benefit (Generative AI Prompt Safety - Redaction) : If the response from a LLM for a Prompt Template has an unacceptable Einstein Trust Layer Safety Score, run alternate code to return a non-generative response to the end user.

- Benefit (Generative AI Prompt Safety - Failover) : Configure a group of prompt templates with similar functional definitions and run these in order, returning the output of the first that returns an acceptable Einstein Trust Layer Safety Score.

- Benefit (Generative AI Prompt Safety - Blocking) : Temporarily block future runs of any Prompt Template that achieves a low Einstein Trust Layer Safety Score on a single run.

- Benefit (Generative AI Prompt Safety - Recent Safest) : Configure a group of prompt templates with similar functional definitions and run the one with the best Einstein Trust Layer Safety Scores based on recent runs.

- Benefit (Generative AI Prompt Safety - Use Safest) : Configure a group of prompt templates, run each and use the output with the best Safety score as computed by the Einstein Trust Layer.


