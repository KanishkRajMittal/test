import schedule
import time
import subprocess

def run_my_script():
    subprocess.run(["python3", "potd.py"])

# Schedule the script to run every 2 minutes
schedule.every(2).minutes.do(run_my_script)

while True:
    schedule.run_pending()
    time.sleep(1)
