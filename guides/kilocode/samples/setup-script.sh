#!/bin/bash

# Kilo Code Setup Script
# This script helps you quickly set up Kilo Code with custom rules, instructions, and memory banks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Kilo Code is installed
check_kilocode_installation() {
    log_info "Checking Kilo Code installation..."
    
    if ! command -v kilocode &> /dev/null; then
        log_error "Kilo Code is not installed or not in PATH"
        echo "Please install Kilo Code first: https://kilocode.ai/docs/installation"
        exit 1
    fi
    
    local version=$(kilocode --version 2>/dev/null || echo "unknown")
    log_success "Kilo Code found (version: $version)"
}

# Get Kilo Code configuration directory
get_config_dir() {
    local config_dir
    if command -v kilocode &> /dev/null; then
        config_dir=$(kilocode config --show-path 2>/dev/null || echo "$HOME/.kilocode")
    else
        config_dir="$HOME/.kilocode"
    fi
    echo "$config_dir"
}

# Create configuration directory if it doesn't exist
create_config_dir() {
    local config_dir="$1"
    
    if [ ! -d "$config_dir" ]; then
        log_info "Creating configuration directory: $config_dir"
        mkdir -p "$config_dir"
        log_success "Configuration directory created"
    else
        log_info "Configuration directory already exists: $config_dir"
    fi
}

# Backup existing configuration
backup_existing_config() {
    local config_dir="$1"
    local backup_dir="${config_dir}/backup-$(date +%Y%m%d-%H%M%S)"
    
    if [ -f "$config_dir/custom-rules.json" ] || [ -f "$config_dir/custom-instructions.yaml" ] || [ -f "$config_dir/memory-bank-config.json" ]; then
        log_info "Backing up existing configuration..."
        mkdir -p "$backup_dir"
        
        [ -f "$config_dir/custom-rules.json" ] && cp "$config_dir/custom-rules.json" "$backup_dir/"
        [ -f "$config_dir/custom-instructions.yaml" ] && cp "$config_dir/custom-instructions.yaml" "$backup_dir/"
        [ -f "$config_dir/memory-bank-config.json" ] && cp "$config_dir/memory-bank-config.json" "$backup_dir/"
        
        log_success "Backup created at: $backup_dir"
    fi
}

# Copy sample configurations
copy_sample_configs() {
    local config_dir="$1"
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    log_info "Copying sample configurations..."
    
    # Copy custom rules
    if [ -f "$script_dir/custom-rules-example.json" ]; then
        cp "$script_dir/custom-rules-example.json" "$config_dir/custom-rules.json"
        log_success "Custom rules configuration copied"
    else
        log_warning "Custom rules example file not found"
    fi
    
    # Copy instructions
    if [ -f "$script_dir/instructions-example.yaml" ]; then
        cp "$script_dir/instructions-example.yaml" "$config_dir/custom-instructions.yaml"
        log_success "Custom instructions configuration copied"
    else
        log_warning "Instructions example file not found"
    fi
    
    # Copy memory bank config
    if [ -f "$script_dir/memory-bank-config.json" ]; then
        cp "$script_dir/memory-bank-config.json" "$config_dir/memory-bank-config.json"
        log_success "Memory bank configuration copied"
    else
        log_warning "Memory bank config file not found"
    fi
}

# Validate configuration files
validate_configs() {
    local config_dir="$1"
    
    log_info "Validating configuration files..."
    
    # Validate JSON files
    for json_file in "$config_dir/custom-rules.json" "$config_dir/memory-bank-config.json"; do
        if [ -f "$json_file" ]; then
            if command -v jq &> /dev/null; then
                if jq empty "$json_file" 2>/dev/null; then
                    log_success "$(basename "$json_file") is valid JSON"
                else
                    log_error "$(basename "$json_file") contains invalid JSON"
                    return 1
                fi
            else
                log_warning "jq not found, skipping JSON validation for $(basename "$json_file")"
            fi
        fi
    done
    
    # Validate YAML files
    if [ -f "$config_dir/custom-instructions.yaml" ]; then
        if command -v yq &> /dev/null; then
            if yq eval . "$config_dir/custom-instructions.yaml" >/dev/null 2>&1; then
                log_success "custom-instructions.yaml is valid YAML"
            else
                log_error "custom-instructions.yaml contains invalid YAML"
                return 1
            fi
        else
            log_warning "yq not found, skipping YAML validation"
        fi
    fi
    
    # Validate with Kilo Code if available
    if command -v kilocode &> /dev/null; then
        if kilocode config validate 2>/dev/null; then
            log_success "Kilo Code configuration validation passed"
        else
            log_warning "Kilo Code configuration validation failed"
        fi
    fi
}

