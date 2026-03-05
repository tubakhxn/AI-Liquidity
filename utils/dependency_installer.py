import subprocess
import sys
import pkg_resources

REQUIRED_PACKAGES = [
    "numpy", "pandas", "plotly", "dash", "scikit-learn", "torch", "numba"
]

def install_dependencies():
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = [pkg for pkg in REQUIRED_PACKAGES if pkg.lower() not in installed]
    if missing:
        print(f"Installing missing packages: {missing}")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
