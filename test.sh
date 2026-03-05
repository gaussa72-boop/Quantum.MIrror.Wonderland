#!/bin/bash
# 🌀 Quantum Mirror Wonderland - Test Script
# Testet alle Komponenten der App

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🌀 QUANTUM MIRROR WONDERLAND - SYSTEM TEST 🌀             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test Counter
PASSED=0
FAILED=0

# =================== TEST FUNCTIONS ===================

test_python_syntax() {
    echo -e "${YELLOW}[TEST 1/10] Python Syntax Check...${NC}"
    if python3 -m py_compile app.py 2>/dev/null; then
        echo -e "${GREEN}✅ app.py syntax OK${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ app.py syntax ERROR${NC}"
        ((FAILED++))
    fi
}

test_flask_imports() {
    echo -e "${YELLOW}[TEST 2/10] Flask Import Check...${NC}"
    if python3 -c "from app import app; print('Flask OK')" 2>/dev/null; then
        echo -e "${GREEN}✅ Flask imports OK${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ Flask import ERROR${NC}"
        ((FAILED++))
    fi
}

test_backend_imports() {
    echo -e "${YELLOW}[TEST 3/10] Backend Module Check...${NC}"
    if python3 -c "from backend.quantum_mirror_backend import QuantumMirrorBackend; print('Backend OK')" 2>/dev/null; then
        echo -e "${GREEN}✅ Backend module OK${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ Backend module ERROR${NC}"
        ((FAILED++))
    fi
}

test_html_exists() {
    echo -e "${YELLOW}[TEST 4/10] HTML File Check...${NC}"
    if [ -f "web/index.html" ]; then
        echo -e "${GREEN}✅ index.html exists${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ index.html missing${NC}"
        ((FAILED++))
    fi
}

test_js_files() {
    echo -e "${YELLOW}[TEST 5/10] JavaScript Files Check...${NC}"
    JS_FILES=("mirror_world.js" "companion_widget.js" "chat.js" "meta_geometry.js" "user_avatar.js")
    local js_ok=0
    for file in "${JS_FILES[@]}"; do
        if [ -f "web/$file" ]; then
            ((js_ok++))
        fi
    done
    if [ $js_ok -eq 5 ]; then
        echo -e "${GREEN}✅ All 5 JS files present${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ Missing JS files ($js_ok/5)${NC}"
        ((FAILED++))
    fi
}

test_css_exists() {
    echo -e "${YELLOW}[TEST 6/10] CSS File Check...${NC}"
    if [ -f "web/style.css" ] && grep -q "mirror-button" web/style.css; then
        echo -e "${GREEN}✅ CSS file OK${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ CSS file missing or incomplete${NC}"
        ((FAILED++))
    fi
}

test_requirements() {
    echo -e "${YELLOW}[TEST 7/10] Requirements Check...${NC}"
    if grep -q "Flask" backend/requirements.txt && grep -q "gunicorn" backend/requirements.txt; then
        echo -e "${GREEN}✅ Requirements OK${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ Requirements incomplete${NC}"
        ((FAILED++))
    fi
}

test_docker_config() {
    echo -e "${YELLOW}[TEST 8/10] Docker Config Check...${NC}"
    if [ -f "Dockerfile" ] && [ -f "docker-compose.yml" ]; then
        echo -e "${GREEN}✅ Docker config present${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ Docker config missing${NC}"
        ((FAILED++))
    fi
}

test_render_config() {
    echo -e "${YELLOW}[TEST 9/10] Render Config Check...${NC}"
    if [ -f "render.yaml" ] && [ -f "Procfile" ]; then
        echo -e "${GREEN}✅ Render config ready${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ Render config incomplete${NC}"
        ((FAILED++))
    fi
}

test_documentation() {
    echo -e "${YELLOW}[TEST 10/10] Documentation Check...${NC}"
    DOCS=("README.md" "QUICK_START.md" "GITHUB_RENDER_SETUP.md")
    local doc_count=0
    for doc in "${DOCS[@]}"; do
        if [ -f "$doc" ]; then
            ((doc_count++))
        fi
    done
    if [ $doc_count -eq 3 ]; then
        echo -e "${GREEN}✅ Documentation complete${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ Documentation incomplete ($doc_count/3)${NC}"
        ((FAILED++))
    fi
}

# =================== RUN TESTS ===================

echo "🧪 Running System Tests..."
echo ""

test_python_syntax
test_flask_imports
test_backend_imports
test_html_exists
test_js_files
test_css_exists
test_requirements
test_docker_config
test_render_config
test_documentation

# =================== RESULTS ===================

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                      TEST RESULTS                             ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo -e "║ ${GREEN}✅ PASSED: $PASSED${NC}"
echo -e "║ ${RED}❌ FAILED: $FAILED${NC}"
echo "╠════════════════════════════════════════════════════════════════╣"

if [ $FAILED -eq 0 ]; then
    echo -e "║ ${GREEN}🎉 ALL TESTS PASSED - APP IS READY! 🎉${NC}"
else
    echo -e "║ ${RED}⚠️  Some tests failed - check above${NC}"
fi

echo "╚════════════════════════════════════════════════════════════════╝"

# =================== NEXT STEPS ===================

echo ""
echo "📋 NEXT STEPS:"
echo "  1. Start locally: python app.py"
echo "  2. Open browser: http://localhost:5000"
echo "  3. Or open web/index.html directly"
echo ""
echo "🌍 Deploy to Render:"
echo "  1. Create GitHub repo"
echo "  2. Push this code"
echo "  3. Follow: GITHUB_RENDER_SETUP.md"
echo ""

exit $FAILED

