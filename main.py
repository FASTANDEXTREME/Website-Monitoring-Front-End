import subprocess

def run_script(script_name):
    try:
        subprocess.Popen(['python', script_name])
        print(f"{script_name} is running.")
    except Exception as e:
        print(f"Error running {script_name}: {e}")

if __name__ == '__main__':
    scripts = ['graph.py', 'app.py', 'sapps.py']

    for script in scripts:
        run_script(script)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping all scripts.")