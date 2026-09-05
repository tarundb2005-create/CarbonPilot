# CarbonPilot
# CarbonPilot 🌱

### Carbon-Aware Workload Scheduling with Adaptive Feedback

CarbonPilot is a carbon-aware workload scheduling engine designed to reduce the operational carbon footprint of cloud and Kubernetes workloads without violating workload deadlines.

Instead of simply reacting to the current grid carbon intensity, CarbonPilot combines:

- Carbon-intensity forecasts
- Workload energy estimation
- Deadline-aware scheduling
- Workload-level carbon estimation
- Execution feedback
- Adaptive workload energy profiles

The long-term goal is to create an attribution-in-the-loop control system:


Workload
   ↓
Energy + Carbon Prediction
   ↓
Carbon-Aware Scheduler
   ↓
RUN / DEFER
   ↓
Workload Execution
   ↓
Actual Energy / Carbon
   ↓
Workload-Level Feedback
   ↓
Prediction Error
   ↓
Adaptive Profile Update
   ↓
Improved Next Prediction

🚀 Problem

Modern cloud infrastructure and AI workloads consume significant amounts of electricity.
Most carbon-aware computing approaches make scheduling decisions using external carbon-intensity signals:
Carbon Intensity → Scheduler → Workload
However, the actual energy consumption of workloads varies significantly depending on:
CPU requirements
Memory usage
Runtime
Hardware
Workload type
Execution conditions
This creates a gap between:
Predicted workload impact
and
Actual workload impact
CarbonPilot addresses this gap by introducing workload-level feedback into the scheduling process.

💡 Solution

CarbonPilot estimates the energy and carbon impact of a workload before execution and determines whether it should run immediately or be deferred to a lower-carbon execution window.
After execution, actual workload measurements can be submitted to CarbonPilot.
The system calculates the prediction error and learns a correction factor for that workload.
The learned factor is then automatically applied to future predictions.
Example
Initial prediction:
Predicted Energy = 0.048 kWh
Actual Energy    = 0.060 kWh
Prediction Error = +25%
CarbonPilot learns:
Energy Factor = 1.25
Next prediction:
0.048 × 1.25 = 0.060 kWh
This creates an adaptive feedback loop instead of relying on a static energy model.

🧠 Key Innovation

CarbonPilot is not simply a carbon-aware scheduler.
The core idea is:
Workload carbon attribution → feedback error → adaptive scheduling
The system is designed around three layers:
1. Prediction
Estimate workload energy and CO₂e before execution.
2. Decision
Select a lower-carbon execution window while respecting the workload deadline.
3. Learning
Compare predicted and actual workload energy/carbon and update the workload profile.
             ┌──────────────────────┐
             │ CarbonPilot Controller│
             └───────────┬──────────┘
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
      Prediction      Scheduling      Learning
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                  Workload Execution
                         ↓
                  Actual Measurement
                         ↓
                    Feedback
                         ↓
                  Profile Update
⚙️ Current Features

The current MVP implements:
 FastAPI backend
 Workload submission API
 Carbon forecast model
 Energy estimation
 CO₂e calculation
 Deadline-aware scheduling
 RUN / DEFER decisions
 Recommended delay calculation
 Workload-level feedback
 Energy prediction error calculation
 CO₂e prediction error calculation
 Adaptive workload energy correction factor
 Learned factor applied to future predictions
 Workload profile API
 
🏗️ Architecture
                       CarbonPilot
                           │
                           ▼
                 ┌───────────────────┐
                 │  FastAPI Gateway  │
                 └─────────┬─────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
       Workload API   Feedback API   Profile API
             │             │
             ▼             ▼
       ┌──────────┐   ┌──────────────┐
       │ Scheduler│   │ Feedback     │
       │          │   │ Engine       │
       └────┬─────┘   └──────┬───────┘
            │                │
            ▼                ▼
     Carbon Forecast    Prediction Error
            │                │
            ▼                ▼
      RUN / DEFER       Learned Factor
            │                │
            └────────┬───────┘
                     ▼
              Future Prediction
              
📁 Project Structure
CarbonPilot/
│
├── backend/
│   │
│   ├── app/
│   │   ├── main.py
│   │   ├── scheduler.py
│   │   ├── carbon.py
│   │   ├── energy.py
│   │   ├── feedback.py
│   │   ├── schemas.py
│   │   └── services/
│   │       └── carbon_service.py
│   │
│   └── requirements.txt
│
├── .gitignore
└── README.md

🛠️ Technology Stack
Backend
Python
FastAPI
Uvicorn
Pydantic
Scheduling
Carbon-intensity forecasting
Deadline-aware window selection
Energy estimation
CO₂e estimation
Adaptive correction factors
Planned Infrastructure
Kubernetes
Container-level energy telemetry
Kepler integration
Persistent workload profiles
Real-time carbon-intensity APIs

🚀 Getting Started
1. Clone the repository
git clone https://github.com/tarundb2005-create/CarbonPilot.git
cd CarbonPilot
2. Create a virtual environment
python3 -m venv .venv
3. Activate the environment
macOS / Linux
source .venv/bin/activate
Windows
.venv\Scripts\activate
4. Install dependencies
cd backend
pip install -r requirements.txt
5. Start the API
uvicorn app.main:app --reload
The API will be available at:
http://127.0.0.1:8000
Interactive API documentation:
http://127.0.0.1:8000/docs

