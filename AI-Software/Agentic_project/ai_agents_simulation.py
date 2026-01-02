"""
AI Agents Simulation for AutoParts Inc. Smart Manufacturing
Demonstrates the three core agents: QCIA, PMA, and WOA

This simulation shows how AI agents work together to optimize
manufacturing operations, quality control, and workforce management.
"""

import random
import time
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np

@dataclass
class SensorData:
    """Data structure for manufacturing sensor readings"""
    timestamp: datetime
    production_line: str
    quality_metrics: Dict[str, float]
    machine_health: Dict[str, float]
    workforce: Dict[str, any]

@dataclass
class AgentDecision:
    """Data structure for agent decisions"""
    agent_type: str
    timestamp: datetime
    action: str
    priority: str
    message: str
    confidence: float
    metrics: Dict[str, any]

class QualityControlIntelligenceAgent:
    """AI Agent for real-time quality control and defect detection"""
    
    def __init__(self):
        self.name = "Quality Control Intelligence Agent (QCIA)"
        self.defect_threshold = 0.7
        self.inspection_threshold = 0.4
        self.decisions_made = 0
        self.alerts_triggered = 0
        
    def analyze_quality(self, sensor_data: SensorData) -> AgentDecision:
        """Analyze quality metrics and make decisions"""
        quality = sensor_data.quality_metrics
        defect_probability = quality['defect_probability']
        surface_quality = quality['surface_quality']
        dimensional_accuracy = quality['dimensional_accuracy']
        
        # Calculate overall quality score
        quality_score = (
            (1 - defect_probability) * 0.4 +
            (surface_quality / 100) * 0.3 +
            (dimensional_accuracy / 100) * 0.3
        )
        
        # Make decision based on quality metrics
        if defect_probability > self.defect_threshold or surface_quality < 80:
            action = "immediate_alert"
            priority = "critical"
            message = f"CRITICAL: High defect risk detected ({defect_probability:.1%}). Stop production for inspection."
            confidence = 0.95
            self.alerts_triggered += 1
        elif defect_probability > self.inspection_threshold or surface_quality < 90:
            action = "enhanced_inspection"
            priority = "medium"
            message = f"CAUTION: Elevated defect risk ({defect_probability:.1%}). Enhanced quality checks recommended."
            confidence = 0.80
        else:
            action = "continue_production"
            priority = "low"
            message = f"NORMAL: Quality within acceptable range ({defect_probability:.1%} defect probability)."
            confidence = 0.75
        
        self.decisions_made += 1
        
        return AgentDecision(
            agent_type="QCIA",
            timestamp=sensor_data.timestamp,
            action=action,
            priority=priority,
            message=message,
            confidence=confidence,
            metrics={
                "defect_probability": defect_probability,
                "surface_quality": surface_quality,
                "dimensional_accuracy": dimensional_accuracy,
                "quality_score": quality_score
            }
        )

class PredictiveMaintenanceAgent:
    """AI Agent for predictive equipment maintenance"""
    
    def __init__(self):
        self.name = "Predictive Maintenance Agent (PMA)"
        self.critical_thresholds = {
            'temperature': 90,
            'vibration': 8,
            'efficiency': 70,
            'pressure': 120
        }
        self.decisions_made = 0
        self.maintenance_scheduled = 0
        
    def predict_maintenance_needs(self, sensor_data: SensorData) -> AgentDecision:
        """Predict maintenance needs based on machine health data"""
        health = sensor_data.machine_health
        
        # Calculate risk factors
        temp_risk = max(0, (health['temperature'] - 70) / 30)
        vibration_risk = health['vibration'] / 10
        efficiency_risk = max(0, (90 - health['efficiency']) / 20)
        pressure_risk = max(0, (health['pressure'] - 100) / 30)
        
        # Overall health score
        health_score = 1 - (temp_risk + vibration_risk + efficiency_risk + pressure_risk) / 4
        health_score = max(0, min(1, health_score))
        
        # Estimate time to failure
        if health_score < 0.3:
            time_to_failure = "< 4 hours"
            action = "immediate_maintenance"
            priority = "critical"
            message = f"CRITICAL: Equipment failure imminent. Health score: {health_score:.2f}"
            confidence = 0.90
            self.maintenance_scheduled += 1
        elif health_score < 0.6:
            time_to_failure = "24-48 hours"
            action = "schedule_maintenance"
            priority = "medium"
            message = f"SCHEDULE: Preventive maintenance recommended. Health score: {health_score:.2f}"
            confidence = 0.75
            self.maintenance_scheduled += 1
        else:
            time_to_failure = "> 1 week"
            action = "continue_monitoring"
            priority = "low"
            message = f"NORMAL: Equipment operating normally. Health score: {health_score:.2f}"
            confidence = 0.70
        
        self.decisions_made += 1
        
        return AgentDecision(
            agent_type="PMA",
            timestamp=sensor_data.timestamp,
            action=action,
            priority=priority,
            message=message,
            confidence=confidence,
            metrics={
                "health_score": health_score,
                "time_to_failure": time_to_failure,
                "temperature": health['temperature'],
                "vibration": health['vibration'],
                "efficiency": health['efficiency'],
                "pressure": health['pressure']
            }
        )

