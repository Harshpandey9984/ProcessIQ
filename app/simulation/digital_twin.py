"""
Digital Twin Manager for creating and managing digital twins of manufacturing processes.
"""

import uuid
import time
import logging
import threading
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime

from app.core.config import settings
from app.simulation.engine import SimulationEngine
from app.models.schemas.digital_twin import (
    DigitalTwinConfig, 
    DigitalTwinStatus,
    DigitalTwinData,
    ScenarioConfig,
    ScenarioResult
)

logger = logging.getLogger(__name__)


class DigitalTwin:
    """Digital twin of a manufacturing process."""
    
    def __init__(self, twin_id: str, config: DigitalTwinConfig):
        """Initialize a digital twin."""
        self.twin_id = twin_id
        self.name = config.name
        self.process_type = config.process_type
        self.description = config.description
        self.parameters = config.parameters.copy()
        self.update_frequency = config.update_frequency
        self.simulation_speed_factor = config.simulation_speed_factor
        self.include_random_events = config.include_random_events
        
        self.created_at = datetime.now().isoformat()
        self.status = "initializing"
        self.current_time = 0.0
        self.uptime = 0.0
        self.last_updated = datetime.now().isoformat()
        
        # Current sensor readings and metrics
        self.current_metrics = {}
        
        # Historical data
        self.max_history_points = 10000  # Limit memory usage
        self.timestamps = []
        self.parameter_history = {param: [] for param in self.parameters}
        self.sensor_history = {}
        self.metric_history = {}
        self.events = []
        
        # Simulation engine
        self.simulation_engine = SimulationEngine()
        
        # Thread for running the simulation
        self.thread = None
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        """Start the digital twin simulation."""
        if self.status in ["running", "initializing"]:
            return
            
        self.running = True
        self.status = "running"
        self.thread = threading.Thread(target=self._simulation_loop)
        self.thread.daemon = True
        self.thread.start()
        
        logger.info(f"Digital twin {self.name} ({self.twin_id}) started")

    def stop(self):
        """Stop the digital twin simulation."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5.0)
        self.status = "terminated"
        logger.info(f"Digital twin {self.name} ({self.twin_id}) stopped")

    def pause(self):
        """Pause the digital twin simulation."""
        if self.status == "running":
            self.status = "paused"
            logger.info(f"Digital twin {self.name} ({self.twin_id}) paused")

    def resume(self):
        """Resume the digital twin simulation."""
        if self.status == "paused":
            self.status = "running"
            logger.info(f"Digital twin {self.name} ({self.twin_id}) resumed")

    def update_parameters(self, new_parameters: Dict[str, float]):
        """Update the digital twin parameters."""
        with self.lock:
            self.parameters.update(new_parameters)
            
            # Record parameter change event
            event = {
                "timestamp": self.current_time,
                "type": "parameter_change",
                "parameters": new_parameters.copy()
            }
            self.events.append(event)
            
            logger.info(f"Digital twin {self.name} ({self.twin_id}) parameters updated: {new_parameters}")

    def get_status(self) -> DigitalTwinStatus:
        """Get the current status of the digital twin."""
        return DigitalTwinStatus(
            twin_id=self.twin_id,
            name=self.name,
            process_type=self.process_type,
            created_at=self.created_at,
            status=self.status,
            current_time=self.current_time,
            uptime=self.uptime,
            current_parameters=self.parameters.copy(),
            current_metrics=self.current_metrics.copy(),
            last_updated=self.last_updated
        )

    def get_data(self, start_time: Optional[float] = None, end_time: Optional[float] = None) -> DigitalTwinData:
        """Get data from the digital twin for a specific time period."""
        with self.lock:
            # Default to all data if no time range is specified
            if start_time is None:
                start_time = 0.0
            if end_time is None:
                end_time = float('inf')
            
            # Find indices for the requested time range
            indices = [i for i, ts in enumerate(self.timestamps) if start_time <= ts <= end_time]
            
            if not indices:
                # No data in the requested range
                return DigitalTwinData(
                    twin_id=self.twin_id,
                    process_type=self.process_type,
                    start_time=start_time,
                    end_time=end_time,
                    timestamps=[],
                    parameters={param: [] for param in self.parameter_history},
                    sensor_readings={sensor: [] for sensor in self.sensor_history},
                    quality_metrics={metric: [] for metric in self.metric_history},
                    events=[]
                )
            
            # Extract data for the requested time range
            timestamps = [self.timestamps[i] for i in indices]
            
            parameters = {}
            for param, history in self.parameter_history.items():
                if history:  # Check if history is not empty
                    parameters[param] = [history[i] if i < len(history) else history[-1] for i in indices]
                else:
                    parameters[param] = [0.0] * len(indices)
            
            sensor_readings = {}
            for sensor, history in self.sensor_history.items():
                if history:  # Check if history is not empty
                    sensor_readings[sensor] = [history[i] if i < len(history) else history[-1] for i in indices]
                else:
                    sensor_readings[sensor] = [0.0] * len(indices)
            
            quality_metrics = {}
            for metric, history in self.metric_history.items():
                if history:  # Check if history is not empty
                    quality_metrics[metric] = [history[i] if i < len(history) else history[-1] for i in indices]
                else:
                    quality_metrics[metric] = [0.0] * len(indices)
            
            # Extract events in the time range
            events_in_range = [event for event in self.events 
                               if start_time <= event["timestamp"] <= end_time]
            
            return DigitalTwinData(
                twin_id=self.twin_id,
                process_type=self.process_type,
                start_time=start_time,
                end_time=end_time,
                timestamps=timestamps,
                parameters=parameters,
                sensor_readings=sensor_readings,
                quality_metrics=quality_metrics,
                events=events_in_range
            )

    def run_scenario(self, scenario: ScenarioConfig) -> ScenarioResult:
        """Run a what-if scenario on the digital twin."""
        scenario_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Copy current state for baseline
        baseline_params = self.parameters.copy()
        baseline_metrics = self.current_metrics.copy()
        
        # Apply parameter changes for the scenario
        scenario_params = baseline_params.copy()
        scenario_params.update(scenario.parameter_changes)
        
        # Run simulation with scenario parameters
        config = {
            "process_type": self.process_type,
            "duration": scenario.duration,
            "parameters": scenario_params,
            "random_seed": scenario.random_seed,
            "include_sensor_noise": True
        }
        
        # Convert dict to SimulationConfig
        from app.models.schemas.simulation import SimulationConfig
        sim_config = SimulationConfig(**config)
        
        # Run the simulation
        result = self.simulation_engine.run_simulation(sim_config)
        
        # Calculate impact analysis (percentage changes)
        impact_analysis = {}
        scenario_metrics = {}
        
        # Extract final metrics from simulation result
        scenario_metrics["quality_score"] = result.quality_metrics["quality_score"]
        scenario_metrics["energy_consumption"] = result.energy_consumption / scenario.duration * 3600  # per hour
        scenario_metrics["throughput"] = result.throughput
        scenario_metrics["defect_rate"] = result.defect_rate
        
        # Calculate percentage changes
        for metric, value in scenario_metrics.items():
            if metric in baseline_metrics and baseline_metrics[metric] != 0:
                impact_analysis[metric] = (value - baseline_metrics[metric]) / baseline_metrics[metric] * 100
            else:
                impact_analysis[metric] = 0.0
        
        execution_time = time.time() - start_time
        
        # Create ScenarioResult object
        scenario_result = ScenarioResult(
            scenario_id=scenario_id,
            twin_id=self.twin_id,
            name=scenario.name,
            start_time=0.0,  # Simulation time, not real time
            end_time=scenario.duration,
            parameter_changes=scenario.parameter_changes,
            baseline_metrics=baseline_metrics,
            scenario_metrics=scenario_metrics,
            impact_analysis=impact_analysis,
            timestamps=result.timestamps,
            time_series_data=result.sensor_readings,
            execution_time=execution_time
        )
        
        return scenario_result

    def _simulation_loop(self):
        """Main simulation loop for the digital twin."""
        sim_dt = 1.0 / self.update_frequency  # Time step in seconds
        real_dt = sim_dt / self.simulation_speed_factor  # Adjusted for simulation speed
        
        last_random_event_time = 0.0
        random_event_interval = 300.0  # 5 minutes between random events
        
        try:
            while self.running:
                start_time = time.time()
                
                if self.status != "paused":
                    with self.lock:
                        # Advance simulation time
                        self.current_time += sim_dt
                        self.uptime += sim_dt
                        
                        # Run a short simulation for the current time step
                        self._update_simulation_step(sim_dt)
                        
                        # Generate random events if enabled
                        if self.include_random_events and (self.current_time - last_random_event_time) >= random_event_interval:
                            self._generate_random_event()
                            last_random_event_time = self.current_time
                        
                        # Update last updated timestamp
                        self.last_updated = datetime.now().isoformat()
                        
                        # Log status periodically (every 60 seconds of simulation time)
                        if int(self.current_time) % 60 == 0 and sim_dt < 60:
                            logger.debug(f"Digital twin {self.name} running at time {self.current_time:.1f}s")
                            
                # Calculate sleep time to maintain real-time factor
                elapsed = time.time() - start_time
                sleep_time = max(0.0, real_dt - elapsed)
                
                time.sleep(sleep_time)
                
        except Exception as e:
            self.status = "error"
            logger.error(f"Digital twin {self.name} ({self.twin_id}) error: {str(e)}")
            raise

    def _update_simulation_step(self, dt: float):
        """Update the digital twin state for a single time step."""
        # Create a short-duration simulation config
        from app.models.schemas.simulation import SimulationConfig
        
        config = SimulationConfig(
            process_type=self.process_type,
            duration=dt,
            parameters=self.parameters,
            include_sensor_noise=True
        )
        
        # Run the simulation for this time step
        result = self.simulation_engine.run_simulation(config)
        
        # Extract latest values from result
        latest_sensor_readings = {}
        for sensor, values in result.sensor_readings.items():
            if values:  # Check if values is not empty
                latest_sensor_readings[sensor] = values[-1]
        
        # Update current metrics
        self.current_metrics = result.quality_metrics.copy()
        self.current_metrics["energy_consumption"] = result.energy_consumption / dt * 3600  # per hour
        self.current_metrics["throughput"] = result.throughput
        self.current_metrics["defect_rate"] = result.defect_rate
        
        # Store historical data
        self.timestamps.append(self.current_time)
        
        for param, value in self.parameters.items():
            if param in self.parameter_history:
                self.parameter_history[param].append(value)
            else:
                self.parameter_history[param] = [value]
        
        for sensor, value in latest_sensor_readings.items():
            if sensor in self.sensor_history:
                self.sensor_history[sensor].append(value)
            else:
                self.sensor_history[sensor] = [value]
        
        for metric, value in self.current_metrics.items():
            if metric in self.metric_history:
                self.metric_history[metric].append(value)
            else:
                self.metric_history[metric] = [value]
                
        # Trim history if it gets too long
        if len(self.timestamps) > self.max_history_points:
            self._trim_history()

    def _trim_history(self):
        """Trim historical data to limit memory usage."""
        trim_to = self.max_history_points // 2  # Remove half the data points
        
        self.timestamps = self.timestamps[-trim_to:]
        
        for param in self.parameter_history:
            if self.parameter_history[param]:
                self.parameter_history[param] = self.parameter_history[param][-trim_to:]
                
        for sensor in self.sensor_history:
            if self.sensor_history[sensor]:
                self.sensor_history[sensor] = self.sensor_history[sensor][-trim_to:]
                
        for metric in self.metric_history:
            if self.metric_history[metric]:
                self.metric_history[metric] = self.metric_history[metric][-trim_to:]
                
        logger.debug(f"Trimmed history for digital twin {self.name} to {trim_to} points")

    def _generate_random_event(self):
        """Generate a random event in the digital twin."""
        event_types = ["machine_failure", "material_deviation", "power_fluctuation", "quality_alert"]
        event_type = np.random.choice(event_types, p=[0.2, 0.3, 0.3, 0.2])
        
        event = {
            "timestamp": self.current_time,
            "type": "random_event",
            "event_type": event_type,
            "severity": np.random.choice(["low", "medium", "high"], p=[0.6, 0.3, 0.1])
        }
        
        # Add event effects based on type
        if event_type == "machine_failure":
            # Simulate temporary parameter shifts
            param = np.random.choice(list(self.parameters.keys()))
            original_value = self.parameters[param]
            deviation = 0.2 * original_value * (np.random.random() - 0.5)
            
            self.parameters[param] = original_value + deviation
            event["affected_parameter"] = param
            event["deviation"] = deviation
            
            # Schedule restoration after some time
            restore_time = self.current_time + np.random.uniform(10, 60)
            restore_event = {
                "timestamp": restore_time,
                "type": "parameter_restoration",
                "parameter": param,
                "value": original_value,
                "related_event_type": event_type
            }
            self.events.append(restore_event)
            
        elif event_type == "material_deviation":
            # Impact quality metrics temporarily
            quality_impact = -0.1 * np.random.random()
            self.current_metrics["quality_score"] = max(0, min(1, self.current_metrics.get("quality_score", 0.8) + quality_impact))
            event["quality_impact"] = quality_impact
            
        elif event_type == "power_fluctuation":
            # Impact energy metrics
            energy_impact = 0.15 * np.random.random()
            self.current_metrics["energy_consumption"] = self.current_metrics.get("energy_consumption", 100) * (1 + energy_impact)
            event["energy_impact"] = energy_impact
            
        elif event_type == "quality_alert":
            # Impact defect rate
            defect_impact = 0.05 * np.random.random()
            self.current_metrics["defect_rate"] = min(1, self.current_metrics.get("defect_rate", 0.05) + defect_impact)
            event["defect_impact"] = defect_impact
        
        logger.info(f"Generated random event for twin {self.name}: {event_type} (severity: {event['severity']})")
        self.events.append(event)


class DigitalTwinManager:
    """Manager for creating and tracking digital twins."""
    
    def __init__(self):
        """Initialize the digital twin manager."""
        self.twins = {}  # Dictionary of twin_id -> DigitalTwin
        logger.info("Digital Twin Manager initialized")

    def create_digital_twin(self, config: DigitalTwinConfig) -> DigitalTwinStatus:
        """Create a new digital twin."""
        twin_id = str(uuid.uuid4())
        
        # Create the digital twin
        twin = DigitalTwin(twin_id, config)
        self.twins[twin_id] = twin
        
        # Start the digital twin simulation
        twin.start()
        
        logger.info(f"Created digital twin {config.name} with ID {twin_id}")
        
        return twin.get_status()

    def get_status(self, twin_id: str) -> DigitalTwinStatus:
        """Get the current status of a digital twin."""
        if twin_id not in self.twins:
            raise ValueError(f"Digital twin with ID {twin_id} not found")
        
        return self.twins[twin_id].get_status()

    def get_data(self, twin_id: str, start_time: Optional[float] = None, end_time: Optional[float] = None) -> DigitalTwinData:
        """Get data from a digital twin for a specific time period."""
        if twin_id not in self.twins:
            raise ValueError(f"Digital twin with ID {twin_id} not found")
        
        return self.twins[twin_id].get_data(start_time, end_time)

    def update_parameters(self, twin_id: str, parameters: Dict[str, float]) -> DigitalTwinStatus:
        """Update the parameters of a digital twin."""
        if twin_id not in self.twins:
            raise ValueError(f"Digital twin with ID {twin_id} not found")
        
        self.twins[twin_id].update_parameters(parameters)
        return self.twins[twin_id].get_status()

    def run_scenario(self, twin_id: str, scenario: ScenarioConfig) -> ScenarioResult:
        """Run a what-if scenario on a digital twin."""
        if twin_id not in self.twins:
            raise ValueError(f"Digital twin with ID {twin_id} not found")
        
        return self.twins[twin_id].run_scenario(scenario)

    def list_twins(self) -> List[Dict[str, Any]]:
        """List all available digital twins."""
        return [
            {
                "twin_id": twin_id,
                "name": twin.name,
                "process_type": twin.process_type,
                "status": twin.status,
                "created_at": twin.created_at
            }
            for twin_id, twin in self.twins.items()
        ]

    def delete_twin(self, twin_id: str):
        """Delete a digital twin."""
        if twin_id not in self.twins:
            raise ValueError(f"Digital twin with ID {twin_id} not found")
        
        # Stop the twin's simulation
        self.twins[twin_id].stop()
        
        # Remove from dictionary
        del self.twins[twin_id]
        
        logger.info(f"Deleted digital twin with ID {twin_id}")

    def stop_all(self):
        """Stop all digital twins."""
        for twin_id, twin in list(self.twins.items()):
            twin.stop()
        
        logger.info(f"Stopped all digital twins")
