# Tests

All unit tests in this project are written using Python's built-in `unittest` framework. If you wish to contribute, please follow this convention and use `unittest` for any new tests.

## Credentials

For safety, always create and use a separate JSON file for your credentials when testing or using this library. Do not hard-code credentials in your test files. Helpful utilities are provided in this directory to make loading and using your credentials easier.

**Note:**  
The `.gitignore` file is configured to prevent a `credentials.json` file` from being committed to the repository. Always verify that your sensitive information is not included in commits.

Thank you for helping keep this project secure and consistent!