# Initialize memory banks
initialize_memory_banks() {
    local config_dir="$1"
    
    log_info "Initializing memory banks..."
    
    if command -v kilocode &> /dev/null; then
        # Create memory bank directory
        mkdir -p "$config_dir/memory-banks"
        
        # Initialize project memory bank
        if kilocode memory init --type="project" --name="default" 2>/dev/null; then
            log_success "Project memory bank initialized"
        else
            log_warning "Failed to initialize project memory bank (command may not exist)"
        fi
    else
        log_warning "Kilo Code command not available, skipping memory bank initialization"
    fi
}

# Set up Git hooks (optional)
setup_git_hooks() {
    if [ -d ".git" ]; then
        log_info "Setting up Git hooks..."
        
        local hook_file=".git/hooks/pre-commit"
        if [ ! -f "$hook_file" ]; then
            cat > "$hook_file" << 'EOF'
#!/bin/bash
# Kilo Code pre-commit hook

if command -v kilocode &> /dev/null; then
    echo "Running Kilo Code validation..."
    if ! kilocode validate --staged; then
        echo "Kilo Code validation failed. Commit aborted."
        exit 1
    fi
fi
EOF
            chmod +x "$hook_file"
            log_success "Git pre-commit hook created"
        else
            log_info "Git pre-commit hook already exists"
        fi
    else
        log_info "Not in a Git repository, skipping Git hooks setup"
    fi
}

# Main setup function
main() {
    echo "========================================"
    echo "       Kilo Code Setup Script"
    echo "========================================"
    echo
    
    # Check installation
    check_kilocode_installation
    
    # Get configuration directory
    local config_dir
    config_dir=$(get_config_dir)
    log_info "Using configuration directory: $config_dir"
    
    # Create config directory
    create_config_dir "$config_dir"
    
    # Backup existing configuration
    backup_existing_config "$config_dir"
    
    # Copy sample configurations
    copy_sample_configs "$config_dir"
    
    # Validate configurations
    if ! validate_configs "$config_dir"; then
        log_error "Configuration validation failed"
        exit 1
    fi
    
    # Initialize memory banks
    initialize_memory_banks "$config_dir"
    
    # Set up Git hooks
    setup_git_hooks
    
    echo
    echo "========================================"
    log_success "Kilo Code setup completed successfully!"
    echo "========================================"
    echo
    echo "Next steps:"
    echo "1. Review and customize the configuration files in: $config_dir"
    echo "2. Restart your IDE or editor to load the new configurations"
    echo "3. Test Kilo Code with your project"
    echo
    echo "Configuration files created:"
    echo "- custom-rules.json: Coding rules and standards"
    echo "- custom-instructions.yaml: AI assistant instructions"
    echo "- memory-bank-config.json: Memory and learning settings"
    echo
    echo "For more information, see the guide: guides/kilocode/kilocode-guide.md"
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "Kilo Code Setup Script"
        echo
        echo "Usage: $0 [options]"
        echo
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --version, -v  Show script version"
        echo
        echo "This script will:"
        echo "1. Check Kilo Code installation"
        echo "2. Create configuration directory"
        echo "3. Backup existing configurations"
        echo "4. Copy sample configurations"
        echo "5. Validate configuration files"
        echo "6. Initialize memory banks"
        echo "7. Set up Git hooks (if in a Git repository)"
        exit 0
        ;;
    --version|-v)
        echo "Kilo Code Setup Script v1.0.0"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac