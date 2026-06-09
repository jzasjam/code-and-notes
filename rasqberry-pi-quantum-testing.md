# RasQberry Two — Event Preparation Guide
### Introduction to Quantum Computing with the IBM RasQberry Pi

---

## About This Guide

This guide is written for event organisers running an introductory Quantum Computing session using a **RasQberry Two** setup (a 3D-printed functional model of IBM Quantum System Two, running on a Raspberry Pi 5 with Qiskit). It also covers the **Raspberry Pi AI HAT+** (Hailo-8L/8 accelerator) and provides a simple CNN walkthrough to contrast classical and quantum AI approaches.

The guide is structured in three parts:

1. **Understanding the Setup** — what the hardware represents and why it matters
2. **Demo Walkthroughs** — what each built-in demo shows, and how to explain it to participants
3. **AI HAT+ CNN Example** — a simple convolutional neural network demo to run on the accelerator

---

## Part 1: Understanding the Setup

### 1.1 What is RasQberry Two?

The RasQberry Two is an **educational functional model** of IBM's Quantum System Two — a real, cryogenically cooled quantum computer. The 3D-printed housing replicates the iconic cylindrical form factor of the real machine (which keeps qubits near absolute zero). Inside is a Raspberry Pi 5, running **Qiskit** (IBM's open-source quantum computing SDK), which can simulate quantum circuits locally or (with an IBM account) submit real jobs to IBM's quantum cloud.

**Talking point for participants:**  
> "The real IBM Quantum System Two in the lab is kept at about 15 millikelvin — colder than outer space — to stop thermal noise from disrupting the qubits. Our model runs at room temperature and uses simulation to show the same quantum behaviour."

### 1.2 Key Quantum Computing Concepts

Before running demos, make sure you're comfortable explaining these core ideas:

**Qubit**  
A classical bit is either 0 or 1. A qubit can be in a *superposition* of both states simultaneously — described by a complex probability amplitude — until it is measured. At measurement it "collapses" to 0 or 1.

**Superposition**  
The ability of a qubit to exist in multiple states at once. Applying a Hadamard gate (H) to a |0⟩ qubit puts it into an equal superposition of |0⟩ and |1⟩, giving a 50/50 measurement probability — but critically, quantum algorithms can exploit the *phases* of those states before collapsing them.

**Entanglement**  
Two qubits can be correlated in a way that has no classical equivalent: measuring one instantly determines the outcome of measuring the other, regardless of distance. The GHZ state is a canonical example.

**Interference**  
Quantum algorithms use constructive and destructive interference (like waves) to amplify paths leading to the correct answer and cancel paths leading to wrong answers.

**Quantum Gates**  
Quantum gates manipulate qubits analogously to classical logic gates. Common ones include:
- **X gate**: Flips |0⟩ to |1⟩ and vice versa (quantum NOT)
- **H gate (Hadamard)**: Puts a qubit into superposition
- **Z gate**: Flips the phase of |1⟩
- **CNOT gate**: Flips the second qubit only if the first is |1⟩ (used to create entanglement)

### 1.3 Hardware Overview

| Component | What It Does |
|---|---|
| **Raspberry Pi 5** | The main computer; runs Qiskit and all demos |
| **3D-printed model** | Scale replica of IBM Quantum System Two housing |
| **WS2812 LED panels (×4)** | Display quantum circuit measurement results visually |
| **AI HAT+ (Hailo-8L or Hailo-8)** | Neural network inference accelerator for classical AI demos |
| **GPIO pin 18** | Controls the LED strips |

### 1.4 Connecting to the Pi

SSH or VNC into the Pi using:
- **Username:** `rasqberry`
- **Password:** `Qiskit1!`

To access the demo menu:
```bash
sudo raspi-config
# Select: 0 RasQberry → Quantum Computing Demos
```

Activate the Qiskit virtual environment for manual code:
```bash
source /home/rasqberry/RasQberry-Two/venv/RQB2/bin/activate
```

Verify Qiskit installation:
```bash
pip list | grep qiskit
```

---

## Part 2: Demo Walkthroughs

### 2.1 Bloch Sphere

**Launch:** Desktop icon **"Grok Bloch"**, or:
```bash
cd ~/RasQberry-Two
source venv/RQB2/bin/activate
cd demos/grok-bloch
python3 grok_bloch.py
# Then open browser: http://localhost:5000
```

**What it shows:**  
An interactive 3D visualisation of a single qubit's quantum state. The qubit is represented as a vector (arrow) on a unit sphere:

