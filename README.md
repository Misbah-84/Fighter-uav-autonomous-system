# Fixed-Wing Fighter UAV Autonomous Flight Stack & Design Framework

An enterprise-grade, multi-disciplinary autonomous flight stack and systems engineering framework developed for high-speed fixed-wing UAV operations. This repository contains edge AI target tracking pipelines, cascaded flight control algorithms, and structural validation workflows optimized for dynamic mission environments requiring real-time vision-in-the-loop navigation.

---

# 🚀 Technical Architecture Overview

The system architecture decouples high-throughput computer vision processing from deterministic flight stabilization control loops, establishing a robust, low-latency edge computing node directly onboard the air vehicle.

```text
                 [ IMX219 8MP Camera ]
                       │ (CSI-2)
                       ▼
┌──────────────────────────────────────────────────────────────┐
│ NVIDIA Jetson Orin Nano Super (Edge Compute Node)            │
│                                                              │
│ • TensorRT Optimized YOLO26s-OBB (~11 ms inference)          │
│ • ByteTrack Multi-Target Association Pipeline                │
│ • Pyzbar QR Parser with Perspective Correction               │
└──────────────────────────────┬───────────────────────────────┘
                               │
                    MAVLink 2 over UART
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│ Pixhawk Cube Orange + Here 4 GPS                             │
│                                                              │
│ • TECS Glide Pitch Controller                               │
│ • Cascaded PD Visual Servoing                               │
│ • Real-Time Crab-Angle Wind Compensation                    │
└──────────────────────────────────────────────────────────────┘
```

---

# 🛠️ Key Features & Engineering Modules

## 1. Computer Vision & Target Tracking Pipeline

### Oriented Bounding Boxes (OBB)

Implements YOLO26s-OBB optimized using NVIDIA TensorRT, enabling accurate estimation of rival UAV heading and bank angle during aggressive maneuvers.

### Robust Multi-Object Tracking

Integrated with ByteTrack to maintain stable object identities during rapid airframe rotations and temporary occlusions.

### Dynamic QR Capture Engine

Uses Pyzbar enhanced with:

- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Perspective correction
- Motion blur compensation

to decode QR markers during high-speed dives of **22 to 28 m/s** under varying lighting conditions.

---

## 2. Guidance, Navigation & Control (GNC)

### Cascaded PD Visual Servoing

A closed-loop controller that converts camera pixel errors:

- \(e_x\)
- \(e_y\)

directly into roll and pitch commands for rapid visual target alignment.

### Total Energy Control System (TECS)

Controls throttle and pitch allocation during terminal dive phases while maintaining structural and kinetic safety margins.

### Crosswind Compensation

Uses EKF3 wind estimation from Pixhawk to compute crab angle corrections, ensuring the camera remains aligned with the ground target.

---

## 3. Dynamic Air Defense Avoidance

### Tangential Bypass Routing

A hybrid autonomous routing module that:

- Receives dynamic no-fly zone updates via UDP
- Generates tangential bypass trajectories
- Injects temporary waypoints through MAVLink

### Fail-Safe Intervention

Dual redundant manual override through low-latency 5.8 GHz analog FPV whenever telemetry latency exceeds predefined safety limits.

---

## 4. Structural Integrity Validation

The airframe has been validated using ANSYS Static Structural Analysis.

Results for a simulated **5G emergency pull-out maneuver**:

| Parameter | Value |
|-----------|-------|
| Peak von Mises Stress | **13.56 MPa** |
| Critical Regions | Wing roots and horizontal stabilizer joints |
| Result | Large structural safety margin |

---

# 📊 System Components & Bill of Materials

| Category | Component | Interface | Description |
|----------|-----------|-----------|-------------|
| Compute | NVIDIA Jetson Orin Nano Super | UART / Ethernet | Edge AI execution and vision processing |
| Autopilot | Pixhawk Cube Orange + Here 4 GPS | MAVLink / CAN | Flight stabilization and navigation |
| Camera | Yahboom IMX219 8MP Camera | CSI-2 | High-resolution visual tracking |
| Telemetry | RFD900x Radio Link | UART / 915 MHz | Long-range telemetry communication |
| Network | Ubiquiti Bullet AC | Ethernet / 5 GHz | High-bandwidth onboard networking |
| Propulsion | T-Motor AT5220-B KV380 + 115A ESC | PWM / XT60 | Brushless propulsion system |

---

# 💻 Getting Started

## Prerequisites

- JetPack SDK 6.0+
- CUDA 12.x
- TensorRT
- OpenCV with CUDA support
- Python 3.10+
- ArduPilot or PX4
- MAVProxy or DroneKit-Python

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/fighter-uav-autonomous-system.git

cd fighter-uav-autonomous-system
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Compile the TensorRT engine:

```bash
python scripts/compile_engine.py \
    --weights weights/yolo26s-obb.onnx \
    --output weights/yolo26s-obb.engine
```

---

## Running the Onboard Stack

Start the autonomous mission supervisor:

```bash
python main_supervisor.py \
    --camera /dev/video0 \
    --baud 921600 \
    --fc /dev/ttyTHS1
```

---

