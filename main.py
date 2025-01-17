from app.src.application import App

APP = None

def launch_app():
    global APP
    APP = App("Chaotic Cryptography Simulation")

if __name__ == "__main__":
    print("\n\n\nRunning Chaotic Cryptography Simulation\n\n-----------------------------\n\nCreated by Hugo, Nicolas, Théodore\n\n")

    # Window setup
    launch_app()