class WorkforceOptimizationAgent:
    """AI Agent for workforce allocation and optimization"""
    
    def __init__(self):
        self.name = "Workforce Optimization Agent (WOA)"
        self.production_target = 100
        self.skill_weights = {'expert': 3, 'intermediate': 2, 'novice': 1}
        self.decisions_made = 0
        self.optimizations_made = 0
        
    def optimize_workforce(self, sensor_data: SensorData) -> AgentDecision:
        """Optimize workforce allocation based on production needs"""
        workforce = sensor_data.workforce
        
        # Calculate workforce efficiency
        total_skill_points = sum(
            count * self.skill_weights[skill] 
            for skill, count in workforce['skill_levels'].items()
        )
        
        max_possible_skill = workforce['available_workers'] * self.skill_weights['expert']
        skill_efficiency = total_skill_points / max_possible_skill if max_possible_skill > 0 else 0
        
        current_rate = workforce['current_production_rate']
        efficiency_gap = self.production_target - current_rate
        
        # Calculate overall workforce score
        workforce_score = (skill_efficiency + (current_rate / 100)) / 2
        
        # Make optimization decision
        if efficiency_gap > 15:
            action = "major_optimization"
            priority = "high"
            message = f"OPTIMIZE: Significant efficiency gap ({efficiency_gap:.1f}%). Deploy expert workers to critical stations."
            confidence = 0.85
            self.optimizations_made += 1
            recommendations = [
                "Deploy 2-3 expert workers to bottleneck stations",
                "Implement real-time AR guidance for novice workers",
                "Redistribute intermediate workers to support areas"
            ]
        elif efficiency_gap > 5:
            action = "minor_adjustment"
            priority = "medium"
            message = f"ADJUST: Minor efficiency gap ({efficiency_gap:.1f}%). Skill reallocation recommended."
            confidence = 0.75
            recommendations = [
                "Redistribute intermediate workers to high-demand areas",
                "Pair novice workers with experienced mentors",
                "Optimize break schedules to maintain coverage"
            ]
        else:
            action = "maintain_allocation"
            priority = "low"
            message = f"OPTIMAL: Workforce allocation efficient. Current rate: {current_rate:.1f}%"
            confidence = 0.70
            recommendations = [
                "Continue current allocation",
                "Monitor for continuous improvement opportunities",
                "Prepare for next shift transition"
            ]
        
        self.decisions_made += 1
        
        return AgentDecision(
            agent_type="WOA",
            timestamp=sensor_data.timestamp,
            action=action,
            priority=priority,
            message=message,
            confidence=confidence,
            metrics={
                "workforce_score": workforce_score,
                "efficiency_gap": efficiency_gap,
                "skill_efficiency": skill_efficiency,
                "current_production_rate": current_rate,
                "recommendations": recommendations
            }
        )

