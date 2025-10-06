#!/bin/bash

# ShadowRecon v1.0 Installation Script
# Developed by kernelpanic | A product of infosbios
# "In the shadows, we prepare for the hunt..."

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Shadow banner
echo -e "${PURPLE}"
echo "🎭 ============================================================== 🎭"
echo "   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗"
echo "   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║"
echo "   ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║"
echo "   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║"
echo "   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝"
echo "   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝"
echo "   ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗"  
echo "   ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║"
echo "   ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║"
echo "   ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║"
echo "   ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║"
echo "   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝"
echo ""
echo "   Ultimate Web Attack Surface Discovery Framework v1.0"
echo "   'In the shadows, we find the truth. In reconnaissance, we find power.'"
echo ""
echo "   Developed by kernelpanic | A product of infosbios"
echo "🎭 ============================================================== 🎭"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${YELLOW}⚠️  Running as root detected. This is recommended for system-wide installation.${NC}"
   INSTALL_GLOBAL=true
else
   echo -e "${BLUE}ℹ️  Running as regular user. Installing for current user only.${NC}"
   INSTALL_GLOBAL=false
fi

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check system requirements
print_status "🔍 Checking system requirements..."

# Check Python 3.8+
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    PYTHON_VERSION_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_VERSION_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [[ $PYTHON_VERSION_MAJOR -ge 3 ]] && [[ $PYTHON_VERSION_MINOR -ge 8 ]]; then
        print_success "Python $PYTHON_VERSION found ✓"
    else
        print_error "Python 3.8+ required. Found: $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    print_success "pip3 found ✓"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    print_success "pip found ✓"
    PIP_CMD="pip"
else
    print_error "pip not found. Please install pip first."
    exit 1
fi

# Install Python dependencies
print_status "📦 Installing Python dependencies..."

if [[ $INSTALL_GLOBAL == true ]]; then
    $PIP_CMD install -r requirements.txt --break-system-packages 2>/dev/null || $PIP_CMD install -r requirements.txt
else
    $PIP_CMD install -r requirements.txt --user
fi

if [[ $? -eq 0 ]]; then
    print_success "Python dependencies installed ✓"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Create symbolic link for global access
if [[ $INSTALL_GLOBAL == true ]]; then
    print_status "🔗 Creating global shadowrecon command..."

    SHADOWRECON_PATH=$(pwd)/shadowrecon.py

    # Make executable
    chmod +x "$SHADOWRECON_PATH"

    # Create symbolic link
    if ln -sf "$SHADOWRECON_PATH" /usr/local/bin/shadowrecon 2>/dev/null; then
        print_success "Global shadowrecon command created ✓"
    else
        print_warning "Could not create global command. You can run: python3 $(pwd)/shadowrecon.py"
    fi
else
    print_status "🔗 Setting up user-local access..."
    chmod +x shadowrecon.py

    # Add to user PATH if not already there
    USER_BIN="$HOME/.local/bin"
    mkdir -p "$USER_BIN"

    if ln -sf "$(pwd)/shadowrecon.py" "$USER_BIN/shadowrecon" 2>/dev/null; then
        print_success "Local shadowrecon command created ✓"

        # Check if ~/.local/bin is in PATH
        if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
            print_warning "Add $USER_BIN to your PATH to use 'shadowrecon' command globally"
            echo "Add this line to your ~/.bashrc or ~/.zshrc:"
            echo "export PATH=\$PATH:$USER_BIN"
        fi
    else
        print_warning "Could not create local command. You can run: python3 $(pwd)/shadowrecon.py"
    fi
fi

# Create output directory
print_status "📁 Creating output directory..."
mkdir -p ./shadowrecon_output
print_success "Output directory created ✓"

# Install optional external tools (if available)
print_status "🛠️  Checking for optional external tools..."

check_tool() {
    if command -v $1 &> /dev/null; then
        print_success "$1 found ✓"
        return 0
    else
        print_warning "$1 not found (optional)"
        return 1
    fi
}

# Check external tools
check_tool "nuclei"
check_tool "subfinder"  
check_tool "ffuf"
check_tool "sqlmap"
check_tool "nmap"
check_tool "gobuster"
check_tool "curl"

# System-specific installations
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_status "🐧 Linux detected - checking for additional tools..."

    if command -v apt-get &> /dev/null; then
        print_status "📦 Debian/Ubuntu detected. You can install additional tools with:"
        echo "sudo apt-get update"
        echo "sudo apt-get install nmap curl dnsutils"
    elif command -v yum &> /dev/null; then
        print_status "📦 RedHat/CentOS detected. You can install additional tools with:"
        echo "sudo yum install nmap curl bind-utils"
    elif command -v pacman &> /dev/null; then
        print_status "📦 Arch detected. You can install additional tools with:"
        echo "sudo pacman -S nmap curl bind-tools"
    fi

elif [[ "$OSTYPE" == "darwin"* ]]; then
    print_status "🍎 macOS detected"
    if command -v brew &> /dev/null; then
        print_status "🍺 Homebrew detected. You can install additional tools with:"
        echo "brew install nmap curl"
    else
        print_status "Consider installing Homebrew for additional tools: https://brew.sh"
    fi
fi

# Test installation
print_status "🧪 Testing ShadowRecon installation..."

if python3 shadowrecon.py --version &> /dev/null; then
    print_success "ShadowRecon installation test passed ✓"
else
    print_error "Installation test failed"
    exit 1
fi

# Installation complete
echo ""
echo -e "${PURPLE}🎭 ============================================================== 🎭${NC}"
echo -e "${GREEN}✅ SHADOWRECON v1.0 INSTALLATION COMPLETE! ✅${NC}"
echo -e "${PURPLE}🎭 ============================================================== 🎭${NC}"
echo ""
echo -e "${CYAN}🚀 QUICK START:${NC}"
echo "   Basic scan:     shadowrecon -d example.com"
echo "   Deep scan:      shadowrecon -d example.com --deep --crawl --inject"
echo "   Multiple scans: shadowrecon -l targets.txt --threads 200"
echo ""
echo -e "${CYAN}📊 OUTPUT:${NC}"
echo "   Reports will be saved to: ./shadowrecon_output/"
echo "   Formats: HTML (interactive), JSON (machine-readable), CSV (spreadsheet)"
echo ""
echo -e "${CYAN}🔧 ADVANCED USAGE:${NC}"
echo "   With external tools: shadowrecon -d target.com --nuclei --subfinder --ffuf"
echo "   Custom payloads:     shadowrecon -d target.com --payloads xss,lfi,ssrf,sqli"
echo "   Verbose mode:        shadowrecon -d target.com --verbose"
echo ""
echo -e "${PURPLE}💀 'In the shadows, the hunt begins. The framework is ready.'${NC}"
echo -e "${PURPLE}🎭 Developed by kernelpanic | A product of infosbios${NC}"
echo ""

# Final instructions
if [[ $INSTALL_GLOBAL == true ]]; then
    echo -e "${GREEN}Global installation complete! Use 'shadowrecon' command from anywhere.${NC}"
else
    echo -e "${BLUE}User installation complete! Use 'python3 shadowrecon.py' or add ~/.local/bin to PATH.${NC}"
fi

echo -e "${YELLOW}📖 For full documentation, visit: https://github.com/infosbios/shadowrecon${NC}"
echo -e "${YELLOW}🐛 Report issues at: https://github.com/infosbios/shadowrecon/issues${NC}"
echo ""
