import os
import sys
import subprocess


def install_packages():
    """Install required packages from requirements.txt"""
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"{requirements_file} not found.")
        sys.exit(1)
    try:
        with open(requirements_file, "r") as f:
            required_packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        for package in required_packages:
            package_name = package.split("~")[0].split("=")[0]
            try:
                __import__(package_name)
            except ImportError:
                print(f"{package_name} is not installed. Installing...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Error installing packages: {e}")
        sys.exit(1)
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

def launch_app():
    """Launch the application"""
    from app.src.application import App
    app = App("Chaotic Cryptography Simulation")

if __name__ == "__main__":
    print("\n\n\nRunning Chaotic Cryptography Simulation\n\n-----------------------------\n\nCreated by Hugo, Nicolas, Théodore\n\n")
    install_packages()
    print("\n\nLibraries installed, launching app\n\n")
    # Window setup
    launch_app()
