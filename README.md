# ProcessIQ - Digital Twin Optimization Platform for Manufacturing Processes

## Project Overview

This platform creates digital twins of manufacturing processes, using AI to optimize production parameters, predict quality issues, and simulate process improvements without disrupting physical production. The solution leverages Intel hardware to demonstrate the power of AI in manufacturing.

Repository: [https://github.com/Harshpandey9984/ProcessIQ](https://github.com/Harshpandey9984/ProcessIQ)

## Core Features

- **Process Simulation Engine**: Mathematical models of manufacturing processes with physics-based simulation capabilities
- **Digital Twin Framework**: Real-time synchronization with production data and visualization of process states
- **AI Optimization Module**: Machine learning models for parameter optimization and process improvement
- **Decision Support Dashboard**: Interactive visualization of current vs. optimized processes and scenario planning tools
- **ML Model Management**: Train, deploy, and monitor machine learning models for defect prediction and process control

## Project Structure

```
digital-twin-platform/
├── app/
│   ├── api/             # FastAPI server implementation
│   │   ├── endpoints/   # API route handlers for each feature
│   ├── core/            # Application configuration and settings
│   ├── frontend/        # React-based user interface
│   │   ├── src/
│   │       ├── components/ # Reusable UI components
│   │       ├── pages/      # Main application pages
│   │       ├── services/   # API client services
│   ├── models/          # ML models for optimization and prediction
│   ├── simulation/      # Process simulation engine
│   └── optimization/    # AI optimization algorithms
├── data/                # Sample datasets and synthetic data generators
└── docs/                # Documentation
```

## Getting Started

### Local Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Harshpandey9984/ProcessIQ.git
   cd ProcessIQ
   ```

2. **Start the Platform**:
   ```bash
   ./start_platform.bat
   ```

3. **Access the Application**:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8001](http://localhost:8001)
   - API Documentation: [http://localhost:8001/docs](http://localhost:8001/docs)

4. **Login Credentials**:
   - Admin: admin@example.com / password
   - User: user@example.com / password

3. **Start the Frontend**:
   ```bash
   cd app/frontend
   npm install
   npm start
   ```

### Docker Deployment

Use Docker Compose to run the entire stack:

```bash
docker-compose up -d
```

This will start the following services:
- Backend API (FastAPI) on port 8000
- Frontend (React) on port 3000
- PostgreSQL database on port 5432
- InfluxDB time series database on port 8086
- MinIO object storage on ports 9000/9001

## Intel Hardware Optimizations

This project leverages several Intel-specific libraries and technologies:
- **Intel OpenVINO**: Accelerates ML model inference for real-time predictions
- **Intel DAAL**: Enhances machine learning algorithm performance
- **Intel MKL**: Optimizes mathematical computations in simulations
- **Intel oneAPI**: Provides hardware acceleration across different Intel architectures
- **Intel AVX-512**: Accelerates vector operations for physics-based simulations

## Key Components Added

- **Models Page**: ML model management interface for training, deployment, and monitoring
- **Settings Page**: Platform configuration with Intel hardware optimization settings
- **API Services**: React service modules for communicating with backend endpoints
- **Data Visualization**: Components for real-time monitoring and result visualization
- **Docker Configuration**: Containerized deployment setup for the entire platform

## License

This project is part of the Intel Hackathon and is for demonstration purposes.
>>>>>>> master
