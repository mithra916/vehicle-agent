import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class VehicleTestAgent:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.results = []
        self.health_score = 100
        self.vehicle_type = self.detect_fuel_type()

    def detect_fuel_type(self):
        if 'battery_voltage' in self.data.columns or 'ev_flag' in self.data.columns:
            return 'EV'
        elif 'fuel_consumed' in self.data.columns or 'fuel_type' in self.data.columns:
            return 'Fuel'
        return 'Unknown'

    def run_all_tests(self):
        self.braking_test()
        self.acceleration_test()
        self.stability_test()
        self.speed_test()
        self.suspension_test()
        self.cornering_test()
        self.torque_test()
        self.efficiency_test()
        self.calculate_health_score()
        return self.results, self.health_score

    def record_result(self, test_name, passed, reason=None, suggestion=None):
        self.results.append({
            'test': test_name,
            'result': '✅ Passed' if passed else ('⚠️ Not Implemented' if passed is None else '❌ Failed'),
            'priority': self.get_priority(passed),
            'reason': reason if not passed else None,
            'suggestion': suggestion if not passed else None
        })

    def get_priority(self, passed):
        if passed is None or passed is False:
            return "Medium"
        return None

    def braking_test(self):
        std = self.data['gFx'].std()
        self.record_result("Braking Test", std > 0.03,
            "Braking force too consistent – possible malfunction",
            "Check braking system for response lag or sensor error")

    def acceleration_test(self):
        std = self.data['gFy'].std()
        self.record_result("Acceleration Test", std > 0.03,
            "Low acceleration variance, possible sluggishness",
            "Check throttle, fuel injectors, or engine power")

    def stability_test(self):
        std = self.data['wy'].std()
        self.record_result("Stability Test", std < 0.05,
            "High yaw rate variance, unstable turning",
            "Check suspension, steering response")

    def speed_test(self):
        mean = self.data['speed'].mean()
        self.record_result("Speed Test", mean > 1.5,
            "Low average speed — performance issue suspected",
            "Inspect drivetrain, acceleration system")

    def suspension_test(self):
        std = self.data['gFz'].std()
        self.record_result("Suspension Test", std > 0.01,
            "Suspension travel too minimal",
            "Inspect shock absorbers and suspension setup")

    def cornering_test(self):
        mean = self.data['gFz'].mean()
        self.record_result("Cornering Grip Test", mean > 0.9,
            "Low lateral force, poor cornering grip",
            "Check tires, suspension stiffness")

    def torque_test(self):
        delta_speed = self.data['speed'].max() - self.data['speed'].min()
        self.record_result("Torque Test", delta_speed > 3,
            "Insufficient speed change under test",
            "Inspect torque delivery, transmission")

    def efficiency_test(self):
        if self.vehicle_type == 'Fuel':
            if 'fuel_consumed' in self.data.columns and 'distance' in self.data.columns:
                efficiency = self.data['distance'].sum() / self.data['fuel_consumed'].sum()
                self.record_result("Fuel Efficiency Test", efficiency > 10,
                    f"Low efficiency: {efficiency:.2f} km/l",
                    "Inspect fuel system")
            else:
                self.record_result("Fuel Efficiency Test", None,
                    "Fuel consumption data missing",
                    "Include fuel usage logs or distance/time data")
        elif self.vehicle_type == 'EV':
            if 'battery_used' in self.data.columns and 'distance' in self.data.columns:
                efficiency = self.data['distance'].sum() / self.data['battery_used'].sum()
                self.record_result("Battery Efficiency Test", efficiency > 5,
                    f"Low battery efficiency: {efficiency:.2f} km/kWh",
                    "Inspect battery health")
            else:
                self.record_result("Battery Efficiency Test", None,
                    "Battery usage data missing",
                    "Include battery usage logs or distance/time data")
        else:
            self.record_result("Efficiency Test", None,
                "Unknown fuel type",
                "Cannot evaluate efficiency without knowing fuel type")

    def calculate_health_score(self):
        total = sum(1 for r in self.results if r['result'] in ['✅ Passed', '❌ Failed'])
        failed = sum(1 for r in self.results if r['result'] == '❌ Failed')
        self.health_score = int(100 - (failed / total) * 100) if total > 0 else 0

    def visualize_metrics(self):
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=self.data[['speed', 'gFx', 'gFy', 'gFz']])
        plt.title("Vehicle Performance Trends")
        plt.xlabel("Time Index")
        plt.ylabel("Sensor Readings")
        plt.legend(['Speed', 'Braking (gFx)', 'Acceleration (gFy)', 'Lateral Force (gFz)'])
        plt.grid(True)
        plt.tight_layout()
        plt.show()
