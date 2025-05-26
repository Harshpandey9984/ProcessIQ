"""
Process optimization module for manufacturing processes.
"""

import uuid
import time
import logging
import numpy as np
from typing import Dict, List, Optional, Any, Tuple

from app.simulation.engine import SimulationEngine
from app.models.schemas.simulation import SimulationConfig
from app.models.schemas.optimization import (
    OptimizationRequest, 
    OptimizationResult, 
    OptimizationConfig,
    OptimizationConstraint,
    OptimizedParameter
)

from app.core.config import settings

logger = logging.getLogger(__name__)


class ProcessOptimizer:
    """Optimizer for manufacturing processes."""
    
    def __init__(self):
        """Initialize the process optimizer."""
        self.simulation_engine = SimulationEngine()
        
        # Available optimization algorithms
        self.algorithms = {
            "parameter": ["bayesian_optimization", "genetic_algorithm", "grid_search"],
            "schedule": ["reinforcement_learning", "constraint_satisfaction", "heuristic"]
        }
        
        # Intel optimizations
        if settings.USE_INTEL_OPTIMIZATIONS:
            try:
                import daal4py
                import sklearnex
                sklearnex.patch_sklearn()
                self.use_intel = True
                logger.info("Intel optimizations for ML enabled")
            except ImportError:
                self.use_intel = False
                logger.warning("Intel ML optimizations not available, using standard libraries")
        else:
            self.use_intel = False

    def optimize_parameters(self, request: OptimizationRequest) -> OptimizationResult:
        """
        Optimize process parameters based on the provided configuration and constraints.
        
        Args:
            request: Optimization request configuration
            
        Returns:
            OptimizationResult: Results from the optimization
        """
        start_time = time.time()
        
        # Validate process type
        process_type = request.process_type
        if process_type not in self.simulation_engine.get_process_types():
            raise ValueError(f"Process type '{process_type}' not supported")
        
        # Get available parameters for this process type
        available_parameters = {
            param.name: param for param in self.simulation_engine.get_parameters(process_type)
        }
        
        # Check if requested parameters to optimize are valid
        for param_name in request.parameters_to_optimize:
            if param_name not in available_parameters:
                raise ValueError(f"Parameter '{param_name}' not available for process type '{process_type}'")
        
        # Choose optimization algorithm based on request
        algorithm_name = request.config.algorithm
        if algorithm_name not in self.algorithms["parameter"]:
            raise ValueError(f"Algorithm '{algorithm_name}' not supported for parameter optimization")
        
        # Create parameter search space
        param_bounds = {}
        for param_name in request.parameters_to_optimize:
            param = available_parameters[param_name]
            param_bounds[param_name] = (param.min_value, param.max_value)
        
        # Get initial values for parameters and estimate initial performance
        initial_params = {}
        for param_name, param in available_parameters.items():
            if param_name in request.fixed_parameters:
                initial_params[param_name] = request.fixed_parameters[param_name]
            else:
                initial_params[param_name] = param.default_value
        
        initial_performance = self._evaluate_parameters(
            process_type, 
            initial_params, 
            request.target_variable, 
            request.maximize
        )
        
        # Run the appropriate optimization algorithm
        if algorithm_name == "bayesian_optimization":
            best_params, best_value = self._bayesian_optimization(
                process_type,
                param_bounds,
                request.fixed_parameters,
                request.target_variable,
                request.maximize,
                request.constraints,
                request.config.max_iterations
            )
        elif algorithm_name == "genetic_algorithm":
            best_params, best_value = self._genetic_algorithm(
                process_type,
                param_bounds,
                request.fixed_parameters,
                request.target_variable,
                request.maximize,
                request.constraints,
                request.config.max_iterations
            )
        elif algorithm_name == "grid_search":
            best_params, best_value = self._grid_search(
                process_type,
                param_bounds,
                request.fixed_parameters,
                request.target_variable,
                request.maximize,
                request.constraints,
                request.config.max_iterations
            )
        else:
            raise ValueError(f"Algorithm '{algorithm_name}' implementation not found")
        
        # Create OptimizedParameter objects
        optimized_parameters = []
        for param_name, value in best_params.items():
            if param_name in request.parameters_to_optimize:
                param = available_parameters[param_name]
                original_value = initial_params[param_name]
                improvement = None
                if original_value != 0:
                    improvement = (value - original_value) / original_value * 100
                
                optimized_parameters.append(
                    OptimizedParameter(
                        name=param_name,
                        value=value,
                        original_value=original_value,
                        unit=param.unit,
                        improvement_percent=improvement
                    )
                )
        
        # Estimate impact on quality, energy, and throughput
        sim_config = SimulationConfig(
            process_type=process_type,
            duration=60.0,  # 1 minute simulation
            parameters=best_params
        )
        sim_result = self.simulation_engine.run_simulation(sim_config)
        
        # Calculate improvements
        quality_impact = {
            metric: (sim_result.quality_metrics[metric] - initial_performance.get(f"quality_{metric}", 0))
            for metric in sim_result.quality_metrics
            if metric != "quality_score"  # Skip the aggregated score
        }
        
        energy_impact = (
            initial_performance.get("energy_consumption", 0) - sim_result.energy_consumption
        ) / initial_performance.get("energy_consumption", 1) * 100 if initial_performance.get("energy_consumption", 0) != 0 else 0
        
        throughput_impact = (
            sim_result.throughput - initial_performance.get("throughput", 0)
        ) / initial_performance.get("throughput", 1) * 100 if initial_performance.get("throughput", 0) != 0 else 0
        
        # Calculate improvement percentage
        if initial_performance.get(request.target_variable, 0) != 0:
            if request.maximize:
                improvement_percent = (best_value - initial_performance.get(request.target_variable, 0)) / abs(initial_performance.get(request.target_variable, 0)) * 100
            else:
                improvement_percent = (initial_performance.get(request.target_variable, 0) - best_value) / abs(initial_performance.get(request.target_variable, 0)) * 100
        else:
            improvement_percent = 0.0
        
        execution_time = time.time() - start_time
        
        # Create optimization result
        optimization_id = str(uuid.uuid4())
        result = OptimizationResult(
            optimization_id=optimization_id,
            process_type=process_type,
            target_variable=request.target_variable,
            initial_value=initial_performance.get(request.target_variable, 0),
            optimized_value=best_value,
            improvement_percent=improvement_percent,
            parameters=optimized_parameters,
            expected_quality_impact=quality_impact,
            expected_energy_impact=energy_impact,
            expected_throughput_impact=throughput_impact,
            confidence_score=0.85,  # This could be calculated based on the optimization algorithm's confidence
            execution_time=execution_time
        )
        
        return result

    def optimize_schedule(self, process_id: int, config: OptimizationConfig) -> Dict[str, Any]:
        """
        Optimize production schedule for a specific manufacturing process.
        
        This is a placeholder implementation.
        
        Args:
            process_id: ID of the manufacturing process
            config: Optimization configuration
            
        Returns:
            Dict: Schedule optimization results
        """
        # This would be a complex implementation integrating with scheduling systems
        # For now, returning a mock result
        return {
            "optimization_id": str(uuid.uuid4()),
            "process_id": process_id,
            "original_makespan": 480,  # minutes
            "optimized_makespan": 420,  # minutes
            "improvement_percent": 12.5,
            "schedule": {
                "jobs": [
                    {"job_id": 1, "start_time": "08:00", "end_time": "09:30", "machine_id": 1},
                    {"job_id": 2, "start_time": "09:45", "end_time": "11:15", "machine_id": 1},
                    # More jobs would be included here
                ],
                "machines": [
                    {"machine_id": 1, "utilization": 0.85},
                    {"machine_id": 2, "utilization": 0.78},
                    # More machines would be included here
                ]
            }
        }

    def get_algorithms(self, optimization_type: str) -> List[str]:
        """
        Get available optimization algorithms for a specific optimization type.
        
        Args:
            optimization_type: Type of optimization ('parameter' or 'schedule')
            
        Returns:
            List[str]: List of available algorithms
        """
        if optimization_type not in self.algorithms:
            raise ValueError(f"Optimization type '{optimization_type}' not supported")
        
        return self.algorithms[optimization_type]

    def multi_objective_optimization(self, request: OptimizationRequest, num_solutions: int = 5) -> List[OptimizationResult]:
        """
        Perform multi-objective optimization and return Pareto-optimal solutions.
        
        This is a simplified implementation that runs multiple single-objective optimizations
        with different weights.
        
        Args:
            request: Optimization request configuration
            num_solutions: Number of Pareto-optimal solutions to return
            
        Returns:
            List[OptimizationResult]: List of optimization results representing Pareto-optimal solutions
        """
        # This would be a complex implementation using multi-objective optimization algorithms
        # For now, returning multiple solutions with different weights
        
        # Make copies of the request for each optimization run
        results = []
        
        # Alternative target variables to consider
        target_variables = [
            request.target_variable,
            "quality_score",
            "energy_consumption",
            "throughput",
            "defect_rate"
        ]
        
        # Keep original target in list and remove duplicates
        if request.target_variable in target_variables[1:]:
            target_variables.remove(request.target_variable)
            
        # Ensure we don't try more targets than available
        num_targets = min(num_solutions, len(target_variables))
        
        for i in range(num_targets):
            # Create a modified request
            modified_request = OptimizationRequest(
                process_type=request.process_type,
                target_variable=target_variables[i],
                maximize=(target_variables[i] != "energy_consumption" and target_variables[i] != "defect_rate"),
                parameters_to_optimize=request.parameters_to_optimize,
                fixed_parameters=request.fixed_parameters,
                constraints=request.constraints,
                config=request.config
            )
            
            try:
                result = self.optimize_parameters(modified_request)
                results.append(result)
            except Exception as e:
                logger.warning(f"Failed to optimize for {target_variables[i]}: {str(e)}")
                continue
                
        return results

    def _evaluate_parameters(self, process_type: str, parameters: Dict[str, float], 
                            target_variable: str, maximize: bool) -> Dict[str, float]:
        """
        Evaluate a set of parameters using the simulation engine.
        
        Args:
            process_type: Type of manufacturing process
            parameters: Dictionary of parameter values
            target_variable: Variable to optimize
            maximize: If True, higher values are better; if False, lower values are better
            
        Returns:
            Dict[str, float]: Dictionary of performance metrics
        """
        # Run a short simulation with the given parameters
        config = SimulationConfig(
            process_type=process_type,
            duration=60.0,  # 1 minute simulation
            parameters=parameters
        )
        
        result = self.simulation_engine.run_simulation(config)
        
        # Extract metrics from simulation result
        metrics = {}
        
        # Copy quality metrics
        for metric, value in result.quality_metrics.items():
            metrics[f"quality_{metric}"] = value
        
        # Add other metrics
        metrics["energy_consumption"] = result.energy_consumption
        metrics["throughput"] = result.throughput
        metrics["defect_rate"] = result.defect_rate
        
        # Check if target variable exists in metrics
        if target_variable not in metrics and not target_variable.startswith("quality_"):
            quality_target = f"quality_{target_variable}"
            if quality_target in metrics:
                target_variable = quality_target
            else:
                raise ValueError(f"Target variable '{target_variable}' not found in simulation results")
        
        return metrics

    def _bayesian_optimization(self, process_type: str, param_bounds: Dict[str, Tuple[float, float]], 
                              fixed_params: Dict[str, float], target_variable: str, maximize: bool,
                              constraints: List[OptimizationConstraint], max_iterations: int) -> Tuple[Dict[str, float], float]:
        """
        Bayesian optimization for process parameters.
        
        Args:
            process_type: Type of manufacturing process
            param_bounds: Dictionary of parameter bounds (min, max)
            fixed_params: Dictionary of fixed parameter values
            target_variable: Variable to optimize
            maximize: If True, maximize target; if False, minimize
            constraints: List of constraints
            max_iterations: Maximum number of iterations
            
        Returns:
            Tuple[Dict[str, float], float]: Best parameters and target value
        """
        try:
            from sklearn.gaussian_process import GaussianProcessRegressor
            from sklearn.gaussian_process.kernels import Matern
            from bayes_opt import BayesianOptimization
        except ImportError:
            logger.error("Required libraries for Bayesian optimization not found")
            # Fall back to a simpler algorithm
            return self._grid_search(process_type, param_bounds, fixed_params, 
                                     target_variable, maximize, constraints, 
                                     max_iterations)
        
        # Define the objective function
        def objective(**kwargs):
            # Combine provided parameters with fixed parameters
            params = fixed_params.copy()
            params.update(kwargs)
            
            # Run simulation and get metrics
            metrics = self._evaluate_parameters(process_type, params, target_variable, maximize)
            
            # Check constraints
            penalty = 0
            for constraint in constraints:
                value = metrics.get(constraint.parameter, params.get(constraint.parameter))
                if value is None:
                    continue
                    
                if constraint.is_hard_constraint:
                    # Hard constraints: Apply large penalty if violated
                    if constraint.min_value is not None and value < constraint.min_value:
                        penalty += 1000 * (constraint.min_value - value)
                    if constraint.max_value is not None and value > constraint.max_value:
                        penalty += 1000 * (value - constraint.max_value)
                    if constraint.equals_value is not None and abs(value - constraint.equals_value) > 1e-6:
                        penalty += 1000 * abs(value - constraint.equals_value)
                else:
                    # Soft constraints: Apply weighted penalty if violated
                    if constraint.min_value is not None and value < constraint.min_value:
                        penalty += constraint.weight * (constraint.min_value - value)
                    if constraint.max_value is not None and value > constraint.max_value:
                        penalty += constraint.weight * (value - constraint.max_value)
                    if constraint.equals_value is not None:
                        penalty += constraint.weight * abs(value - constraint.equals_value)
            
            # Get target value
            target_value = metrics.get(target_variable, 0)
            
            # Apply penalty and adjust for maximization/minimization
            if maximize:
                return target_value - penalty
            else:
                return -target_value - penalty
        
        # Set up the optimizer
        optimizer = BayesianOptimization(
            f=objective,
            pbounds=param_bounds,
            random_state=42
        )
        
        # Run optimization
        optimizer.maximize(
            init_points=5,
            n_iter=max_iterations - 5
        )
        
        # Get best parameters
        best_params = optimizer.max["params"]
        
        # Combine with fixed parameters
        all_params = fixed_params.copy()
        all_params.update(best_params)
        
        # Evaluate the best solution to get the actual metrics
        metrics = self._evaluate_parameters(process_type, all_params, target_variable, maximize)
        best_value = metrics.get(target_variable, 0)
        
        return all_params, best_value

    def _genetic_algorithm(self, process_type: str, param_bounds: Dict[str, Tuple[float, float]], 
                          fixed_params: Dict[str, float], target_variable: str, maximize: bool,
                          constraints: List[OptimizationConstraint], max_iterations: int) -> Tuple[Dict[str, float], float]:
        """
        Genetic algorithm for process parameters.
        
        This is a simplified implementation for demonstration purposes.
        
        Args:
            process_type: Type of manufacturing process
            param_bounds: Dictionary of parameter bounds (min, max)
            fixed_params: Dictionary of fixed parameter values
            target_variable: Variable to optimize
            maximize: If True, maximize target; if False, minimize
            constraints: List of constraints
            max_iterations: Maximum number of iterations
            
        Returns:
            Tuple[Dict[str, float], float]: Best parameters and target value
        """
        # Simple GA implementation
        population_size = 20
        mutation_rate = 0.1
        elitism_count = 2
        
        # Initialize population
        population = []
        for _ in range(population_size):
            individual = {}
            for param_name, (min_val, max_val) in param_bounds.items():
                individual[param_name] = min_val + np.random.random() * (max_val - min_val)
            population.append(individual)
        
        best_individual = None
        best_fitness = float('-inf') if maximize else float('inf')
        
        for generation in range(max_iterations):
            # Evaluate fitness
            fitness_scores = []
            for individual in population:
                # Combine with fixed parameters
                params = fixed_params.copy()
                params.update(individual)
                
                # Run simulation and get metrics
                metrics = self._evaluate_parameters(process_type, params, target_variable, maximize)
                
                # Check constraints
                penalty = 0
                for constraint in constraints:
                    value = metrics.get(constraint.parameter, params.get(constraint.parameter))
                    if value is None:
                        continue
                        
                    if constraint.is_hard_constraint:
                        # Hard constraints: Apply large penalty if violated
                        if constraint.min_value is not None and value < constraint.min_value:
                            penalty += 1000 * (constraint.min_value - value)
                        if constraint.max_value is not None and value > constraint.max_value:
                            penalty += 1000 * (value - constraint.max_value)
                        if constraint.equals_value is not None and abs(value - constraint.equals_value) > 1e-6:
                            penalty += 1000 * abs(value - constraint.equals_value)
                    else:
                        # Soft constraints: Apply weighted penalty if violated
                        if constraint.min_value is not None and value < constraint.min_value:
                            penalty += constraint.weight * (constraint.min_value - value)
                        if constraint.max_value is not None and value > constraint.max_value:
                            penalty += constraint.weight * (value - constraint.max_value)
                        if constraint.equals_value is not None:
                            penalty += constraint.weight * abs(value - constraint.equals_value)
                
                # Get target value
                fitness = metrics.get(target_variable, 0)
                
                # Apply penalty
                if maximize:
                    fitness -= penalty
                else:
                    fitness += penalty
                
                fitness_scores.append(fitness)
                
                # Update best solution
                if (maximize and fitness > best_fitness) or (not maximize and fitness < best_fitness):
                    best_fitness = fitness
                    best_individual = individual.copy()
            
            # Selection and reproduction
            new_population = []
            
            # Elitism: keep best individuals
            if maximize:
                elite_indices = np.argsort(fitness_scores)[-elitism_count:]
            else:
                elite_indices = np.argsort(fitness_scores)[:elitism_count]
                
            for idx in elite_indices:
                new_population.append(population[idx].copy())
            
            # Tournament selection and crossover
            while len(new_population) < population_size:
                # Tournament selection
                tournament_size = 3
                tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
                
                tournament_fitness = [fitness_scores[i] for i in tournament_indices]
                if maximize:
                    parent1_idx = tournament_indices[np.argmax(tournament_fitness)]
                else:
                    parent1_idx = tournament_indices[np.argmin(tournament_fitness)]
                    
                tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
                tournament_fitness = [fitness_scores[i] for i in tournament_indices]
                if maximize:
                    parent2_idx = tournament_indices[np.argmax(tournament_fitness)]
                else:
                    parent2_idx = tournament_indices[np.argmin(tournament_fitness)]
                
                parent1 = population[parent1_idx]
                parent2 = population[parent2_idx]
                
                # Crossover
                child = {}
                for param_name in param_bounds.keys():
                    if np.random.random() < 0.5:
                        child[param_name] = parent1[param_name]
                    else:
                        child[param_name] = parent2[param_name]
                
                # Mutation
                for param_name, (min_val, max_val) in param_bounds.items():
                    if np.random.random() < mutation_rate:
                        delta = (max_val - min_val) * 0.1  # 10% mutation range
                        child[param_name] += np.random.uniform(-delta, delta)
                        child[param_name] = max(min_val, min(max_val, child[param_name]))
                
                new_population.append(child)
            
            # Replace population
            population = new_population
        
        if best_individual is None:
            # This shouldn't happen, but just in case
            best_individual = population[0]
        
        # Combine with fixed parameters
        all_params = fixed_params.copy()
        all_params.update(best_individual)
        
        # Evaluate the best solution to get the actual metrics
        metrics = self._evaluate_parameters(process_type, all_params, target_variable, maximize)
        best_value = metrics.get(target_variable, 0)
        
        return all_params, best_value

    def _grid_search(self, process_type: str, param_bounds: Dict[str, Tuple[float, float]], 
                    fixed_params: Dict[str, float], target_variable: str, maximize: bool,
                    constraints: List[OptimizationConstraint], max_iterations: int) -> Tuple[Dict[str, float], float]:
        """
        Grid search for process parameters.
        
        This is a simple implementation for when more advanced methods are not available.
        
        Args:
            process_type: Type of manufacturing process
            param_bounds: Dictionary of parameter bounds (min, max)
            fixed_params: Dictionary of fixed parameter values
            target_variable: Variable to optimize
            maximize: If True, maximize target; if False, minimize
            constraints: List of constraints
            max_iterations: Maximum number of iterations (used to determine grid density)
            
        Returns:
            Tuple[Dict[str, float], float]: Best parameters and target value
        """
        # Calculate number of points per dimension based on max_iterations
        n_dims = len(param_bounds)
        if n_dims == 0:
            # No parameters to optimize
            metrics = self._evaluate_parameters(process_type, fixed_params, target_variable, maximize)
            return fixed_params, metrics.get(target_variable, 0)
            
        points_per_dim = max(2, int(max_iterations ** (1 / n_dims)))
        
        # Generate grid points for each parameter
        grid_points = {}
        for param_name, (min_val, max_val) in param_bounds.items():
            grid_points[param_name] = np.linspace(min_val, max_val, points_per_dim)
        
        # Initialize best solution
        best_params = None
        if maximize:
            best_value = float('-inf')
        else:
            best_value = float('inf')
        
        # Generate all combinations (this is inefficient for high dimensions)
        import itertools
        param_names = list(param_bounds.keys())
        grid_values = [grid_points[param] for param in param_names]
        
        for values in itertools.product(*grid_values):
            # Create parameter dictionary
            params = fixed_params.copy()
            for i, param_name in enumerate(param_names):
                params[param_name] = values[i]
            
            # Run simulation and get metrics
            metrics = self._evaluate_parameters(process_type, params, target_variable, maximize)
            
            # Check constraints
            constraints_violated = False
            for constraint in constraints:
                if constraint.is_hard_constraint:
                    value = metrics.get(constraint.parameter, params.get(constraint.parameter))
                    if value is None:
                        continue
                        
                    if ((constraint.min_value is not None and value < constraint.min_value) or
                        (constraint.max_value is not None and value > constraint.max_value) or
                        (constraint.equals_value is not None and abs(value - constraint.equals_value) > 1e-6)):
                        constraints_violated = True
                        break
            
            if constraints_violated:
                continue
            
            # Update best solution
            value = metrics.get(target_variable, 0)
            if (maximize and value > best_value) or (not maximize and value < best_value):
                best_value = value
                best_params = params.copy()
        
        if best_params is None:
            # No valid solution found, return initial parameters
            logger.warning("No valid solution found in grid search due to constraints")
            best_params = fixed_params.copy()
            for param_name, (min_val, max_val) in param_bounds.items():
                best_params[param_name] = (min_val + max_val) / 2
            
            metrics = self._evaluate_parameters(process_type, best_params, target_variable, maximize)
            best_value = metrics.get(target_variable, 0)
        
        return best_params, best_value
