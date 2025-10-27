# Contributing to TSON

Thank you for your interest in contributing to TSON! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/tson.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests to ensure everything works: `python tests/test_round trip.py`
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/zenoaihq/tson.git
cd tson

# No external dependencies needed for core library
# Just Python 3.7+

# Run tests
python tests/test_round\ trip.py

# Try the examples
python examples/basic_usage.py
python test_tson_string.py
python llm_integration_example.py
```

## Code Guidelines

- Follow PEP 8 style guide for Python code
- Add tests for any new features
- Update documentation if you change functionality
- Keep commits focused and atomic
- Write clear commit messages

## Testing

Before submitting a PR, ensure:

1. All existing tests pass
2. New features include tests
3. Round-trip conversion works correctly
4. No regressions in token efficiency

Run tests:
```bash
python tests/test_round\ trip.py
```

Test specific TSON strings:
```bash
python test_tson_string.py
```

## Documentation

If you add new features:

1. Update README.md with usage examples
2. Update SPEC.md if syntax changes
3. Add examples to `examples/` directory
4. Update prompts.md if LLM integration changes

## Pull Request Process

1. Ensure your PR description clearly describes the problem and solution
2. Reference any related issues
3. Update the CHANGELOG if applicable
4. Ensure all tests pass
5. Request review from maintainers

## Bug Reports

When filing an issue, please include:

1. TSON version
2. Python version
3. Minimal code example that reproduces the bug
4. Expected behavior
5. Actual behavior
6. Error messages (if any)

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists or is planned
2. Describe the use case
3. Explain why it would benefit TSON users
4. Provide examples if possible

## Questions?

Feel free to open an issue for questions or discussions.

## License

By contributing to TSON, you agree that your contributions will be licensed under the MIT License.
