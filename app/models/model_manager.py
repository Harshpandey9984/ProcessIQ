"""
Model manager for handling ML models in the Digital Twin Optimization Platform.
"""

import os
import uuid
import time
import logging
import pickle
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

import numpy as np
import pandas as pd
from fastapi import UploadFile

from app.core.config import settings
from app.models.schemas.ml_models import (
    ModelInfo, 
    ModelTrainingRequest, 
    ModelTrainingResult,
    ModelPredictionRequest,
    ModelPredictionResult
)

logger = logging.getLogger(__name__)


class ModelManager:
    """Manager for ML models in the Digital Twin Optimization Platform."""
    
    def __init__(self):
        """Initialize the model manager."""
        self.model_dir = settings.MODEL_DIR
        self.models = {}  # In-memory cache of models
        self.model_info = {}  # In-memory cache of model info
        
        # Create model directory if it doesn't exist
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Load existing models
        self._load_existing_models()
        
        # Intel optimizations
        if settings.USE_INTEL_OPTIMIZATIONS:
            try:
                import sklearnex
                sklearnex.patch_sklearn()
                self.use_intel = True
                logger.info("Intel optimizations for ML enabled")
            except ImportError:
                self.use_intel = False
                logger.warning("Intel ML optimizations not available, using standard libraries")
        else:
            self.use_intel = False

    def _load_existing_models(self):
        """Load existing models from disk."""
        if not os.path.exists(self.model_dir):
            return
            
        for filename in os.listdir(self.model_dir):
            if filename.endswith(".pkl"):
                model_id = filename.split(".")[0]
                info_file = os.path.join(self.model_dir, f"{model_id}_info.json")
                
                if os.path.exists(info_file):
                    try:
                        with open(info_file, "r") as f:
                            model_info = json.load(f)
                            self.model_info[model_id] = ModelInfo(**model_info)
                            logger.info(f"Loaded model info for {model_id}")
                    except Exception as e:
                        logger.error(f"Failed to load model info for {model_id}: {str(e)}")

    def get_models(self) -> List[ModelInfo]:
        """Get list of available models with their information."""
        return list(self.model_info.values())

    def train_model(self, request: ModelTrainingRequest) -> ModelTrainingResult:
        """
        Train a new model or retrain an existing model with new data.
        
        Args:
            request: Model training request
            
        Returns:
            ModelTrainingResult: Result of the model training
        """
        start_time = time.time()
        
        # Generate model ID
        model_id = str(uuid.uuid4())
        
        # Load data (in a real implementation, this would come from a database or data service)
        X_train, X_test, y_train, y_test = self._load_training_data(
            request.dataset_id,
            request.input_features,
            request.output_features,
            request.dataset_split_ratio
        )
        
        # Train model based on type
        model, accuracy_metrics, feature_importances = self._train_model_by_type(
            request.model_type,
            X_train, X_test,
            y_train, y_test,
            request.hyperparameters,
            request.use_intel_optimizations
        )
        
        # Save model
        model_path = os.path.join(self.model_dir, f"{model_id}.pkl")
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
        
        # Cache model in memory
        self.models[model_id] = model
        
        # Create model info
        model_info = ModelInfo(
            model_id=model_id,
            name=request.name,
            model_type=request.model_type,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            accuracy_metrics=accuracy_metrics,
            input_features=request.input_features,
            output_features=request.output_features,
            description=request.description,
            version="1.0.0"
        )
        
        # Save model info
        info_path = os.path.join(self.model_dir, f"{model_id}_info.json")
        with open(info_path, "w") as f:
            json.dump(model_info.dict(), f, indent=4)
        
        # Cache model info in memory
        self.model_info[model_id] = model_info
        
        training_time = time.time() - start_time
        
        # Create training result
        result = ModelTrainingResult(
            model_id=model_id,
            name=request.name,
            model_type=request.model_type,
            training_time=training_time,
            accuracy_metrics=accuracy_metrics,
            input_features=request.input_features,
            output_features=request.output_features,
            feature_importances=feature_importances,
            hyperparameters=request.hyperparameters,
            status="success"
        )
        
        return result

    def predict(self, request: ModelPredictionRequest) -> ModelPredictionResult:
        """
        Make predictions using a trained model.
        
        Args:
            request: Model prediction request
            
        Returns:
            ModelPredictionResult: Result of the prediction
        """
        start_time = time.time()
        
        model_id = request.model_id
        
        # Check if model exists
        if model_id not in self.model_info:
            raise ValueError(f"Model with ID {model_id} not found")
        
        # Load model if not in memory
        if model_id not in self.models:
            model_path = os.path.join(self.model_dir, f"{model_id}.pkl")
            if not os.path.exists(model_path):
                raise ValueError(f"Model file for ID {model_id} not found")
                
            with open(model_path, "rb") as f:
                self.models[model_id] = pickle.load(f)
        
        model = self.models[model_id]
        model_info = self.model_info[model_id]
        
        # Prepare input data
        X = self._prepare_prediction_input(request.input_data, model_info.input_features)
        
        # Make prediction
        if request.use_intel_inference and settings.USE_OPENVINO and model_info.model_type in ["random_forest", "gradient_boosting", "xgboost"]:
            # Use OpenVINO for inference if available
            try:
                import openvino as ov
                # This would be a real OpenVINO inference implementation
                # For demonstration, just using the model directly
                y_pred = model.predict(X)
                
                # Get confidence scores if requested
                confidence_scores = None
                if request.include_confidence and hasattr(model, "predict_proba"):
                    confidence_scores = model.predict_proba(X)
            except ImportError:
                # Fall back to standard inference
                y_pred = model.predict(X)
                
                # Get confidence scores if requested
                confidence_scores = None
                if request.include_confidence and hasattr(model, "predict_proba"):
                    confidence_scores = model.predict_proba(X)
        else:
            # Standard inference
            y_pred = model.predict(X)
            
            # Get confidence scores if requested
            confidence_scores = None
            if request.include_confidence and hasattr(model, "predict_proba"):
                confidence_scores = model.predict_proba(X)
        
        # Format predictions
        predictions = []
        for i, pred in enumerate(y_pred):
            pred_dict = {}
            
            if len(model_info.output_features) == 1:
                # Single output
                pred_dict[model_info.output_features[0]] = pred
            else:
                # Multiple outputs
                for j, feature in enumerate(model_info.output_features):
                    pred_dict[feature] = pred[j] if isinstance(pred, (list, np.ndarray)) else pred
            
            predictions.append(pred_dict)
        
        # Format confidence scores
        conf_dict = None
        if confidence_scores is not None:
            conf_dict = {}
            for i, feature in enumerate(model_info.output_features):
                if confidence_scores.shape[1] > 1:  # Multi-class
                    conf_dict[feature] = confidence_scores[:, i].tolist()
                else:  # Binary
                    conf_dict[feature] = confidence_scores.tolist()
        
        prediction_time = time.time() - start_time
        
        # Create prediction result
        result = ModelPredictionResult(
            predictions=predictions,
            model_id=model_id,
            prediction_time=prediction_time,
            confidence_scores=conf_dict
        )
        
        return result

    def upload_model(self, model_name: str, model_type: str, model_file: UploadFile) -> ModelInfo:
        """
        Upload a pre-trained model.
        
        Args:
            model_name: Name for the uploaded model
            model_type: Type of the model
            model_file: Model file to upload
            
        Returns:
            ModelInfo: Information about the uploaded model
        """
        # Generate model ID
        model_id = str(uuid.uuid4())
        
        # Save model file
        model_path = os.path.join(self.model_dir, f"{model_id}.pkl")
        
        # Read and write the file
        with open(model_path, "wb") as f:
            content = model_file.file.read()
            f.write(content)
        
        try:
            # Try to load the model to ensure it's valid
            with open(model_path, "rb") as f:
                model = pickle.load(f)
                
            # For demonstration, assuming input/output features
            input_features = ["feature1", "feature2"]
            output_features = ["output"]
            
            # Create model info
            model_info = ModelInfo(
                model_id=model_id,
                name=model_name,
                model_type=model_type,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
                accuracy_metrics={"unknown": 0.0},  # No metrics available for uploaded models
                input_features=input_features,
                output_features=output_features,
                description=f"Uploaded model: {model_name}",
                version="1.0.0"
            )
            
            # Save model info
            info_path = os.path.join(self.model_dir, f"{model_id}_info.json")
            with open(info_path, "w") as f:
                json.dump(model_info.dict(), f, indent=4)
            
            # Cache model and info in memory
            self.models[model_id] = model
            self.model_info[model_id] = model_info
            
            return model_info
            
        except Exception as e:
            # If there's an error, delete the model file
            if os.path.exists(model_path):
                os.remove(model_path)
            raise ValueError(f"Invalid model file: {str(e)}")

    def delete_model(self, model_id: str):
        """
        Delete a model.
        
        Args:
            model_id: ID of the model to delete
        """
        if model_id not in self.model_info:
            raise ValueError(f"Model with ID {model_id} not found")
            
        # Remove from memory
        if model_id in self.models:
            del self.models[model_id]
        
        del self.model_info[model_id]
        
        # Delete files
        model_path = os.path.join(self.model_dir, f"{model_id}.pkl")
        info_path = os.path.join(self.model_dir, f"{model_id}_info.json")
        
        if os.path.exists(model_path):
            os.remove(model_path)
            
        if os.path.exists(info_path):
            os.remove(info_path)

    def _load_training_data(self, dataset_id: Optional[str], input_features: List[str], 
                           output_features: List[str], split_ratio: float) -> tuple:
        """
        Load training data for model training.
        
        In a real implementation, this would load data from a database or file.
        For demonstration, we're generating synthetic data.
        
        Args:
            dataset_id: ID of dataset to use
            input_features: List of input feature names
            output_features: List of output feature names
            split_ratio: Train/test split ratio
            
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        # Generate synthetic data
        n_samples = 1000
        n_features = len(input_features)
        n_outputs = len(output_features)
        
        np.random.seed(42)
        
        X = np.random.randn(n_samples, n_features)
        
        if n_outputs == 1:
            # Single output - regression
            y = np.sum(X[:, :2], axis=1) + 0.1 * np.random.randn(n_samples)
        else:
            # Multiple outputs
            y = np.column_stack([
                np.sum(X[:, :2], axis=1) + 0.1 * np.random.randn(n_samples),
                np.mean(X[:, 1:3], axis=1) + 0.1 * np.random.randn(n_samples),
                np.max(X[:, 2:4], axis=1) + 0.1 * np.random.randn(n_samples)
            ])
            y = y[:, :n_outputs]  # Truncate to the required number of outputs
        
        # Split data
        split_idx = int(n_samples * split_ratio)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        return X_train, X_test, y_train, y_test

    def _train_model_by_type(self, model_type: str, X_train, X_test, y_train, y_test, 
                            hyperparameters: Dict[str, Any], use_intel: bool) -> tuple:
        """
        Train a model based on its type.
        
        Args:
            model_type: Type of model to train
            X_train: Training features
            X_test: Test features
            y_train: Training targets
            y_test: Test targets
            hyperparameters: Model hyperparameters
            use_intel: Whether to use Intel optimizations
            
        Returns:
            tuple: (trained_model, accuracy_metrics, feature_importances)
        """
        from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
        
        if model_type == "linear_regression":
            from sklearn.linear_model import LinearRegression
            model = LinearRegression(**hyperparameters)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            accuracy_metrics = {
                "mse": float(mse),
                "r2": float(r2)
            }
            
            feature_importances = {f"feature_{i}": float(coef) for i, coef in enumerate(model.coef_)} if len(model.coef_.shape) == 1 else None
            
        elif model_type == "random_forest":
            if use_intel and self.use_intel:
                from sklearnex.ensemble import RandomForestRegressor
                logger.info("Using Intel-optimized RandomForestRegressor")
            else:
                from sklearn.ensemble import RandomForestRegressor
            
            # Set default hyperparameters if not provided
            hyperparams = {
                "n_estimators": 100,
                "max_depth": 10,
                "random_state": 42
            }
            hyperparams.update(hyperparameters)
            
            model = RandomForestRegressor(**hyperparams)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            accuracy_metrics = {
                "mse": float(mse),
                "r2": float(r2)
            }
            
            feature_importances = {f"feature_{i}": float(imp) for i, imp in enumerate(model.feature_importances_)}
            
        elif model_type == "gradient_boosting":
            if use_intel and self.use_intel:
                from sklearnex.ensemble import GradientBoostingRegressor
                logger.info("Using Intel-optimized GradientBoostingRegressor")
            else:
                from sklearn.ensemble import GradientBoostingRegressor
            
            # Set default hyperparameters if not provided
            hyperparams = {
                "n_estimators": 100,
                "learning_rate": 0.1,
                "max_depth": 3,
                "random_state": 42
            }
            hyperparams.update(hyperparameters)
            
            model = GradientBoostingRegressor(**hyperparams)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            accuracy_metrics = {
                "mse": float(mse),
                "r2": float(r2)
            }
            
            feature_importances = {f"feature_{i}": float(imp) for i, imp in enumerate(model.feature_importances_)}
            
        elif model_type == "neural_network":
            # For demonstration, using a simple MLPRegressor
            # In a real implementation, this could use TensorFlow or PyTorch
            from sklearn.neural_network import MLPRegressor
            
            # Set default hyperparameters if not provided
            hyperparams = {
                "hidden_layer_sizes": (100, 50),
                "activation": "relu",
                "max_iter": 500,
                "random_state": 42
            }
            hyperparams.update(hyperparameters)
            
            model = MLPRegressor(**hyperparams)
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            accuracy_metrics = {
                "mse": float(mse),
                "r2": float(r2)
            }
            
            # Neural networks don't have built-in feature importances
            feature_importances = None
            
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        return model, accuracy_metrics, feature_importances

    def _prepare_prediction_input(self, input_data: Union[Dict[str, List[float]], List[Dict[str, float]]], 
                                 input_features: List[str]) -> np.ndarray:
        """
        Prepare input data for prediction.
        
        Args:
            input_data: Input data in one of two formats:
                - Dict mapping feature names to lists of values
                - List of dicts, each mapping feature names to single values
            input_features: Expected input feature names
            
        Returns:
            np.ndarray: Prepared input data as a numpy array
        """
        if isinstance(input_data, dict):
            # Format 1: Dict mapping feature names to lists of values
            # Convert to DataFrame and ensure correct column order
            df = pd.DataFrame(input_data)
            X = df[input_features].values
            
        elif isinstance(input_data, list):
            # Format 2: List of dicts, each mapping feature names to single values
            # Convert to DataFrame and ensure correct column order
            df = pd.DataFrame(input_data)
            X = df[input_features].values
            
        else:
            raise ValueError("Input data must be either a dict of lists or a list of dicts")
        
        return X
