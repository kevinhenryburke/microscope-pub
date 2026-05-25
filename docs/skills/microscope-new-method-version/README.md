# microscope-new-method-version

This skill provides instructions to the AI Code Generator for creating a new Signature Version version of an existing Microscope *Method Iteration*.

## Features

- **Cloning & Scaffolding**: Automatically clones the existing implementation and test classes, stripping out previous business logic to provide a clean slate for the new version.
- **Versioning**: Increments the Signature Version number based on the highest existing version, and resets the Implementation Version to `1.0`.
- **Renaming**: Handles all renaming of classes and internal references to ensure the new version is self-contained.
- **Metadata Generation**: Creates new `Service_Method` and `Service_Implementation` metadata, correctly linking them together.

## Usage

To run this skill in your AI Code Generator terminal, simply ask the tool to: 
"Run the instructions in `skills/microscope-new-method-version/SKILL.md` to create a new method version (Signature Version) of an existing Microscope Method Iteration."

## Testing

The easiest way to test this skill is to use the existing `Payment` service and method created by the `microscope-new-method-setup` skill.
