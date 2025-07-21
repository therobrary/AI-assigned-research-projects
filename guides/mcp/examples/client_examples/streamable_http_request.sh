#!/bin/bash

# MCP Streamable HTTP Client Example
# ==================================
# 
# This script demonstrates how to interact with MCP Streamable HTTP servers
# via the MCP Gateway. Streamable HTTP servers are designed for handling
# large data transfers with efficient streaming.
#
# Usage: ./streamable_http_request.sh [options]
#
# Options:
#   -u, --url URL          MCP Gateway URL (default: http://localhost:8080)
#   -k, --api-key KEY      API key for authentication
#   -f, --file FILE        File to upload/process
#   -o, --output FILE      Output file for downloaded data
#   -t, --timeout SECONDS  Request timeout (default: 600)
#   -v, --verbose          Enable verbose output
#   -h, --help             Show this help message

set -euo pipefail

# Default configuration
MCP_GATEWAY_URL="${MCP_GATEWAY_URL:-http://localhost:8080}"
MCP_API_KEY="${MCP_API_KEY:-}"
TIMEOUT=600
VERBOSE=false
INPUT_FILE=""
OUTPUT_FILE=""

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
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[VERBOSE]${NC} $1"
    fi
}

# Help function
show_help() {
    cat << EOF
MCP Streamable HTTP Client Example

USAGE:
    $0 [options]

OPTIONS:
    -u, --url URL          MCP Gateway URL (default: http://localhost:8080)
    -k, --api-key KEY      API key for authentication
    -f, --file FILE        File to upload/process
    -o, --output FILE      Output file for downloaded data
    -t, --timeout SECONDS  Request timeout (default: 600)
    -v, --verbose          Enable verbose output
    -h, --help             Show this help message

EXAMPLES:
    # Health check
    $0

    # Upload and process a file
    $0 -f document.pdf -o processed_document.json

    # Download large dataset
    $0 -o large_dataset.csv

    # Use custom gateway URL and API key
    $0 -u https://mcp.example.com -k your-api-key -f data.txt

ENVIRONMENT VARIABLES:
    MCP_GATEWAY_URL        Default gateway URL
    MCP_API_KEY           Default API key

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -u|--url)
                MCP_GATEWAY_URL="$2"
                shift 2
                ;;
            -k|--api-key)
                MCP_API_KEY="$2"
                shift 2
                ;;
            -f|--file)
                INPUT_FILE="$2"
                shift 2
                ;;
            -o|--output)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            -t|--timeout)
                TIMEOUT="$2"
                shift 2
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Check dependencies
check_dependencies() {
    local deps=("curl" "jq")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            log_error "Required dependency '$dep' is not installed"
            exit 1
        fi
    done
}

# Setup curl options
setup_curl_opts() {
    CURL_OPTS=(
        "--max-time" "$TIMEOUT"
        "--connect-timeout" "30"
        "--retry" "3"
        "--retry-delay" "5"
        "--fail"
        "--location"
        "--show-error"
    )
    
    if [[ "$VERBOSE" == "true" ]]; then
        CURL_OPTS+=("--verbose")
    else
        CURL_OPTS+=("--silent")
    fi
    
    if [[ -n "$MCP_API_KEY" ]]; then
        CURL_OPTS+=("--header" "Authorization: Bearer $MCP_API_KEY")
    fi
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    local response
    response=$(curl "${CURL_OPTS[@]}" \
        --header "Accept: application/json" \
        "$MCP_GATEWAY_URL/api/v1/streamable/health" 2>/dev/null)
    
    local status
    status=$(echo "$response" | jq -r '.status // "unknown"')
    
    if [[ "$status" == "healthy" ]]; then
        log_success "Streamable HTTP server is healthy"
        return 0
    else
        log_error "Streamable HTTP server health check failed: $status"
        return 1
    fi
}

# Upload and process file
upload_file() {
    local file="$1"
    
    if [[ ! -f "$file" ]]; then
        log_error "Input file does not exist: $file"
        return 1
    fi
    
    local file_size
    file_size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
    log_info "Uploading file: $file (${file_size} bytes)"
    
    local response
    response=$(curl "${CURL_OPTS[@]}" \
        --header "Content-Type: multipart/form-data" \
        --form "file=@$file" \
        --form "process=true" \
        --form "chunk_size=1048576" \
        "$MCP_GATEWAY_URL/api/v1/streamable/upload" 2>/dev/null)
    
    local upload_id
    upload_id=$(echo "$response" | jq -r '.upload_id // empty')
    
    if [[ -n "$upload_id" ]]; then
        log_success "File uploaded successfully. Upload ID: $upload_id"
        
        # Monitor processing status
        monitor_processing "$upload_id"
    else
        log_error "File upload failed"
        echo "$response" | jq '.' 2>/dev/null || echo "$response"
        return 1
    fi
}

