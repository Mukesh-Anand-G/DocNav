# Contributing to DocNav

Thank you for your interest in contributing to DocNav! This document provides guidelines for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Bug Reports**: Use the [GitHub Issues](https://github.com/Mukesh-Anand-G/DocNav/issues) page
2. **Feature Requests**: Open an issue with the "enhancement" label
3. **Questions**: Use [GitHub Discussions](https://github.com/Mukesh-Anand-G/DocNav/discussions)

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/DocNav.git
   cd DocNav
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e .[dev]
   ```

4. **Run tests**
   ```bash
   pytest
   ```

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

4. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Code Style

- **Python**: Follow PEP 8
- **Formatting**: Use `black docnav/`
- **Type hints**: Add type annotations where appropriate
- **Documentation**: Update README.md for new features

## 🧪 Testing

- **Unit tests**: `pytest tests/`
- **Integration tests**: Test CLI commands
- **Manual testing**: Test with various document formats

## 📚 Documentation

- **README.md**: Keep it updated with new features
- **Code comments**: Add comments for complex logic
- **Examples**: Provide usage examples

## 🏷️ Labels for Issues

- `bug`: Bug reports
- `enhancement`: Feature requests
- `documentation`: Documentation issues
- `good first issue`: Good for newcomers
- `help wanted`: Community help needed

## 🚀 Release Process

1. Update version in `pyproject.toml` and `__init__.py`
2. Update `CHANGELOG.md`
3. Create a release tag
4. Build and publish to PyPI

## 💡 Guidelines

- **Be respectful**: Maintain a welcoming and inclusive environment
- **Be patient**: Reviews may take time
- **Be thorough**: Test your changes before submitting
- **Ask questions**: Use discussions for clarification

## 📞 Getting Help

- **Documentation**: Check the [README.md](README.md)
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Ask questions in GitHub Discussions

Thank you for contributing to DocNav! 🎉