| Position | Meaning |
|---|---|
| North pole (top) | Pure |0⟩ state |
| South pole (bottom) | Pure |1⟩ state |
| Equator | Equal superposition (50/50 measurement chance) |
| X-axis | |+⟩ and |−⟩ (Hadamard basis states) |
| Y-axis | Circular basis states |i⟩ and |−i⟩ |

**What participants do:**  
Click gate buttons (X, Y, Z, H, S, T, Rx, Ry, Rz) and watch the arrow move on the sphere in real time.

**Suggested sequence for guided exploration:**
1. Start at |0⟩ (arrow points up). Apply **H** — arrow moves to the equator (+X axis). This is superposition.
2. Apply **H** again — returns to |0⟩. The two H gates cancel. Interference in action.
3. Apply **X** — arrow flips to south pole: |1⟩. This is the quantum NOT gate.
4. Start fresh, apply **H**, then **Z** — arrow moves to the −X axis (the |−⟩ state). The Z gate added a phase but didn't change measurement probability.
5. Demonstrate that phase is *invisible to measurement alone* but crucial for quantum algorithms.

**Key teaching point:**  
The Bloch sphere is only valid for a **single qubit**. Multi-qubit states like entanglement cannot be shown on one sphere — this is a fundamental limit, not a software one.

---

### 2.2 Raspberry Tie (Quantum Circuit → LED Display)

**Launch:** Desktop icon **"Raspberry Tie"**, or:
```bash
cd ~/RasQberry-Two
source venv/RQB2/bin/activate
python3 RQB2-bin/quantum-raspberry-tie.py -int
```

**What it shows:**  
Quantum circuits are executed (on the local Aer simulator, or IBM Quantum cloud hardware), and measurement results are displayed **live on the LED array**. Each LED pixel represents one qubit's measurement: **blue = |1⟩, red = |0⟩**. The layout of the LEDs mirrors the *actual physical topology* of IBM quantum processors.

**Display modes and what they represent:**

| Mode | Qubits | Processor topology |
|---|---|---|
| Bowtie | 5 | IBM's original 5-qubit processor (circa 2016) |
| Tee | 5 | Later 5-qubit layout with lower noise connectivity |
| Hex (heavy-hex) | 12 | Modern IBM processors (Falcon, Heron era) |
| 16-qubit rows | 16 | IBM experimental 16-qubit layout |

**Why topology matters:**  
On a real quantum computer, not every qubit is directly connected to every other. Two-qubit gates (like CNOT) can only be applied between physically adjacent qubits. The "heavy-hex" layout is IBM's current preferred topology because it reduces unwanted cross-qubit interference.

**Suggested demo flow:**
1. Run with the local **Aer simulator** first — results are instant and noise-free.
2. Discuss what "noise-free simulation" means vs real hardware.
3. If an IBM Quantum account is available, submit to real hardware and compare the results — real qubits produce slightly different distributions due to decoherence and gate errors.

**Key teaching point:**  
Quantum measurement is probabilistic. Running the same circuit multiple times gives a *distribution* of results — the LED display changes each time. This is not a bug; it is fundamental to quantum mechanics.

---

### 2.3 GHZ State Demo (Multi-Qubit Entanglement)

**Launch:** Via raspi-config menu or desktop shortcut.

**What it shows:**  
The **GHZ (Greenberger–Horne–Zeilinger) state** is a maximally entangled multi-qubit state. For 3 qubits, the state is:

```
|GHZ⟩ = (|000⟩ + |111⟩) / √2
```

This means when you measure, you get *either* all zeros or all ones — never a mix. The RasQberry demo can simulate GHZ states of up to **192 qubits** (4×4×12), displayed via the integrated LED.

**What it demonstrates:**  
- Entanglement: qubits are correlated even though they were prepared independently
- Scale: quantum computers can represent exponentially large state spaces (2^192 states from 192 qubits, impossible to store classically)

**Suggested explanation:**
> "If we measured qubit 1 and got 0, we'd instantly know every other qubit is also 0 — without measuring them. That's entanglement. The correlation exists in the quantum state, not in any signal passing between qubits."

---

### 2.4 Quantum Fractals

**Launch:** Desktop icon **"Fractals"**, or via the demo menu.

**What it shows:**  
Julia set fractals are animated using quantum-generated parameters. A Qiskit circuit produces a series of measurements, and those measurement outcomes (which are inherently random due to superposition) are used to seed the parameters of the Julia set equation, creating a continuously evolving fractal animation.

**What it demonstrates:**  
- Quantum randomness: unlike pseudo-random number generators on classical computers, quantum measurement is *genuinely* random (according to our best physical theories)
- A creative application of quantum output — not just computation, but generative art