# Monitor processing status
monitor_processing() {
    local upload_id="$1"
    log_info "Monitoring processing status for upload ID: $upload_id"
    
    local status="processing"
    local attempts=0
    local max_attempts=60  # 5 minutes with 5-second intervals
    
    while [[ "$status" == "processing" && $attempts -lt $max_attempts ]]; do
        sleep 5
        ((attempts++))
        
        local response
        response=$(curl "${CURL_OPTS[@]}" \
            --header "Accept: application/json" \
            "$MCP_GATEWAY_URL/api/v1/streamable/status/$upload_id" 2>/dev/null)
        
        status=$(echo "$response" | jq -r '.status // "unknown"')
        local progress
        progress=$(echo "$response" | jq -r '.progress // 0')
        
        log_verbose "Processing status: $status, Progress: ${progress}%"
        
        case "$status" in
            "completed")
                log_success "Processing completed successfully"
                
                # Download result if output file specified
                if [[ -n "$OUTPUT_FILE" ]]; then
                    download_result "$upload_id" "$OUTPUT_FILE"
                fi
                return 0
                ;;
            "failed")
                local error_msg
                error_msg=$(echo "$response" | jq -r '.error // "Unknown error"')
                log_error "Processing failed: $error_msg"
                return 1
                ;;
            "processing")
                # Continue monitoring
                ;;
            *)
                log_warning "Unknown status: $status"
                ;;
        esac
    done
    
    if [[ $attempts -ge $max_attempts ]]; then
        log_error "Processing timeout after $max_attempts attempts"
        return 1
    fi
}

# Download result
download_result() {
    local upload_id="$1"
    local output_file="$2"
    
    log_info "Downloading result to: $output_file"
    
    curl "${CURL_OPTS[@]}" \
        --header "Accept: application/octet-stream" \
        --output "$output_file" \
        "$MCP_GATEWAY_URL/api/v1/streamable/download/$upload_id"
    
    if [[ -f "$output_file" ]]; then
        local file_size
        file_size=$(stat -c%s "$output_file" 2>/dev/null || stat -f%z "$output_file" 2>/dev/null)
        log_success "Result downloaded successfully (${file_size} bytes)"
    else
        log_error "Failed to download result"
        return 1
    fi
}

# Stream large dataset
stream_dataset() {
    local output_file="$1"
    
    log_info "Streaming large dataset to: $output_file"
    
    # Start streaming request
    local stream_response
    stream_response=$(curl "${CURL_OPTS[@]}" \
        --header "Content-Type: application/json" \
        --header "Accept: application/json" \
        --data '{
            "dataset": "large_sample_data",
            "format": "csv",
            "compression": "gzip",
            "chunk_size": 1048576
        }' \
        "$MCP_GATEWAY_URL/api/v1/streamable/stream" 2>/dev/null)
    
    local stream_id
    stream_id=$(echo "$stream_response" | jq -r '.stream_id // empty')
    
    if [[ -n "$stream_id" ]]; then
        log_success "Stream started. Stream ID: $stream_id"
        
        # Download stream data
        curl "${CURL_OPTS[@]}" \
            --header "Accept: application/octet-stream" \
            --output "$output_file" \
            "$MCP_GATEWAY_URL/api/v1/streamable/stream/$stream_id/data"
        
        if [[ -f "$output_file" ]]; then
            local file_size
            file_size=$(stat -c%s "$output_file" 2>/dev/null || stat -f%z "$output_file" 2>/dev/null)
            log_success "Dataset streamed successfully (${file_size} bytes)"
        else
            log_error "Failed to stream dataset"
            return 1
        fi
    else
        log_error "Failed to start stream"
        echo "$stream_response" | jq '.' 2>/dev/null || echo "$stream_response"
        return 1
    fi
}

# Get server statistics
get_stats() {
    log_info "Retrieving server statistics..."
    
    local response
    response=$(curl "${CURL_OPTS[@]}" \
        --header "Accept: application/json" \
        "$MCP_GATEWAY_URL/api/v1/streamable/stats" 2>/dev/null)
    
    echo "$response" | jq '.' 2>/dev/null || echo "$response"
}

# List active streams
list_streams() {
    log_info "Listing active streams..."
    
    local response
    response=$(curl "${CURL_OPTS[@]}" \
        --header "Accept: application/json" \
        "$MCP_GATEWAY_URL/api/v1/streamable/streams" 2>/dev/null)
    
    echo "$response" | jq '.' 2>/dev/null || echo "$response"
}

# Main execution
main() {
    parse_args "$@"
    
    log_info "MCP Streamable HTTP Client"
    log_info "Gateway URL: $MCP_GATEWAY_URL"
    log_info "API Key: ${MCP_API_KEY:+Set}"
    log_info "Timeout: ${TIMEOUT}s"
    echo
    
    check_dependencies
    setup_curl_opts
    
    # Perform health check
    if ! health_check; then
        exit 1
    fi
    
    # Execute based on provided options
    if [[ -n "$INPUT_FILE" ]]; then
        # Upload and process file
        upload_file "$INPUT_FILE"
    elif [[ -n "$OUTPUT_FILE" ]]; then
        # Stream dataset to output file
        stream_dataset "$OUTPUT_FILE"
    else
        # Default actions: show stats and active streams
        echo
        get_stats
        echo
        list_streams
    fi
}

# Run main function with all arguments
main "$@"