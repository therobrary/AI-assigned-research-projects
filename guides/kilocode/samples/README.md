# Kilo Code Sample Configurations

This directory contains example configuration files and helper scripts for setting up Kilo Code with custom rules, instructions, and memory banks.

## Files Overview

### Configuration Files

- **`custom-rules-example.json`** - Complete example of custom coding rules
  - Code style enforcement
  - Security rules
  - Performance guidelines
  - Language-specific rules
  - Custom rule definitions

- **`instructions-example.yaml`** - AI assistant behavior configuration
  - General preferences and tone
  - Context-specific instructions
  - Project-specific settings
  - Coding standards
  - Response templates

- **`memory-bank-config.json`** - Memory and learning system configuration
  - Project context settings
  - Pattern recognition
  - Error tracking
  - Team knowledge sharing
  - Performance optimization

### Helper Scripts

- **`setup-script.sh`** - Automated setup script
  - Validates Kilo Code installation
  - Creates configuration directories
  - Backs up existing configurations
  - Copies sample files
  - Initializes memory banks

## Quick Start

### Option 1: Automated Setup

1. Make the setup script executable:
   ```bash
   chmod +x setup-script.sh
   ```

2. Run the setup script:
   ```bash
   ./setup-script.sh
   ```

### Option 2: Manual Setup

1. Locate your Kilo Code configuration directory:
   ```bash
   kilocode config --show-path
   ```

2. Copy the desired configuration files:
   ```bash
   cp custom-rules-example.json ~/.kilocode/custom-rules.json
   cp instructions-example.yaml ~/.kilocode/custom-instructions.yaml
   cp memory-bank-config.json ~/.kilocode/memory-bank-config.json
   ```

3. Restart Kilo Code or your IDE to load the new configurations.

## Customization Guide

### Custom Rules (`custom-rules-example.json`)

Key sections to customize:

```json
{
  "rules": {
    "code-style": {
      "max-line-length": 120,  // Adjust based on your preference
      "require-documentation": true
    }
  },
  "language-rules": {
    "javascript": {
      "prefer-const": true,    // Enable/disable specific rules
      "no-var": true
    }
  }
}
```

### Instructions (`instructions-example.yaml`)

Key sections to customize:

```yaml
general:
  tone: "professional and helpful"  # Adjust AI personality
  verbosity: "detailed with examples"  # Control response length

projects:
  web-app:
    framework: "React with TypeScript"  # Update for your stack
    testing: "Jest and React Testing Library"
```

### Memory Banks (`memory-bank-config.json`)

Key sections to customize:

```json
{
  "memory-config": {
    "project-context": {
      "retention-period": "30 days",  // Adjust retention
      "max-entries": 1000
    },
    "team-knowledge": {
      "shared-patterns": true,  // Enable/disable team sharing
      "privacy-level": "team-only"
    }
  }
}
```

## Validation

### Check Configuration Syntax

```bash
# Validate JSON files
jq empty custom-rules-example.json
jq empty memory-bank-config.json

# Validate YAML files
yq eval . instructions-example.yaml

# Validate with Kilo Code
kilocode config validate
```

### Test Configuration

```bash
# Test rules on a sample file
kilocode rules test --file="example.js"

# Check memory bank status
kilocode memory status

# Verify instructions are loaded
kilocode config show
```

## Common Customizations

### For Different Project Types

#### React/TypeScript Project
- Enable TypeScript strict mode rules
- Configure React-specific patterns
- Set up component testing guidelines

#### Node.js API Project
- Enable security-focused rules
- Configure database transaction patterns
- Set up API documentation requirements

#### Python Project
- Configure PEP 8 compliance
- Enable type hint requirements
- Set up pytest patterns

### For Different Team Sizes

#### Small Team (2-5 developers)
- Lighter rule enforcement
- Informal documentation requirements
- Shared memory banks

#### Large Team (10+ developers)
- Strict rule enforcement
- Comprehensive documentation
- Team-specific configurations

## Troubleshooting

### Configuration Not Loading

1. Check file permissions:
   ```bash
   ls -la ~/.kilocode/
   ```

2. Validate syntax:
   ```bash
   kilocode config validate
   ```

3. Check Kilo Code logs:
   ```bash
   kilocode --debug
   ```

### Rules Not Applying

1. Verify rule syntax in configuration
2. Check if rules are enabled for file type
3. Restart Kilo Code after changes

### Memory Bank Issues

1. Clear cache and rebuild:
   ```bash
   kilocode memory clear --cache
   kilocode memory rebuild
   ```

2. Check storage space and permissions

## Advanced Usage

### Environment-Specific Configurations

Create different configurations for different environments:

```bash
# Development environment
cp custom-rules-example.json ~/.kilocode/rules-dev.json

# Production environment
cp custom-rules-example.json ~/.kilocode/rules-prod.json
```

### Team Synchronization

Set up shared configurations in your project repository:

```bash
# Project root
mkdir .kilocode
cp samples/*.json .kilocode/
git add .kilocode/
```

### CI/CD Integration

Add validation to your CI pipeline:

```yaml
# .github/workflows/validate.yml
steps:
  - name: Validate Kilo Code Config
    run: kilocode config validate
```

## Need Help?

- Check the main guide: [`../kilocode-guide.md`](../kilocode-guide.md)
- Review official documentation: https://kilocode.ai/docs
- Join the community: https://community.kilocode.ai