# Live decision graph animation (basic)
import time

def show_decision_flow(steps):
    for step in steps:
        print(">>", step)
        time.sleep(0.5)