📡 API Endpoints
Health Check
GET /health
Example response:
{
  "status": "healthy",
  "service": "CarbonPilot"
}
Submit Workload
POST /workloads
CarbonPilot evaluates the workload against available carbon-intensity windows and returns a scheduling decision.
Example:
{
  "name": "ml-training-01",
  "cpu": 2,
  "memory_gb": 4,
  "estimated_runtime_minutes": 30,
  "deadline_minutes": 180
}
Example response:
{
  "workload": "ml-training-01",
  "decision": "DEFER",
  "recommended_delay_minutes": 90,
  "predicted_energy_kwh": 0.048,
  "predicted_co2e_kg": 0.0144,
  "carbon_intensity_g_per_kwh": 300,
  "reason": "A lower-carbon execution window is available without violating the deadline."
}

🔄 Feedback API

After execution, actual workload measurements can be submitted:
POST /feedback
Example:
{
  "workload_name": "ml-training-01",
  "predicted_energy_kwh": 0.048,
  "actual_energy_kwh": 0.060,
  "predicted_co2e_kg": 0.0144,
  "actual_co2e_kg": 0.018
}
CarbonPilot calculates:
Energy Error = +25%
CO₂e Error   = +25%
Learned Factor = 1.25
Example response:
{
  "workload_name": "ml-training-01",
  "predicted_energy_kwh": 0.048,
  "actual_energy_kwh": 0.06,
  "energy_error_percent": 25,
  "predicted_co2e_kg": 0.0144,
  "actual_co2e_kg": 0.018,
  "co2e_error_percent": 25,
  "updated_energy_factor": 1.25,
  "message": "Prediction profile updated using actual workload measurements."
}

📊 Workload Profiles

CarbonPilot stores learned workload energy correction factors.
GET /profiles
Example:
[
  {
    "workload_name": "ml-training-01",
    "energy_factor": 1.25,
    "status": "LEARNED"
  }
]
Future predictions for the same workload automatically use the learned factor.
🔬 Adaptive Feedback Example
First execution
Prediction
   ↓
0.048 kWh
   ↓
Actual execution
   ↓
0.060 kWh
   ↓
Error = +25%
   ↓
Learn factor = 1.25
Next execution
Base estimate
   ↓
0.048 kWh
   ↓
Apply learned factor
   ↓
0.048 × 1.25
   ↓
0.060 kWh
This demonstrates the fundamental adaptive-learning mechanism of CarbonPilot.
📈 Scalability
CarbonPilot is designed as a modular control layer rather than a replacement for the underlying scheduler.
The architecture can scale from:
Single workload
      ↓
Multiple workloads
      ↓
Kubernetes cluster
      ↓
Multi-node cluster
      ↓
Multi-region infrastructure
The scheduler can eventually integrate with:
Kubernetes
Kubernetes Jobs
Batch workloads
ML training workloads
AI inference workloads
CI/CD workloads
Cloud compute infrastructure
Persistent storage can replace the current in-memory workload profiles as the system moves toward production deployment.

🔐 Security Considerations

The current MVP focuses on the scheduling and learning engine.
Production deployment will add:
API authentication
Role-based access control
Secure telemetry collection
Input validation
Rate limiting
Audit logs
Encrypted communication
Secure Kubernetes service accounts
Tenant isolation

🗺️ Roadmap

Phase 1 — MVP
 Carbon-aware scheduling
 Energy estimation
 Deadline constraints
 CO₂e estimation
 Feedback API
 Adaptive workload profiles
 
Phase 2 — Real Execution

 Execute real workloads
 Collect actual resource usage
 Automatic feedback generation
 Remove manual feedback dependency
 
Phase 3 — Kubernetes

 Kubernetes Job integration
 Scheduler/controller integration
 Pod-level workload attribution
 Node-level energy telemetry
 
Phase 4 — Advanced Carbon Intelligence

 Real-time carbon-intensity APIs
 Carbon forecasting
 Uncertainty-aware scheduling
 Multi-node scheduling
 Multi-region scheduling
 Cost + carbon + SLO optimization
 
Phase 5 — Production

 Persistent workload profiles
 Authentication
 Multi-tenant support
 Monitoring
 Auditability
 Production deployment
 
🎯 Target Users

CarbonPilot is primarily designed for organizations operating:
Cloud infrastructure
Kubernetes clusters
AI/ML workloads
Batch processing systems
HPC workloads
CI/CD infrastructure
Large-scale compute platforms
Potential users include:
Platform engineering teams
DevOps teams
Cloud infrastructure teams
ML infrastructure teams
Sustainability engineering teams
Data-center operators

🌍 Expected Impact

CarbonPilot aims to reduce operational carbon emissions by intelligently shifting flexible workloads toward cleaner execution windows while respecting deadlines and operational constraints.
The system focuses on a practical principle:
Don't just predict carbon. Learn from what actually happened.

⚠️ Current Limitations

The current MVP uses:
In-memory workload profiles
Simulated/local carbon forecast data
Estimated workload energy
API-submitted actual measurements
It does not yet claim production-grade energy measurement or automatic Kubernetes execution.
These are part of the next implementation phases.

🏆 Hackathon Focus
CarbonPilot's core technical contribution is an adaptive carbon-aware scheduling loop:
Predict
   ↓
Schedule
   ↓
Execute
   ↓
Measure
   ↓
Attribute
   ↓
Compare
   ↓
Learn
   ↓
Schedule Better
The objective is to move carbon-aware computing from a static forecast-following system toward an adaptive, workload-aware control system.
📄 License
This project is currently developed as a hackathon prototype.

### One important point

I deliberately wrote the README so we **don't overclaim**.

For the hackathon, that's valuable. We should clearly distinguish:

**Already implemented**
→ FastAPI + scheduler + feedback + adaptive factor.

**Next implementation**
→ real workload execution + telemetry + automatic attribution.

That makes the GitHub repository credible when judges inspect it.

After saving it as `README.md`, commit and push:

bash
git add README.md
git commit -m "docs: add project README"
git push
