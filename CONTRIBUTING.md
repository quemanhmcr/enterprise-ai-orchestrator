# Contributing to Enterprise Business AI System

Thank you for your interest in contributing to the Enterprise Business AI System! We welcome contributions from the community to help improve this project.

## Development Process

1.  **Fork the repository** and create your branch from `main`.
2.  **Install dependencies**:
    ```bash
    make install
    ```
3.  **Make your changes**. Ensure you follow the coding standards.
4.  **Run tests**:
    ```bash
    make test
    ```
5.  **Lint and format your code**:
    ```bash
    make format
    make lint
    ```
6.  **Submit a Pull Request**.

## Coding Standards

-   We use **Black** for code formatting.
-   We use **Ruff** for linting.
-   We use **Pytest** for testing.
-   All new features should include appropriate tests.
-   Docstrings should follow the Google Python Style Guide.

## Pull Request Process

1.  Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2.  Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
3.  Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent.
4.  You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Reporting Issues

Please use the GitHub Issues tracker to report bugs or request features.
