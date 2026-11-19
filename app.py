import os
import sys

# Absolute path to the isolated, properly-configured virtual environment Python
current_dir = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(current_dir, ".venv", "Scripts", "python.exe")
inner_app_dir = os.path.join(current_dir, "Automated-Topic-Extraction-and-Learning-Resource-Summary-Generator-main")
inner_app_file = os.path.join(inner_app_dir, "app.py")

# If user invoked using global Python, automatically re-exec using .venv Python
if os.path.exists(venv_python) and os.path.normcase(sys.executable) != os.path.normcase(venv_python):
    import subprocess
    print("⚡ Auto-switching to project virtual environment (.venv)...")
    result = subprocess.run([venv_python, inner_app_file], cwd=inner_app_dir)
    sys.exit(result.returncode)

# Switch working directory to inner folder so paths work seamlessly
os.chdir(inner_app_dir)
sys.path.insert(0, inner_app_dir)

if __name__ == "__main__":
    with open(inner_app_file, "r", encoding="utf-8") as f:
        code = f.read()
    exec(compile(code, inner_app_file, 'exec'))
