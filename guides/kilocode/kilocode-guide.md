# Kilo Code Setup Guide: Custom Rules, Instructions, and Memory Banks

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Setting Up Custom Rules](#setting-up-custom-rules)
4. [Configuring Custom Instructions](#configuring-custom-instructions)
5. [Setting Up Memory Banks](#setting-up-memory-banks)
6. [Advanced Configuration](#advanced-configuration)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)
9. [Examples](#examples)
10. [Further Reading](#further-reading)

## Introduction

This guide provides comprehensive instructions for setting up Kilo Code with custom rules, instructions, and memory banks. Kilo Code is a powerful AI-assisted coding tool that can be customized to fit your specific development workflow and coding standards.

By the end of this guide, you'll have:
- ✅ Custom rules configured for your coding standards
- ✅ Personalized instructions for AI assistance
- ✅ Memory banks set up for context retention
- ✅ A working configuration optimized for your needs

## Prerequisites

Before starting, ensure you have:

- Kilo Code installed and running
- Basic understanding of JSON/YAML configuration files
- Write access to your Kilo Code configuration directory
- Text editor or IDE for editing configuration files

### Installation Verification

```bash
# Verify Kilo Code installation
kilocode --version

# Check configuration directory
kilocode config --show-path
```

## Setting Up Custom Rules

Custom rules allow you to enforce specific coding standards and practices within your projects.

### 1. Create Rules Configuration File

Create a `custom-rules.json` file in your Kilo Code configuration directory:

```bash
# Navigate to config directory
cd $(kilocode config --show-path)

# Create rules file
touch custom-rules.json
```

### 2. Define Rule Categories

Rules are organized into categories for better management:

```json
{
  "rules": {
    "code-style": {
      "enforce-naming-conventions": true,
      "max-line-length": 120,
      "require-documentation": true
    },
    "security": {
      "no-hardcoded-secrets": true,
      "validate-input": true,
      "secure-random": true
    },
    "performance": {
      "avoid-nested-loops": true,
      "optimize-database-queries": true,
      "cache-expensive-operations": true
    }
  }
}
```

### 3. Language-Specific Rules

Configure rules for specific programming languages:

```json
{
  "language-rules": {
    "javascript": {
      "use-strict-mode": true,
      "prefer-const": true,
      "no-var": true
    },
    "python": {
      "max-line-length": 88,
      "use-type-hints": true,
      "follow-pep8": true
    },
    "typescript": {
      "strict-mode": true,
      "explicit-return-types": true,
      "no-any": true
    }
  }
}
```

### 4. Custom Rule Definitions

Define your own rules with conditions and actions:

```json
{
  "custom-rules": [
    {
      "name": "require-error-handling",
      "description": "Ensure all API calls have error handling",
      "pattern": "fetch\\(|axios\\.|http\\.",
      "requirement": "try-catch or error callback",
      "severity": "error"
    },
    {
      "name": "consistent-logging",
      "description": "Use structured logging format",
      "pattern": "console\\.log",
      "suggestion": "Use logger.info() with structured format",
      "severity": "warning"
    }
  ]
}
```

## Configuring Custom Instructions

Custom instructions guide the AI assistant's behavior and responses.

### 1. Create Instructions File

```bash
# Create instructions configuration
touch custom-instructions.yaml
```

### 2. General Instructions

Define overall behavior and tone:

```yaml
general:
  tone: "professional and helpful"
  verbosity: "detailed with examples"
  code_style: "clean and readable"
  explanation_level: "intermediate"
  
preferences:
  - "Prefer functional programming patterns when appropriate"
  - "Always include error handling in code examples"
  - "Provide performance considerations for complex operations"
  - "Include unit tests for new functions"
```

### 3. Context-Specific Instructions

Tailor instructions for different scenarios:

```yaml
contexts:
  code_review:
    focus:
      - "Security vulnerabilities"
      - "Performance bottlenecks"
      - "Code maintainability"
      - "Test coverage"
    
  debugging:
    approach:
      - "Start with simple solutions"
      - "Use console/logging for investigation"
      - "Consider edge cases"
      - "Verify assumptions"
    
  refactoring:
    principles:
      - "Maintain existing functionality"
      - "Improve readability"
      - "Reduce complexity"
      - "Add documentation"
```

### 4. Project-Specific Instructions

Configure instructions for specific projects:

```yaml
projects:
  web-app:
    framework: "React with TypeScript"
    styling: "Tailwind CSS"
    testing: "Jest and React Testing Library"
    state_management: "Zustand"
    
  api-service:
    framework: "Express.js with TypeScript"
    database: "PostgreSQL with Prisma"
    authentication: "JWT with bcrypt"
    documentation: "OpenAPI/Swagger"
```

## Setting Up Memory Banks

Memory banks allow Kilo Code to retain context and learn from your coding patterns.

### 1. Initialize Memory Bank

```bash
# Create memory bank directory
mkdir -p memory-banks

# Initialize with configuration
kilocode memory init --type="project" --name="my-project"
```

### 2. Configure Memory Types

Set up different types of memory storage:

```json
{
  "memory-config": {
    "project-context": {
      "enabled": true,
      "retention-period": "30 days",
      "max-entries": 1000,
      "categories": [
        "code-patterns",
        "decision-rationale",
        "architectural-choices"
      ]
    },
    "coding-patterns": {
      "enabled": true,
      "learn-from-usage": true,
      "suggest-similar": true,
      "confidence-threshold": 0.8
    },
    "error-solutions": {
      "enabled": true,
      "track-resolutions": true,
      "suggest-fixes": true
    }
  }
}
```

### 3. Populate Memory Banks

Add initial knowledge to memory banks:

```json
{
  "knowledge-base": {
    "common-patterns": [
      {
        "pattern": "React component with hooks",
        "template": "functional component with useState and useEffect",
        "best-practices": ["proper cleanup", "dependency arrays", "error boundaries"]
      },
      {
        "pattern": "API error handling",
        "template": "try-catch with specific error types",
        "best-practices": ["user-friendly messages", "logging", "retry logic"]
      }
    ],
    "project-specific": {
      "architecture": "microservices with API gateway",
      "database-patterns": "repository pattern with services",
      "testing-strategy": "unit tests for business logic, integration for APIs"
    }
  }
}
```

## Advanced Configuration

### Environment-Specific Settings

Configure different settings for development, testing, and production:

```json
{
  "environments": {
    "development": {
      "rules": {
        "strictness": "medium",
        "auto-format": true,
        "debug-mode": true
      }
    },
    "production": {
      "rules": {
        "strictness": "high",
        "performance-checks": true,
        "security-scan": true
      }
    }
  }
}
```

### Team Configuration

Set up shared configurations for team consistency:

```yaml
team:
  shared-rules: true
  enforce-standards: true
  review-guidelines:
    - "All PRs require at least one approval"
    - "Security review for authentication changes"
    - "Performance review for database changes"
  
coding-standards:
  naming: "camelCase for variables, PascalCase for classes"
  documentation: "JSDoc for public methods"
  testing: "Minimum 80% coverage for new code"
```

## Best Practices

### ✅ Do's

- **Start Simple**: Begin with basic rules and gradually add complexity
- **Version Control**: Keep your configurations in version control
- **Team Alignment**: Ensure team members use consistent configurations
- **Regular Updates**: Review and update rules based on project evolution
- **Documentation**: Document custom rules and their rationale
- **Testing**: Test configurations with sample code before applying

### ❌ Don'ts

- **Over-Configure**: Avoid too many restrictive rules initially
- **Ignore Context**: Don't apply the same rules to all project types
- **Static Rules**: Don't set rules once and forget them
- **Individual Configs**: Avoid having different configs for each team member
- **Hardcoded Values**: Don't hardcode environment-specific values

### Performance Considerations

- Memory banks can impact performance with large datasets
- Regular cleanup of old memory entries
- Optimize rule complexity for faster processing
- Monitor Kilo Code resource usage

### Security Guidelines

- Never store sensitive data in configurations
- Use environment variables for secrets
- Regularly audit custom rules for security implications
- Implement proper access controls for shared configurations

## Troubleshooting

### Common Issues

#### 1. Configuration Not Loading

```bash
# Check configuration syntax
kilocode config validate

# Verify file permissions
ls -la $(kilocode config --show-path)

# Check configuration format
kilocode config lint
```

#### 2. Rules Not Applying

- Verify rule syntax in configuration file
- Check if rules are enabled for current project type
- Ensure Kilo Code is restarted after configuration changes

#### 3. Memory Bank Issues

```bash
# Clear memory bank cache
kilocode memory clear --cache

# Rebuild memory indexes
kilocode memory rebuild

# Check memory bank status
kilocode memory status
```

#### 4. Performance Problems

- Reduce memory bank retention period
- Simplify complex rules
- Check for recursive rule dependencies
- Monitor system resources

### Debugging Commands

```bash
# Enable debug mode
kilocode --debug

# View current configuration
kilocode config show

# Test specific rules
kilocode rules test --file="example.js"

# Check memory bank usage
kilocode memory stats
```

## Examples

See the [`samples/`](./samples/) directory for complete working examples:

- [`custom-rules-example.json`](./samples/custom-rules-example.json)
- [`instructions-example.yaml`](./samples/instructions-example.yaml)
- [`memory-bank-config.json`](./samples/memory-bank-config.json)
- [`setup-script.sh`](./samples/setup-script.sh)

### Quick Start Example

For a rapid setup, use our provided setup script:

```bash
# Download and run setup script
curl -O https://raw.githubusercontent.com/your-repo/kilocode-examples/main/setup-script.sh
chmod +x setup-script.sh
./setup-script.sh
```

## Further Reading

### Official Documentation
- [Kilo Code Advanced Usage - Custom Rules](https://kilocode.ai/docs/advanced-usage/custom-rules)
- [Kilo Code Advanced Usage - Custom Instructions](https://kilocode.ai/docs/advanced-usage/custom-instructions)
- [Kilo Code Advanced Usage - Memory Bank](https://kilocode.ai/docs/advanced-usage/memory-bank)

### Community Resources
- [Kilo Code GitHub Repository](https://github.com/kilocode/kilocode)
- [Community Examples and Templates](https://github.com/kilocode/examples)
- [Best Practices Blog Posts](https://kilocode.ai/blog/best-practices)

### Configuration References
- [JSON Schema for Rules](https://kilocode.ai/schemas/rules.json)
- [YAML Schema for Instructions](https://kilocode.ai/schemas/instructions.yaml)
- [Memory Bank API Reference](https://kilocode.ai/docs/api/memory)

### Tutorials and Guides
- [Setting Up Team Configurations](https://kilocode.ai/tutorials/team-setup)
- [Advanced Rule Customization](https://kilocode.ai/tutorials/advanced-rules)
- [Memory Bank Optimization](https://kilocode.ai/tutorials/memory-optimization)

---

**Need Help?** Join the [Kilo Code Community](https://community.kilocode.ai) or check our [FAQ](https://kilocode.ai/docs/faq).