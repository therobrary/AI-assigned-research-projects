# GitHub Copilot Custom Instructions Guide for VS Code

A comprehensive guide to setting up repository-level custom instructions for GitHub Copilot in Visual Studio Code.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setting Up Custom Instructions](#setting-up-custom-instructions)
- [Custom Instructions Schema](#custom-instructions-schema)
- [Practical Examples](#practical-examples)
- [Best Practices](#best-practices)
- [Troubleshooting & FAQs](#troubleshooting--faqs)
- [References](#references)

## Overview

GitHub Copilot custom instructions allow you to provide repository-specific context and guidelines that influence how Copilot generates code suggestions. This feature helps ensure that AI-generated code follows your project's conventions, coding standards, and architectural patterns.

### Benefits

- **Consistent Code Style**: Enforce coding standards and conventions across your team
- **Context-Aware Suggestions**: Provide domain-specific knowledge and project structure
- **Quality Improvements**: Guide Copilot toward better practices and patterns
- **Team Productivity**: Reduce code review cycles by getting better initial suggestions

## Prerequisites

Before setting up custom instructions, ensure you have:

- **GitHub Copilot subscription** (Individual, Business, or Enterprise)
- **VS Code** with the GitHub Copilot extension installed
- **Repository access** with write permissions to create `.github/` files
- **VS Code version 1.73.0 or later** (recommended for best compatibility)

## Setting Up Custom Instructions

### Step 1: Create the Instructions File

Create a file named `copilot-instructions.md` in your repository's `.github/` directory:

```
your-repo/
├── .github/
│   └── copilot-instructions.md
├── src/
└── README.md
```

### Step 2: Configure VS Code Settings

Ensure GitHub Copilot custom instructions are enabled in VS Code:

1. Open VS Code Settings (`Ctrl+,` / `Cmd+,`)
2. Search for "copilot instructions"
3. Verify that **"GitHub Copilot: Enable Custom Instructions"** is checked
4. Optionally, adjust the **"GitHub Copilot: Instructions Priority"** setting

### Step 3: Restart VS Code

After creating your instructions file, restart VS Code to ensure the custom instructions are loaded.

## Custom Instructions Schema

The `.github/copilot-instructions.md` file uses standard Markdown format with specific sections that Copilot recognizes:

### Basic Structure

```markdown
# Custom Instructions for [Project Name]

## Code Style and Conventions
[Your coding standards and style preferences]

## Architecture and Patterns
[Project architecture guidelines and preferred patterns]

## Dependencies and Libraries
[Preferred libraries, frameworks, and tools]

## Testing Guidelines
[Testing conventions and frameworks]

## Domain-Specific Context
[Business logic, domain knowledge, and project-specific requirements]
```

### Supported Content Types

- **Text descriptions** of coding standards and conventions
- **Code examples** showing preferred patterns
- **Lists** of preferred libraries or forbidden practices
- **Architecture diagrams** (using Markdown or ASCII art)
- **Links** to external documentation and style guides

## Practical Examples

### Example 1: Team Conventions

```markdown
# Custom Instructions for Our Project

## Code Style and Conventions
- Use TypeScript with strict mode enabled
- Follow the Airbnb JavaScript style guide
- Use camelCase for variables and functions, PascalCase for classes
- Prefer const over let, avoid var
- Use async/await instead of Promise.then()
- Maximum line length: 100 characters

## Error Handling
- Always use typed errors extending Error class
- Include contextual information in error messages
- Log errors with appropriate severity levels using our logger utility

## Testing
- Write unit tests using Jest framework
- Use React Testing Library for component tests
- Maintain minimum 80% code coverage
- Follow AAA pattern (Arrange, Act, Assert)
```

### Example 2: Language-Specific Configuration

```markdown
# Python Project Custom Instructions

## Code Style
- Follow PEP 8 style guidelines
- Use Black for code formatting
- Maximum line length: 88 characters (Black default)
- Use type hints for all function parameters and return values

## Dependencies
- Prefer standard library solutions when possible
- Use pandas for data manipulation
- Use requests for HTTP calls
- Use pytest for testing

## Architecture
- Follow clean architecture principles
- Separate business logic from infrastructure
- Use dependency injection for external services
- Create interfaces for all external dependencies
```

### Example 3: React/Frontend Project

```markdown
# React Frontend Custom Instructions

## Component Guidelines
- Use functional components with hooks instead of class components
- Prefer named exports over default exports
- Use TypeScript interfaces for all props
- Follow the container/presenter component pattern

## State Management
- Use React Context for global state
- Prefer useState and useReducer over external state libraries
- Keep state as close to where it's used as possible

## Styling
- Use CSS Modules for component styling
- Follow BEM naming convention for CSS classes
- Use CSS custom properties for theme values
- Avoid inline styles except for dynamic values
```

### Example 4: Quality-of-Life Improvements

```markdown
# Development Quality Guidelines

## Performance Considerations
- Implement lazy loading for large components
- Use React.memo for expensive pure components
- Optimize images and assets before committing
- Consider bundle size impact when adding dependencies

## Security
- Validate all user inputs
- Use parameterized queries for database operations
- Never commit secrets or API keys
- Implement proper authentication and authorization

## Documentation
- Write JSDoc comments for all public functions
- Update README.md when adding new features
- Include examples in function documentation
- Document complex business logic inline
```

## Best Practices

### Writing Effective Instructions

1. **Be Specific**: Provide concrete examples rather than vague guidelines
2. **Keep It Current**: Regularly update instructions as your project evolves
3. **Use Examples**: Include code snippets showing preferred patterns
4. **Prioritize**: Put the most important guidelines first
5. **Be Concise**: Avoid overly verbose instructions that may dilute important points

### File Organization

```markdown
# Recommended Structure
1. Project overview and context
2. Critical coding standards
3. Architecture patterns
4. Testing requirements
5. Performance considerations
6. Security guidelines
7. Additional resources and links
```

### Version Control Best Practices

- **Review Changes**: Treat custom instructions like code - review all changes
- **Document Updates**: Include changelog comments when updating instructions
- **Test Impact**: Verify that instruction changes improve code suggestions
- **Team Alignment**: Ensure all team members agree on the guidelines

## Troubleshooting & FAQs

### Common Issues

#### Q: My custom instructions don't seem to be working
**A:** Check the following:
- Ensure the file is named exactly `copilot-instructions.md`
- Verify the file is in the `.github/` directory at the repository root
- Restart VS Code after making changes
- Check that GitHub Copilot extension is up to date

#### Q: Copilot is not following my instructions consistently
**A:** Consider these factors:
- Instructions may be too vague - be more specific
- Complex instructions might be ignored - simplify and prioritize
- Large files may not be fully processed - keep instructions concise
- Some suggestions may override instructions based on context

#### Q: How do I know if my instructions are being used?
**A:** Indicators that instructions are working:
- Code suggestions match your specified patterns
- Generated code follows your naming conventions
- Suggested libraries match your preferences
- Comments and documentation style align with guidelines

#### Q: Can I use multiple instruction files?
**A:** No, GitHub Copilot only recognizes one `copilot-instructions.md` file per repository in the `.github/` directory.

### Performance Considerations

- **File Size**: Keep instructions under 2KB for optimal performance
- **Complexity**: Simple, clear instructions work better than complex ones
- **Update Frequency**: Changes take effect after VS Code restart

### Debugging Tips

1. **Test Incrementally**: Add instructions gradually to identify what works best
2. **Use Comments**: Add comments in your code to reinforce instructions
3. **Monitor Suggestions**: Pay attention to how suggestions change after updates
4. **Team Feedback**: Collect feedback from team members on suggestion quality

## Advanced Configuration

### Multi-Language Projects

For projects using multiple programming languages, organize instructions by language:

```markdown
# Multi-Language Project Instructions

## General Guidelines
[Cross-language standards]

## JavaScript/TypeScript
[JS/TS specific guidelines]

## Python
[Python specific guidelines]

## CSS/Styling
[Styling guidelines]
```

### Integration with Other Tools

- **ESLint/Prettier**: Mention your linting rules in instructions
- **Husky/Git Hooks**: Reference pre-commit requirements
- **CI/CD**: Include deployment and testing pipeline considerations

### Environment-Specific Instructions

```markdown
## Development Environment
- Use development database connections
- Enable debug logging
- Include source maps

## Production Considerations
- Optimize for performance
- Minimize bundle size
- Use production-ready error handling
```

## References

- [Official GitHub Documentation: Adding repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/custom-instructions/adding-repository-custom-instructions-for-github-copilot?tool=vscode)
- [GitHub Copilot VS Code Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- [GitHub Copilot Best Practices](https://docs.github.com/en/copilot/using-github-copilot/best-practices-for-using-github-copilot)
- [VS Code Settings Documentation](https://code.visualstudio.com/docs/getstarted/settings)

### Additional Resources

- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [React Best Practices](https://react.dev/learn)
- [Python PEP 8 Style Guide](https://peps.python.org/pep-0008/)

---

**Last Updated**: [Current Date]  
**Contributors**: [Your Team]  
**Reviewed By**: DX Team