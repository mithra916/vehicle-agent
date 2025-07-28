import pandas as pd
from agent.vehicle_test_agent import VehicleTestAgent
from agent.pdf_report_generator import generate_pdf_report

# 🔹 Load your vehicle sensor data
data_path = 'data/dataset.csv'
df = pd.read_csv(data_path)

# 🔹 Create and run the Vehicle Test Agent
agent = VehicleTestAgent(df)
results, health_score = agent.run_all_tests()

# 🔹 Assign test priorities based on type of failure
for result in results:
    if result['result'] == '❌ Failed':
        result['priority'] = 'Medium'
    elif result['result'] == '⚠️ Not Implemented':
        result['priority'] = 'Medium'
    else:
        result['priority'] = None

# 🔹 Print results to console
for r in results:
    print(f"--- {r['test']} ---")
    print(f"{r['result']}  Priority: {r['priority']}")
    if r['reason']:
        print(f"Reason: {r['reason']}")
    if r['suggestion']:
        print(f"Suggestion: {r['suggestion']}")
    print()

# 🔹 Generate PDF Report
generate_pdf_report(results, health_score)
