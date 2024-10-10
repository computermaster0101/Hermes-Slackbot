import subprocess

def restart_computer():
    try:
        # Restart the computer
        subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    restart_computer()