**Key teaching point:**  
Quantum computers don't always outperform classical ones at *speed* — they offer new approaches. Here, true quantum randomness drives an application that a classical computer could only approximate with pseudo-randomness.

---

### 2.5 Quantum Lights Out

**Launch:** Desktop icon, or via the demo menu.

**What it shows:**  
A quantum implementation of the classic *Lights Out* puzzle, where toggling a light also toggles its neighbours. The RasQberry version uses a quantum algorithm (based on linear algebra over GF(2)) to *solve* the puzzle, then visualises the solution step-by-step on the LED array.

**Why it's interesting:**  
Lights Out has a known classical solution, but it illustrates how quantum algorithms can express and solve systems of linear equations — a foundation of more powerful algorithms like **HHL (Harrow-Hassidim-Lloyd)**, which can solve linear systems exponentially faster than classical methods under certain conditions.

---

### 2.6 Qoffee Maker (Optional / Fun Demo)

**What it shows:**  
Participants design a quantum circuit; the measurement result determines which drink they receive (if connected to a physical dispenser). This gamifies the concept that quantum measurement outcomes are probabilistic and that circuit design determines the *probability distribution* of outcomes.

---

## Part 3: AI HAT+ — Simple CNN Example

### 3.1 About the Raspberry Pi AI HAT+

The AI HAT+ attaches to the Raspberry Pi 5's PCIe Gen 3 interface and contains a **Hailo neural network inference accelerator**. It is available in:

- **13 TOPS** variant (Hailo-8L) — entry-level, good for object detection, classification, segmentation
- **26 TOPS** variant (Hailo-8) — handles larger models and multiple concurrent networks

When a current Raspberry Pi OS image is running, the Pi automatically detects the Hailo accelerator. It is particularly suited to running **CNNs (Convolutional Neural Networks)** for vision tasks locally, without cloud dependency.

**Why include this at a quantum computing event?**  
Contrasting *classical neural networks* (which the AI HAT+ accelerates) with *quantum circuits* helps participants understand what quantum computing does and doesn't replace. Both are "computing with probability" in a loose sense, but via entirely different mechanisms.

---

### 3.2 Simple CNN Example — MNIST Digit Classifier

This example trains a small CNN to recognise handwritten digits (the MNIST dataset — the standard "hello world" of deep learning), then runs inference on the Raspberry Pi using the AI HAT+. It runs entirely on the Pi with no cloud required.

**Step 1: Set up the environment**

Open a terminal on the Pi and create a fresh virtual environment for the AI demo:

```bash
python3 -m venv ~/cnn_demo_env
source ~/cnn_demo_env/bin/activate
pip install tensorflow numpy matplotlib pillow
```

> **Note on the AI HAT+:** The Hailo accelerator uses Hailo's `hailort` runtime and a model compiler to convert trained models to `.hef` format. For simplicity, this demo runs TensorFlow inference on the **Pi CPU** first, so participants can see training and inference work without HAT+ setup complexity. Section 3.4 covers accelerating it with the HAT+.

---

**Step 2: Create the training script**

Save the following as `~/cnn_demo_env/train_mnist_cnn.py`:

```python
"""
Simple CNN for MNIST digit classification
Event demo: Introduction to Convolutional Neural Networks
Runs on Raspberry Pi 5 (CPU). For AI HAT+ acceleration, see convert step.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Pi
import matplotlib.pyplot as plt
import os

print("TensorFlow version:", tf.__version__)
print("Loading MNIST dataset...")

# --- Load and preprocess data ---
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalise pixel values to [0, 1] and add channel dimension
x_train = x_train.astype('float32') / 255.0
x_test  = x_test.astype('float32') / 255.0
x_train = x_train[..., np.newaxis]  # Shape: (60000, 28, 28, 1)
x_test  = x_test[..., np.newaxis]   # Shape: (10000, 28, 28, 1)

print(f"Training samples: {len(x_train)}, Test samples: {len(x_test)}")

# --- Build the CNN ---
model = models.Sequential([
    # First convolutional block
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),

    # Second convolutional block
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),

    # Classifier head
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')  # 10 output classes (digits 0-9)
])

model.summary()

# --- Compile and train ---
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("\nTraining... (this takes ~5-10 minutes on Pi CPU)")
history = model.fit(
    x_train, y_train,
    epochs=5,
    batch_size=64,
    validation_split=0.1,
    verbose=1
)

# --- Evaluate ---
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\nTest accuracy: {test_acc:.4f}  ({test_acc*100:.1f}%)")

# --- Save model ---
model.save(os.path.expanduser('~/cnn_demo_env/mnist_cnn.keras'))
print("Model saved to ~/cnn_demo_env/mnist_cnn.keras")

# --- Plot training history ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(history.history['accuracy'], label='Training')
ax1.plot(history.history['val_accuracy'], label='Validation')
ax1.set_title('Model Accuracy')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Accuracy')
ax1.legend()
ax2.plot(history.history['loss'], label='Training')
ax2.plot(history.history['val_loss'], label='Validation')
ax2.set_title('Model Loss')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Loss')
ax2.legend()
plt.tight_layout()
plt.savefig(os.path.expanduser('~/cnn_demo_env/training_history.png'))
print("Training plot saved to ~/cnn_demo_env/training_history.png")
```

