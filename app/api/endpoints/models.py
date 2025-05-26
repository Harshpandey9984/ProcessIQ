"""
API endpoints for ML model operations.
"""

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, Query, UploadFile, File

from app.models.model_manager import ModelManager
from app.models.schemas.ml_models import (
    ModelInfo, 
    ModelTrainingRequest, 
    ModelTrainingResult,
    ModelPredictionRequest,
    ModelPredictionResult
)

router = APIRouter()

model_manager = ModelManager()

@router.get("/", response_model=List[ModelInfo])
async def get_available_models() -> Any:
    """
    Get list of available models with their information.
    """
    try:
        models = model_manager.get_models()
        return models
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve models: {str(e)}"
        )

@router.post("/train", response_model=ModelTrainingResult)
async def train_model(request: ModelTrainingRequest) -> Any:
    """
    Train a new model or retrain an existing model with new data.
    """
    try:
        result = model_manager.train_model(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model training failed: {str(e)}"
        )

@router.post("/predict", response_model=ModelPredictionResult)
async def predict_with_model(request: ModelPredictionRequest) -> Any:
    """
    Make predictions using a trained model.
    """
    try:
        result = model_manager.predict(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

@router.post("/upload", response_model=ModelInfo)
async def upload_model(
    model_name: str = Query(..., description="Name for the uploaded model"),
    model_type: str = Query(..., description="Type of the model"),
    model_file: UploadFile = File(..., description="Model file to upload")
) -> Any:
    """
    Upload a pre-trained model.
    """
    try:
        model_info = model_manager.upload_model(model_name, model_type, model_file)
        return model_info
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model upload failed: {str(e)}"
        )

@router.delete("/{model_id}", response_model=Dict[str, str])
async def delete_model(model_id: str) -> Any:
    """
    Delete a model.
    """
    try:
        model_manager.delete_model(model_id)
        return {"status": "success", "message": f"Model {model_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Model not found or deletion failed: {str(e)}"
        )
