

# Microscope Package Installation

The main package is called **Microscope** and uses the namespace **mscope**. The latest recommended version can be installed via this link:

[Microscope Package installation URL](https://login.salesforce.com/packaging/installPackage.apexp?p0=04tJ7000000DHMBIA4)

Alternatively you can install the package using the SFDX CLI, for example:

```bash
sf package install --package 04tJ7000000DHMBIA4 --target-org <target-org> --wait 20
```

We recommend that you install the app for Administrators only, the objects or reports are needed for administrative users only and not by end users of the org. Additional sharing of reports and objects might be needed for business analysis and in the case can be shared to other non-admin users using the standard platform folder and object sharing techniques (e.g. permission sets and groups).

Sometimes there will be a separate pre-release version of the package available. If so, you can install it using the above commands but replacing the Subscriber Package Version Id. The latest pre-release version is: 04tJ7000000DHMBIA4.


### Platform Cache

One important thing to consider post-install involves __Platform Cache__. A cache partition called __mscope.FrameworkCache__ is packaged with the app but no space is allocated to it (doing so would cause installation to fail in orgs without platform cache available.) After installation, if you have platform cache available in the org then allocate at least 1MB of Org Cache to get the performance benefits of using the Cache. Developer Edition orgs for example have no cache allocation so this is not going to be usable in those orgs. The app still functions however but is slightly slower as a result.

This one cache partition is used by all invocations across the org, regardless of namespaces. 

Note also to check the partition size after each Microscope package upgrade, it may have been reset by a package push

### Permission Sets

End users do not need any permissions to use Microscope, but you will need to assign the following permission sets to some admin and system users:

#### microscopeAdmin

Provides the core access needed to administer the Microscope application. It is the lightest of the five sets and is focused on surfacing the packaged admin UI rather than granting broad object CRUD.

This permission set makes the `Service_Framework_Dashboards` app visible and exposes the main admin-facing tabs: `Invocation_Dashboard`, `Microscope_Admin_Jobs`, `Service_Dashboard`, and `Service_Framework_Audit__c`.

#### microscopeBatch

Grants access required to run Microscope batch jobs and use the rerun capability. It is intended for users who need to create, manage, and review batch processing runs rather than only view results.

The permission set provides create, read, edit, and delete access across `Batch_Item_Run__c`, `Batch_Item__c`, `Batch_Run__c`, and `Rerun_Group__c`, with broad field-level access for batch input, output, feedback, semantic scoring, safety scoring, and rerun configuration fields. It also makes the related tabs visible and enables all packaged batch and rerun record types, including Agentforce, Models API, Prompt Test, Audit Rerun, and Data Upload variants.

#### microscopeAuditEdit / microscopeAuditRead

Provides edit / read access respectively to the Microscope audit object so administrators and support users can inspect and maintain detailed execution history. It is centered on the audit trail captured for service invocations.

The permission set grants full access to `Service_Framework_Audit__c` and exposes its tab. Its field permissions cover a wide audit footprint including service and invocation identifiers, status and duration data, input and output payloads, error details, validation state, user and context information, cache usage, semantic scoring, and safety scoring fields.

#### microscopeInvocationValidationEdit / microscopeInvocationValidationRead

Provides edit / read access respectively to the Microscope invocation validation object. It is used for reviewing and maintaining validation records that describe how invocations map to services, implementations, and metadata.

The permission set grants full access to `Invocation_Validation__c` and makes its tab visible. The field access includes invocation metadata, service and method references, implementation class and flow references, alternate and fallback mappings, pilot and scratch stub details, validation state, configuration warnings, and related versioning fields.

#### microscopeServiceValidationEdit / microscopeServiceValidationRead

Provides edit / read access respectively to the service validation model used by Microscope. This covers the validation objects that describe services, methods, implementations, and underlying implementation artefacts.

The permission set grants access to `Service_Validation__c`, `Method_Validation__c`, `Implementation_Validation__c`, and `Implementation_Artefact__c`, and makes all four tabs visible. Its field permissions cover service names, package and permission metadata, method definitions and documentation links, implementation versions and variant keys, artefact references, historic flags, and rollup-style activity counts such as active methods, implementations, and invocations.

#### microscopeAgent

Provides the access needed to run Microscope Agent actions. This permission set is intended for users or system contexts that need to invoke the packaged agent functionality, rather than administer the broader Microscope application.

The permission set grants Apex class access to the packaged agent action classes `ActionSObjectSObject` and `ActionStringString`, and also enables access to the core Microscope custom metadata used by the agent layer. This includes service, method, invocation, event, release, implementation, platform event, business bundle, and service error code metadata definitions.
