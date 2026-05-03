# Microscope Architectural Framework for Salesforce

## Introduction

Enterprise Salesforce orgs become harder to understand as they grow. Teams lose visibility of how business functions, code, and dependencies connect, and the consequences of change become harder to predict. Delivery slows, release risk increases, and time to market suffers.

This application addresses that problem and solves several others by splitting a complex org's customisations into **business-aligned partitions**. Links between those partitions are **decoupled**, **abstracted**, and managed through **custom metadata** at an architectural level. Reporting and visualizations over that metadata let teams understand how the org is structured through a macro-level business lens.

There are many beneficial features:

- It defines a **holistic, multi-faceted, architecture at scale pattern** which puts metadata control at the heart of the architecture, which provides clarity and business insights. It also provides a companion process for architectural delivery that teams need to deliver consistently and predictably.

- Decoupling promotes the use of very clearly scoped **Services**. Enterprises can create **concurrent versions**, which can be released quickly and independently. It solves the existing problems of supporting **phased adoption** and instant **rollback**.

- Platform permissioning features for users (**Custom Permissions**) can be used to override metadata so that different behaviors for different users or environments can be facilitated. This greatly simplifies the challenges enterprises face in delivering regional processing variations across multiple markets. This need will increase with wider adoption of Gen AI functionality like **Prompt Templates** and **Agentforce Actions**.

- It allows for **piloting** and **A/B testing** of functionality for groups of suitably permissioned users in a new and structured way. This can be applied to pilot changes to Prompt Templates and Agentforce Actions.

- The decoupled architecture allows for switchable alternative processing in environments that can be directed by using **Custom Settings**. The alternates may be simulated responses in development and testing contexts or failover outage processing in production. This approach is superior to the norm of mocking interfaces as it is standardized and configuration-controlled and allows very quick switching to alternative processing.

- The application **audits** every call across each connection, creating a single source of processing and error information across the org. The core platform does not provide an equivalent easy-to-use, standardized transactional log.

- The application audit provides a critical new data source that can be uploaded to business intelligence platforms through simple configuration. User interactions can be captured in Salesforce **Data 360**, enriching the overall customer view and providing a valuable new data source for generative AI grounding and summarization.

- Dependencies are managed through decoupling and abstraction. This approach complements and facilitates greater use of **Salesforce DX packaging**, which is hard to adopt in Enterprises due to org complexity. The application also contains a structured approach to remediating technical debt.

- The application audit supports **rerunning of transactions**, which is unique to this platform.