class ManufacturingSimulator:
    """Simulates manufacturing environment and AI agent interactions"""
    
    def __init__(self):
        self.qcia = QualityControlIntelligenceAgent()
        self.pma = PredictiveMaintenanceAgent()
        self.woa = WorkforceOptimizationAgent()
        
        self.simulation_data = []
        self.agent_decisions = []
        self.performance_metrics = {
            'defect_rate': [],
            'equipment_uptime': [],
            'production_efficiency': [],
            'cost_savings': []
        }
        
    def generate_sensor_data(self, timestamp: datetime, scenario: str = "normal") -> SensorData:
        """Generate realistic sensor data based on scenario"""
        
        if scenario == "quality_issue":
            # Simulate quality problems
            defect_prob = random.uniform(0.6, 0.9)
            surface_quality = random.uniform(60, 85)
            dimensional_accuracy = random.uniform(85, 95)
        elif scenario == "maintenance_needed":
            # Simulate equipment degradation
            defect_prob = random.uniform(0.2, 0.5)
            surface_quality = random.uniform(85, 95)
            dimensional_accuracy = random.uniform(90, 98)
        else:
            # Normal operation
            defect_prob = random.uniform(0.05, 0.3)
            surface_quality = random.uniform(90, 99)
            dimensional_accuracy = random.uniform(95, 99.5)
        
        # Machine health varies based on scenario
        if scenario == "maintenance_needed":
            temperature = random.uniform(85, 95)
            vibration = random.uniform(6, 9)
            efficiency = random.uniform(65, 80)
            pressure = random.uniform(110, 125)
        else:
            temperature = random.uniform(70, 85)
            vibration = random.uniform(2, 6)
            efficiency = random.uniform(80, 95)
            pressure = random.uniform(95, 110)
        
        # Workforce data
        available_workers = random.randint(15, 25)
        expert_workers = random.randint(2, 6)
        intermediate_workers = random.randint(8, 12)
        novice_workers = available_workers - expert_workers - intermediate_workers
        
        production_rate = random.uniform(75, 100) if scenario == "normal" else random.uniform(60, 85)
        
        return SensorData(
            timestamp=timestamp,
            production_line="Line_A",
            quality_metrics={
                'defect_probability': defect_prob,
                'surface_quality': surface_quality,
                'dimensional_accuracy': dimensional_accuracy
            },
            machine_health={
                'temperature': temperature,
                'vibration': vibration,
                'efficiency': efficiency,
                'pressure': pressure
            },
            workforce={
                'available_workers': available_workers,
                'skill_levels': {
                    'expert': expert_workers,
                    'intermediate': intermediate_workers,
                    'novice': novice_workers
                },
                'current_production_rate': production_rate
            }
        )
    
    def run_simulation(self, duration_hours: int = 24, interval_minutes: int = 5):
        """Run the manufacturing simulation"""
        print(f"Starting AI Agents Manufacturing Simulation")
        print(f"Duration: {duration_hours} hours, Interval: {interval_minutes} minutes")
        print("=" * 60)
        
        start_time = datetime.now()
        current_time = start_time
        end_time = start_time + timedelta(hours=duration_hours)
        
        cycle_count = 0
        
        while current_time < end_time:
            cycle_count += 1
            
            # Determine scenario based on random events
            scenario_roll = random.random()
            if scenario_roll < 0.1:
                scenario = "quality_issue"
            elif scenario_roll < 0.2:
                scenario = "maintenance_needed"
            else:
                scenario = "normal"
            
            # Generate sensor data
            sensor_data = self.generate_sensor_data(current_time, scenario)
            self.simulation_data.append(sensor_data)
            
            # Get decisions from all agents
            qcia_decision = self.qcia.analyze_quality(sensor_data)
            pma_decision = self.pma.predict_maintenance_needs(sensor_data)
            woa_decision = self.woa.optimize_workforce(sensor_data)
            
            # Store decisions
            self.agent_decisions.extend([qcia_decision, pma_decision, woa_decision])
            
            # Calculate performance metrics
            self._update_performance_metrics(sensor_data, [qcia_decision, pma_decision, woa_decision])
            
            # Print status every hour
            if cycle_count % (60 // interval_minutes) == 0:
                hours_elapsed = (current_time - start_time).total_seconds() / 3600
                print(f"Hour {hours_elapsed:.0f}: Processed {cycle_count} cycles")
                print(f"  QCIA: {qcia_decision.action} ({qcia_decision.priority})")
                print(f"  PMA: {pma_decision.action} ({pma_decision.priority})")
                print(f"  WOA: {woa_decision.action} ({woa_decision.priority})")
                print()
            
            # Advance time
            current_time += timedelta(minutes=interval_minutes)
        
        print(f"Simulation completed: {cycle_count} cycles processed")
        self._generate_summary_report()
    
    def _update_performance_metrics(self, sensor_data: SensorData, decisions: List[AgentDecision]):
        """Update performance tracking metrics"""
        # Calculate defect rate based on QCIA actions
        if any(d.action == "immediate_alert" for d in decisions if d.agent_type == "QCIA"):
            defect_rate = sensor_data.quality_metrics['defect_probability']
        else:
            defect_rate = sensor_data.quality_metrics['defect_probability'] * 0.3  # Reduced by AI intervention
        
        # Calculate equipment uptime based on PMA actions
        pma_decision = next(d for d in decisions if d.agent_type == "PMA")
        if pma_decision.action == "immediate_maintenance":
            uptime = 0.7  # Planned downtime better than failure
        elif pma_decision.action == "schedule_maintenance":
            uptime = 0.95
        else:
            uptime = 0.99
        
        # Calculate production efficiency based on WOA actions
        base_efficiency = sensor_data.workforce['current_production_rate'] / 100
        woa_decision = next(d for d in decisions if d.agent_type == "WOA")
        if woa_decision.action == "major_optimization":
            efficiency = min(1.0, base_efficiency * 1.15)
        elif woa_decision.action == "minor_adjustment":
            efficiency = min(1.0, base_efficiency * 1.05)
        else:
            efficiency = base_efficiency
        
        # Calculate cost savings (simplified model)
        quality_savings = (0.15 - defect_rate) * 10000  # $10k per % defect reduction
        maintenance_savings = uptime * 5000  # $5k per % uptime
        efficiency_savings = efficiency * 3000  # $3k per % efficiency
        total_savings = quality_savings + maintenance_savings + efficiency_savings
        
        # Store metrics
        self.performance_metrics['defect_rate'].append(defect_rate)
        self.performance_metrics['equipment_uptime'].append(uptime)
        self.performance_metrics['production_efficiency'].append(efficiency)
        self.performance_metrics['cost_savings'].append(total_savings)
    
    def _generate_summary_report(self):
        """Generate comprehensive simulation summary"""
        print("\\n" + "=" * 60)
        print("SIMULATION SUMMARY REPORT")
        print("=" * 60)
        
        # Agent performance summary
        print(f"\\nAgent Performance:")
        print(f"QCIA - Decisions: {self.qcia.decisions_made}, Alerts: {self.qcia.alerts_triggered}")
        print(f"PMA - Decisions: {self.pma.decisions_made}, Maintenance Scheduled: {self.pma.maintenance_scheduled}")
        print(f"WOA - Decisions: {self.woa.decisions_made}, Optimizations: {self.woa.optimizations_made}")
        
        # Performance metrics
        avg_defect_rate = np.mean(self.performance_metrics['defect_rate'])
        avg_uptime = np.mean(self.performance_metrics['equipment_uptime'])
        avg_efficiency = np.mean(self.performance_metrics['production_efficiency'])
        total_savings = sum(self.performance_metrics['cost_savings'])
        
        print(f"\\nPerformance Metrics:")
        print(f"Average Defect Rate: {avg_defect_rate:.1%} (Target: <5%)")
        print(f"Average Equipment Uptime: {avg_uptime:.1%} (Target: >95%)")
        print(f"Average Production Efficiency: {avg_efficiency:.1%} (Target: >90%)")
        print(f"Total Cost Savings: ${total_savings:,.0f}")
        
        # ROI calculation
        annual_savings = total_savings * (365 * 24) / len(self.simulation_data) * (5 / 60)  # Extrapolate to annual
        implementation_cost = 5500000  # $5.5M from case study
        roi = (annual_savings - implementation_cost) / implementation_cost * 100
        
        print(f"\\nROI Analysis:")
        print(f"Projected Annual Savings: ${annual_savings:,.0f}")
        print(f"Implementation Cost: ${implementation_cost:,.0f}")
        print(f"Projected ROI: {roi:.1f}%")
        
        # Decision distribution
        decision_counts = {}
        for decision in self.agent_decisions:
            key = f"{decision.agent_type}_{decision.action}"
            decision_counts[key] = decision_counts.get(key, 0) + 1
        
        print(f"\\nDecision Distribution:")
        for decision_type, count in sorted(decision_counts.items()):
            print(f"  {decision_type}: {count}")
    
    def create_visualizations(self):
        """Create performance visualization dashboard"""
        print("\\nGenerating performance visualizations...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Defect rate over time
        axes[0, 0].plot(self.performance_metrics['defect_rate'], color='red', linewidth=2)
        axes[0, 0].axhline(y=0.05, color='green', linestyle='--', label='Target (5%)')
        axes[0, 0].set_title('Defect Rate Over Time')
        axes[0, 0].set_ylabel('Defect Rate')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Equipment uptime
        axes[0, 1].plot(self.performance_metrics['equipment_uptime'], color='blue', linewidth=2)
        axes[0, 1].axhline(y=0.95, color='green', linestyle='--', label='Target (95%)')
        axes[0, 1].set_title('Equipment Uptime')
        axes[0, 1].set_ylabel('Uptime %')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Production efficiency
        axes[1, 0].plot(self.performance_metrics['production_efficiency'], color='orange', linewidth=2)
        axes[1, 0].axhline(y=0.90, color='green', linestyle='--', label='Target (90%)')
        axes[1, 0].set_title('Production Efficiency')
        axes[1, 0].set_ylabel('Efficiency %')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Cumulative cost savings
        cumulative_savings = np.cumsum(self.performance_metrics['cost_savings'])
        axes[1, 1].plot(cumulative_savings, color='green', linewidth=2)
        axes[1, 1].set_title('Cumulative Cost Savings')
        axes[1, 1].set_ylabel('Savings ($)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('simulation_results/agent_performance_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Dashboard saved as: simulation_results/agent_performance_dashboard.png")
    
    def export_results(self):
        """Export simulation results to JSON"""
        results = {
            'simulation_metadata': {
                'total_cycles': len(self.simulation_data),
                'agents_deployed': 3,
                'simulation_duration': '24 hours',
                'generated_at': datetime.now().isoformat()
            },
            'agent_performance': {
                'qcia': {
                    'decisions_made': self.qcia.decisions_made,
                    'alerts_triggered': self.qcia.alerts_triggered,
                    'alert_rate': self.qcia.alerts_triggered / self.qcia.decisions_made if self.qcia.decisions_made > 0 else 0
                },
                'pma': {
                    'decisions_made': self.pma.decisions_made,
                    'maintenance_scheduled': self.pma.maintenance_scheduled,
                    'maintenance_rate': self.pma.maintenance_scheduled / self.pma.decisions_made if self.pma.decisions_made > 0 else 0
                },
                'woa': {
                    'decisions_made': self.woa.decisions_made,
                    'optimizations_made': self.woa.optimizations_made,
                    'optimization_rate': self.woa.optimizations_made / self.woa.decisions_made if self.woa.decisions_made > 0 else 0
                }
            },
            'performance_summary': {
                'average_defect_rate': float(np.mean(self.performance_metrics['defect_rate'])),
                'average_uptime': float(np.mean(self.performance_metrics['equipment_uptime'])),
                'average_efficiency': float(np.mean(self.performance_metrics['production_efficiency'])),
                'total_cost_savings': float(sum(self.performance_metrics['cost_savings']))
            }
        }
        
        with open('simulation_results/simulation_log.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("Results exported to: simulation_results/simulation_log.json")

def main():
    """Main simulation execution"""
    print("AI Agents Manufacturing Simulation")
    print("AutoParts Inc. Smart Manufacturing Implementation")
    print("=" * 60)
    
    # Create simulation results directory
    import os
    os.makedirs('simulation_results', exist_ok=True)
    
    # Initialize and run simulation
    simulator = ManufacturingSimulator()
    
    # Run 24-hour simulation with 5-minute intervals
    simulator.run_simulation(duration_hours=24, interval_minutes=5)
    
    # Generate visualizations
    simulator.create_visualizations()
    
    # Export results
    simulator.export_results()
    
    print("\\n" + "=" * 60)
    print("SIMULATION COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("Files generated:")
    print("  • simulation_results/agent_performance_dashboard.png")
    print("  • simulation_results/simulation_log.json")
    print("\\nThe simulation demonstrates the effectiveness of AI agents in:")
    print("  • Quality control and defect prevention")
    print("  • Predictive maintenance and uptime optimization")
    print("  • Workforce allocation and productivity enhancement")

if __name__ == "__main__":
    main()