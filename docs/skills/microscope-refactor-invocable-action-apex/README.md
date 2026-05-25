# microscope-refactor-invocable-action-apex: Agentforce Action in Apex

Use this skill to refactor an existing **Agentforce Action in Apex** (a class containing an `@InvocableMethod`) into a Microscope Service invocation. This ensures that your Agentforce logic follows the Microscope architectural patterns, shifting the heavy lifting to a reusable service method while keeping the Invocable method as a clean entry point.

## About the Skill

In your AI Code Generator terminal, simply ask the tool to:
> "Run the skill in `skills/microscope-refactor-invocable-action-apex/SKILL.md` to refactor an Agentforce Action in Apex."

You will be asked to provide:
1. The **name or file path** of the Apex class.
2. The target folders for service and invocation metadata.

## Testing

Deploy the classes in `./testSkill/classes` to your scratch org and then run the skill, specifying the `OrderHandler` class when prompted.