Run the training:
```bash
cd ~/cnn_demo_env
python train_mnist_cnn.py
```

Expected output: ~98% test accuracy after 5 epochs.

---

**Step 3: Run inference on new images**

Save the following as `~/cnn_demo_env/run_inference.py`:

```python
"""
Run inference with the trained MNIST CNN.
Shows example predictions with visualisation.
"""

import numpy as np
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# Load model
model = tf.keras.models.load_model(
    os.path.expanduser('~/cnn_demo_env/mnist_cnn.keras')
)

# Load test set
(_, _), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_test = x_test.astype('float32') / 255.0
x_test_expanded = x_test[..., np.newaxis]

# Pick 16 random test images
indices = np.random.choice(len(x_test), 16, replace=False)
images  = x_test_expanded[indices]
labels  = y_test[indices]

# Predict
predictions = model.predict(images, verbose=0)
predicted_classes = np.argmax(predictions, axis=1)
confidences       = np.max(predictions, axis=1)

# Plot
fig, axes = plt.subplots(4, 4, figsize=(8, 8))
for i, ax in enumerate(axes.flat):
    ax.imshow(images[i].squeeze(), cmap='gray')
    correct = predicted_classes[i] == labels[i]
    colour  = 'green' if correct else 'red'
    ax.set_title(
        f"Pred: {predicted_classes[i]} ({confidences[i]*100:.0f}%)\nTrue: {labels[i]}",
        color=colour, fontsize=8
    )
    ax.axis('off')

plt.suptitle('CNN Inference on MNIST — green=correct, red=wrong', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.expanduser('~/cnn_demo_env/inference_results.png'))
print("Saved inference_results.png")
print(f"\nResults: {np.sum(predicted_classes == labels)}/16 correct")
```

Run inference:
```bash
python run_inference.py
```

Open the saved PNGs with the Pi's image viewer to see the results.

---

### 3.3 What Does the CNN Actually Do? (Explaining to Participants)

Use this explanation when walking participants through the code:

**Convolutional layers** scan across the image with small filters (3×3 pixel windows). Each filter learns to detect a feature — an edge, a curve, a corner. Early layers detect simple features; deeper layers combine them into complex patterns like "closed loop at the top" (digit 8) or "vertical stroke" (digit 1).

**Max pooling** reduces the spatial size, making the network tolerant of small shifts or distortions in where the digit appears.

**Dense layers** take the extracted features and learn which combination means digit 0, which means digit 1, and so on.

**Training** adjusts millions of numerical weights by comparing predictions to correct answers and nudging weights slightly using backpropagation — gradient descent on the loss function.

---

### 3.4 Accelerating with the AI HAT+ (Advanced)

The AI HAT+ uses Hailo's runtime to run models in `.hef` (Hailo Executable Format). To use it:

**Step 1: Install Hailo software**

On the Pi with the HAT+ attached:
```bash
# Check if HAT+ is detected
hailortcli fw-control identify
```

If not installed, follow the official Hailo documentation at https://hailo.ai/developer-zone/ (free account required to download).

**Step 2: Convert the TensorFlow model**

The Hailo Model Zoo and Dataflow Compiler convert standard formats (TFLite/ONNX) to `.hef`:

```bash
# First export to TFLite
python3 - <<'EOF'
import tensorflow as tf
model = tf.keras.models.load_model('/home/rasqberry/cnn_demo_env/mnist_cnn.keras')
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open('/home/rasqberry/cnn_demo_env/mnist_cnn.tflite', 'wb') as f:
    f.write(tflite_model)
print("Saved mnist_cnn.tflite")
EOF
```

Then use the Hailo Dataflow Compiler (requires the full Hailo SDK, typically on a more powerful machine) to compile to `.hef`, then copy back to the Pi.

**Step 3: Run inference via hailort**

