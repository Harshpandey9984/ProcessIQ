"""
Schemas for ML model data models.
"""

from typing import Dict, List, Optional, Union, Any
from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    """Information about a trained model."""
    model_id: str
    name: str
    model_type: str
    created_at: str
    updated_at: str
    accuracy_metrics: Dict[str, float]
    input_features: List[str]
    output_features: List[str]
    description: Optional[str] = None
    version: str = "1.0.0"


class ModelTrainingRequest(BaseModel):
    """Request to train a new model or retrain an existing model."""
    model_type: str = Field(..., description="Type of model to train")
    name: str = Field(..., description="Name for the model")
    input_features: List[str] = Field(..., description="List of input feature names")
    output_features: List[str] = Field(..., description="List of output feature names")
    dataset_id: Optional[str] = Field(None, description="ID of dataset to use")
    dataset_split_ratio: float = Field(0.8, description="Train/test split ratio")
    hyperparameters: Dict[str, Any] = Field(default_factory=dict, description="Model hyperparameters")
    use_intel_optimizations: bool = Field(True, description="Whether to use Intel-optimized algorithms")
    description: Optional[str] = None


class ModelTrainingResult(BaseModel):
    """Result of model training."""
    model_id: str
    name: str
    model_type: str
    training_time: float
    accuracy_metrics: Dict[str, float]
    input_features: List[str]
    output_features: List[str]
    feature_importances: Optional[Dict[str, float]] = None
    hyperparameters: Dict[str, Any]
    status: str


class ModelPredictionRequest(BaseModel):
    """Request to make predictions using a trained model."""
    model_id: str = Field(..., description="ID of the model to use for prediction")
    input_data: Union[Dict[str, List[float]], List[Dict[str, float]]] = Field(
        ..., description="Input data for prediction"
    )
    include_confidence: bool = Field(False, description="Whether to include confidence scores")
    use_intel_inference: bool = Field(True, description="Whether to use Intel-optimized inference")


class ModelPredictionResult(BaseModel):
    """Result of model prediction."""
    predictions: List[Dict[str, Any]]
    model_id: str
    prediction_time: float
    confidence_scores: Optional[Dict[str, List[float]]] = None
