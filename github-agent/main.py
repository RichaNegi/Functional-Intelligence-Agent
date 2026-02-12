from agents.planner_agent import PlannerAgent
 
def main():
 
    agent = PlannerAgent()
 
    result = agent.analyze(
        "https://github.com/Sachittarway/FSAD-Employee-Management-System"
    )
 
    print(result)
 
 
if __name__ == "__main__":
    main()