```python
from hailo_platform import (HEF, VDevice, HailoStreamInterface,
                            InferVStreams, ConfigureParams)
import numpy as np

hef = HEF('mnist_cnn.hef')
with VDevice() as target:
    configure_params = ConfigureParams.create_from_hef(hef, interface=HailoStreamInterface.PCIe)
    network_groups = target.configure(hef, configure_params)
    network_group = network_groups[0]
    with InferVStreams(network_group, {}, {}) as infer_pipeline:
        # ... run inference batches
        pass
```

> **For event day:** Unless Hailo SDK setup is pre-completed, using the CPU TFLite path (Section 3.2) is more reliable for a live demo. The AI HAT+ is best demonstrated using the Pi's built-in `rpicam` object detection demos, which come pre-compiled:
>
> ```bash
> rpicam-hello -t 0 --post-process-file \
>   /usr/share/rpi-camera-assets/hailo_yolov8_inference.json
> ```
> This runs YOLOv8 object detection at real-time speeds using the HAT+.

---

## Part 4: Suggested Event Structure

### Option A: Guided Walkthrough (~60–90 minutes)

| Time | Activity |
|---|---|
| 0–10 min | Introduction: classical vs quantum computing, what a qubit is |
| 10–25 min | Bloch Sphere demo — participants apply gates and discuss superposition and phase |
| 25–40 min | Raspberry Tie — run circuits on Aer simulator, watch LED results, discuss probabilistic measurement |
| 40–50 min | GHZ demo — explain entanglement with scale demo up to 192 qubits |
| 50–60 min | Fractals or Lights Out — creative/applied demo |
| 60–80 min | AI HAT+ CNN demo — contrast with classical ML, run live object detection |
| 80–90 min | Q&A and open exploration |

### Option B: Explore-at-Your-Own-Pace (~90 minutes)

Set up stations:

| Station | Demo |
|---|---|
| 1 | Bloch Sphere (browser on Pi display) |
| 2 | Raspberry Tie (LED array) |
| 3 | GHZ state + Fractals |
| 4 | AI HAT+ live camera object detection |
| 5 | Guided Qiskit code — participants write their first quantum circuit |

### First Quantum Circuit (Station 5 worksheet)

Give participants this snippet to run:
```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Create a 2-qubit circuit
qc = QuantumCircuit(2, 2)

# Put qubit 0 into superposition
qc.h(0)

# Entangle qubit 0 and qubit 1 (Bell state)
qc.cx(0, 1)

# Measure both qubits
qc.measure([0, 1], [0, 1])

# Draw the circuit
print(qc.draw(output='text'))

# Simulate
simulator = AerSimulator()
job     = simulator.run(qc, shots=1024)
counts  = job.result().get_counts()
print("\nMeasurement results (1024 shots):")
print(counts)
```

**Expected output:**  
Roughly 50% `00` and 50% `11` — never `01` or `10`. This is a **Bell state**: the simplest form of entanglement. Ask participants: *"Why do we never see 01 or 10?"*

---

## Part 5: Troubleshooting Quick Reference

| Problem | Solution |
|---|---|
| Demo won't launch | `source venv/RQB2/bin/activate` first |
| Browser shows blank page | Navigate manually to `http://localhost:5000`; check `lsof -ti:5000` for port conflicts |
| LEDs not lighting | Check LED strip connected to GPIO pin 18; run `sudo raspi-config` and check LED demo |
| Qiskit import error | Check venv is active; run `pip list \| grep qiskit` |
| AI HAT+ not detected | Run `hailortcli fw-control identify`; ensure HAT+ is seated in PCIe M.2 slot |
| TFLite inference slow | Normal on CPU — 28×28 MNIST is fast; larger images take longer without HAT+ |
| IBM Quantum connection fails | Check internet connection; API token may have expired — regenerate at quantum.ibm.com |

---

## Useful Links

- RasQberry Two documentation: https://rasqberry.org
- Qiskit documentation: https://docs.qiskit.org
- IBM Quantum Learning (free courses): https://learning.quantum.ibm.com
- Raspberry Pi AI HAT+ product page: https://www.raspberrypi.com/products/ai-hat/
- Hailo developer zone: https://hailo.ai/developer-zone/
- Fun with Quantum (Jupyter notebooks): http://fun-with-quantum.org
- Quantum Paradoxes (Maria Violaris): https://www.mariaviolaris.com/quantum-paradoxes/

---

*RasQberry is an independent educational project. IBM®, IBM Quantum®, Qiskit®, and IBM Quantum System Two are trademarks of IBM Corporation. This guide is for educational use.*
