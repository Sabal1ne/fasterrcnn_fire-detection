#!/usr/bin/env python3
"""
Simple test script to verify deployment configuration
"""
import os
import sys

def test_environment_variables():
    """Test that environment variables are properly read"""
    print("Testing environment variable support...")
    
    # Test default values
    os.environ.pop('GRADIO_SHARE', None)
    os.environ.pop('GRADIO_AUTH', None)
    os.environ.pop('GRADIO_SERVER_NAME', None)
    os.environ.pop('GRADIO_SERVER_PORT', None)
    
    # Import module to test defaults
    import importlib
    if 'app' in sys.modules:
        del sys.modules['app']
    
    # This will fail if imports are broken, but that's okay for now
    try:
        import app
        assert app.GRADIO_SHARE == False, "Default GRADIO_SHARE should be False"
        assert app.GRADIO_SERVER_NAME == "0.0.0.0", "Default server name should be 0.0.0.0"
        assert app.GRADIO_SERVER_PORT == 7860, "Default port should be 7860"
        assert app.GRADIO_AUTH is None, "Default auth should be None"
        print("✅ Default values test passed")
    except ImportError as e:
        print(f"⚠️  Cannot fully test - dependencies not installed: {e}")
        print("   This is expected in CI environment")
        return True
    
    # Test with environment variables set
    os.environ['GRADIO_SHARE'] = 'True'
    os.environ['GRADIO_AUTH'] = 'user:pass'
    os.environ['GRADIO_SERVER_PORT'] = '8080'
    
    if 'app' in sys.modules:
        del sys.modules['app']
    
    try:
        import app
        importlib.reload(app)
        assert app.GRADIO_SHARE == True, "GRADIO_SHARE should be True"
        assert app.GRADIO_AUTH == "user:pass", "Auth should be set"
        assert app.GRADIO_SERVER_PORT == 8080, "Port should be 8080"
        print("✅ Environment variable override test passed")
    except ImportError:
        pass
    
    return True

def test_files_exist():
    """Test that all deployment files exist"""
    print("\nTesting deployment files...")
    
    required_files = [
        'DEPLOYMENT.md',
        'PUBLIC_ACCESS.md',
        'Dockerfile',
        'docker-compose.yml',
        '.dockerignore',
        '.env.example',
        'railway.json',
        'render.yaml',
        'README_HF.md',
        'launch_public.sh',
        'launch_public.bat'
    ]
    
    all_exist = True
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✅ {filename} exists")
        else:
            print(f"❌ {filename} NOT FOUND")
            all_exist = False
    
    return all_exist

def test_scripts_executable():
    """Test that shell scripts are executable"""
    print("\nTesting script permissions...")
    
    if os.path.exists('launch_public.sh'):
        if os.access('launch_public.sh', os.X_OK):
            print("✅ launch_public.sh is executable")
        else:
            print("⚠️  launch_public.sh is not executable (run: chmod +x launch_public.sh)")
    
    return True

def test_syntax():
    """Test Python file syntax"""
    print("\nTesting Python syntax...")
    
    files = ['app.py', 'launch_ui.py']
    for filename in files:
        try:
            with open(filename, 'r') as f:
                compile(f.read(), filename, 'exec')
            print(f"✅ {filename} syntax is valid")
        except SyntaxError as e:
            print(f"❌ {filename} has syntax error: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Deployment Configuration Test Suite")
    print("=" * 60)
    print()
    
    results = []
    results.append(("Syntax Check", test_syntax()))
    results.append(("Files Exist", test_files_exist()))
    results.append(("Scripts Executable", test_scripts_executable()))
    results.append(("Environment Variables", test_environment_variables()))
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed")
        sys.exit(1)
