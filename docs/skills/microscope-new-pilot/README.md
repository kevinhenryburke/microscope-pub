# microscope-new-pilot

This skill provides instructions for creating a new pilot for an existing Microscope Service-side implementation.

## Features

- **Implementation Versioning**: Automatically runs the `microscope-new-implementation-version` skill to clone and increment the existing implementation class, test class, and metadata.
- **Custom Permission Setup**: Generates a new Custom Permission to restrict access to the pilot.
- **Pilot Invocation Creation**: Creates a new Invocation metadata record configured as a Permission Overridecorrectly linking the original Invocation Call to the new Custom Permission and the newly generated implementation version.

## Usage

To run this skill in your AI Code Generator terminal simply ask the tool to "run the instructions in the file skills/microscope-new-pilot/SKILL.md to create a new pilot implementation from an existing Invocation."

## Testing

The easiest way to test this skill is to use an existing Invocation record from your project that you wish to try implementing a pilot variant for.
