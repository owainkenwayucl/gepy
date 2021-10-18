def run(command):
    import subprocess
    return subprocess.run(command, capture_output=True, encoding='UTF-8')
    