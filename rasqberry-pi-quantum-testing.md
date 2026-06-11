# RasQberry Two — Event Preparation Guide
## Introduction to Quantum Computing with the IBM RasQberry Pi

---

### About This Guide

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

**Notes:** 
Issues when launching - File Not Found as the Python script has been updated to v8 and Sense HAT emulator not displaying the LEDs.
I needed to launch the Quantum Raspberry Tie from the desktop twice to open the Sense HAT emulator, then used `cd /RasQberry-Two/demos/quantum-raspberry-tie` before lauching with `python QuantumRaspberryTie.v8_0.py`.  

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

**NOTE:** No demo or code given at https://rasqberry.org/03-quantum-computing-demos/01-demo-list/

Try...
```python
"""
GHZ State Demo — Multi-qubit Entanglement
For RasQberry Two event days.

Demonstrates a GHZ state: (|000...0⟩ + |111...1⟩) / √2
When measured, you always get ALL zeros or ALL ones — never a mix.
That is the signature of entanglement.
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import time

def build_ghz_circuit(n_qubits):
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(0)                          # Superposition on first qubit
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)              # Entangle each qubit to the next
    qc.measure(range(n_qubits), range(n_qubits))
    return qc

def run_ghz_demo(n_qubits=5, shots=1024):
    print(f"\n{'='*50}")
    print(f"  GHZ State Demo — {n_qubits} Qubits")
    print(f"{'='*50}")

    qc = build_ghz_circuit(n_qubits)
    print(qc.draw(output='text'))

    print(f"\nRunning {shots} measurements on Aer simulator...")
    simulator = AerSimulator()
    job    = simulator.run(qc, shots=shots)
    counts = job.result().get_counts()

    print("\nResults:")
    all_zeros = '0' * n_qubits
    all_ones  = '1' * n_qubits
    for state, count in sorted(counts.items(), key=lambda x: -x[1]):
        bar    = '█' * int(count / shots * 40)
        label  = " ← ALL ZEROS" if state == all_zeros else \
                 " ← ALL ONES"  if state == all_ones  else \
                 " ← (unexpected — noise?)"
        print(f"  |{state}⟩  {count:4d} shots  {bar}{label}")

    print(f"\nKey point: only |{'0'*n_qubits}⟩ and |{'1'*n_qubits}⟩ appear.")
    print("Measuring one qubit as 0 means ALL others must also be 0.")
    print("That correlation — with no classical explanation — is entanglement.\n")

if __name__ == "__main__":
    for n in [3, 5, 8]:
        run_ghz_demo(n_qubits=n, shots=1024)
        time.sleep(1)
```

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


## Part 3: Troubleshooting Quick Reference

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

### Useful Links

- RasQberry Two documentation: https://rasqberry.org
- Qiskit documentation: https://docs.qiskit.org
- IBM Quantum Learning (free courses): https://learning.quantum.ibm.com
- Raspberry Pi AI HAT+ product page: https://www.raspberrypi.com/products/ai-hat/
- Hailo developer zone: https://hailo.ai/developer-zone/
- Fun with Quantum (Jupyter notebooks): http://fun-with-quantum.org
- Quantum Paradoxes (Maria Violaris): https://www.mariaviolaris.com/quantum-paradoxes/

---

*RasQberry is an independent educational project. IBM®, IBM Quantum®, Qiskit®, and IBM Quantum System Two are trademarks of IBM Corporation. This guide is for educational use.*


---

## Part 4: AI HAT+ 

### INSTALL AI HAT+
https://www.raspberrypi.com/news/get-started-with-the-raspberry-pi-ai-hat/
https://www.raspberrypi.com/documentation/computers/ai.html#software

Update and upgrade and ensure firmware is >6 December 2023...
```bash
sudo apt update
sudo apt full-upgrade -y
sudo rpi-eeprom-update -a
sudo reboot
```

Install Dependencies...
```bash
sudo apt install dkms
sudo apt install hailo-all
sudo reboot
```

Verify after roboot
```bash
hailortcli fw-control identify
```

### 4.1 About the Raspberry Pi AI HAT+

The AI HAT+ attaches to the Raspberry Pi 5's PCIe Gen 3 interface and contains a **Hailo neural network inference accelerator**. It is available in:

- **13 TOPS** variant (Hailo-8L) — entry-level, good for object detection, classification, segmentation
- **26 TOPS** variant (Hailo-8) — handles larger models and multiple concurrent networks

When a current Raspberry Pi OS image is running, the Pi automatically detects the Hailo accelerator. It is particularly suited to running **CNNs (Convolutional Neural Networks)** for vision tasks locally, without cloud dependency.

**Why include this at a quantum computing event?**  
Contrasting *classical neural networks* (which the AI HAT+ accelerates) with *quantum circuits* helps participants understand what quantum computing does and doesn't replace. Both are "computing with probability" in a loose sense, but via entirely different mechanisms.

---

## Part 5: Raspberry Pi AI HAT+ — CNN Classification Demo Guide
### Running and Benchmarking MobileNet on the Hailo Accelerator

---

## 5.1 About This Guide

This guide covers running a **real CNN image classification demo** on the Raspberry Pi AI HAT+ (Hailo-8L or Hailo-8) without needing the full Hailo Dataflow Compiler or SDK conversion toolchain. It uses **DeGirum PySDK**, which provides pre-built `.hef` model files with integrated pre/post-processing, and builds up to a direct **CPU vs HAT+ speed comparison** that makes the value of the accelerator immediately tangible.

---

## 5.2 Prerequisites

Before starting, verify the AI HAT+ is detected by the Pi:

```bash
hailortcli fw-control identify
```

You should see output like:

```
Identifying board
Board Name: Hailo-8
Device Architecture: HAILO8L        ← 13 TOPS variant
  or
Device Architecture: HAILO8         ← 26 TOPS variant
```

If this command is not found, install the Hailo runtime first:

```bash
sudo apt install hailort python3-hailort
```

Then reboot and retry.

---

### Step 1: Set Up the Environment

Create a virtual environment for the AI HAT+ demos:

```bash
python3 -m venv ~/hailo_demo_env
source ~/hailo_demo_env/bin/activate
```

Install the required packages:

```bash
pip install degirum pillow numpy
pip install tensorflow   # needed for the CPU benchmark in Step 3
```

> **Note:** The first `pip install tensorflow` on the Pi can take 10–15 minutes. 

---

### Step 2: Download a Test Image

The demos below work on any JPEG or PNG. Download a simple test image to start with:

```bash
cd ~
wget -O test_image.jpg \
  "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"
```

You can substitute any image you like — the model classifies from 1000 ImageNet categories, so everyday photos of animals, vehicles, food, and objects all work well.

---

### Step 3: Single Image Classification on the HAT+

Save the following as `~/hailo_demo_env/hailo_classify.py`:

```python
"""
ImageNet image classification on Raspberry Pi AI HAT+
using DeGirum PySDK and a pre-built MobileNetV2 HEF.
No camera required — classifies any JPEG or PNG image.

Usage:
    python hailo_classify.py [path/to/image.jpg]
"""

import degirum as dg
import sys
import time

# Load MobileNetV2 from DeGirum's Hailo model zoo.
# On first run this downloads the .hef and postprocessor (~5MB).
# After that it runs fully offline from the local cache.
print("Loading model...")
zoo = dg.connect(dg.LOCAL, "degirum/hailo")

# Change device_id to "HAILO8" if you have the 26 TOPS variant
model = zoo.load_model(
    "mobilenet_v2--224x224_quant_hailort_hailo8l_1",
    device_id="HAILO8L"
)

# Use image path from command line, or default to test_image.jpg
image_path = sys.argv[1] if len(sys.argv) > 1 else "test_image.jpg"
print(f"Running inference on: {image_path}\n")

start  = time.perf_counter()
result = model(image_path)
elapsed = (time.perf_counter() - start) * 1000

print("Top 5 predictions:")
print(f"{'Rank':<6} {'Label':<45} {'Confidence':>10}")
print("-" * 63)
for i, r in enumerate(result.results[:5], 1):
    print(f"  {i:<4} {r['label']:<45} {r['score']*100:>8.1f}%")

print(f"\nInference time: {elapsed:.1f} ms")
```

Run it:

```bash
cd ~/hailo_demo_env
source ~/hailo_demo_env/bin/activate
python hailo_classify.py ~/test_image.jpg
```

**Expected output (example):**

```
Loading model...
Running inference on: /home/rasqberry/test_image.jpg

Top 5 predictions:
Rank   Label                                         Confidence
---------------------------------------------------------------
  1    golden retriever                                  82.4%
  2    Labrador retriever                                 9.1%
  3    kuvasz                                             2.3%
  4    clumber spaniel                                    1.8%
  5    Sussex spaniel                                     0.9%

Inference time: 4.2 ms
```

## 5.3 What is it doing?

MobileNetV2 is a **convolutional neural network** designed specifically for edge devices. It takes a 224×224 pixel image, passes it through a series of convolutional layers that detect progressively complex features (edges → textures → object parts → whole objects), and outputs a probability score across 1000 ImageNet categories. The HAT+ runs the convolutional layers in hardware at high speed — the CPU only handles loading the image and reading the result.

---

### Step 4: CPU vs HAT+ Speed Comparison

This is the most compelling demo — it runs the same MobileNetV2 model on the Pi CPU (via TensorFlow) and on the Hailo HAT+ (via DeGirum), then prints a direct comparison.

Save the following as `~/hailo_demo_env/hailo_vs_cpu.py`:

```python
"""
Speed comparison: CPU (TensorFlow) vs Hailo AI HAT+ (DeGirum)
Runs MobileNetV2 image classification on both backends and compares throughput.

Usage:
    python hailo_vs_cpu.py [path/to/image.jpg]
"""

import degirum as dg
import tensorflow as tf
import numpy as np
import time
import sys
from PIL import Image

IMAGE_PATH = sys.argv[1] if len(sys.argv) > 1 else "test_image.jpg"
N_RUNS     = 50  # number of inference passes to average over

print(f"Image: {IMAGE_PATH}")
print(f"Runs per backend: {N_RUNS}\n")

# Preprocess the image once for TensorFlow (224x224, normalised to [0,1])
img       = Image.open(IMAGE_PATH).convert("RGB").resize((224, 224))
img_array = np.array(img).astype("float32") / 255.0
img_batch = np.expand_dims(img_array, 0)

# ----------------------------------------------------------------
# CPU benchmark — TensorFlow MobileNetV2
# ----------------------------------------------------------------
print("=" * 50)
print("BACKEND 1: CPU (TensorFlow MobileNetV2)")
print("=" * 50)

print("Loading model...")
cpu_model = tf.keras.applications.MobileNetV2(weights="imagenet")

print("Warming up (1 run)...")
_ = cpu_model.predict(img_batch, verbose=0)

print(f"Benchmarking ({N_RUNS} runs)...")
start = time.perf_counter()
for _ in range(N_RUNS):
    cpu_preds = cpu_model.predict(img_batch, verbose=0)
cpu_time = (time.perf_counter() - start) / N_RUNS * 1000

decoded = tf.keras.applications.mobilenet_v2.decode_predictions(
    cpu_preds, top=3
)[0]
print(f"\nTop result: {decoded[0][1]} ({decoded[0][2]*100:.1f}%)")
print(f"Average inference time: {cpu_time:.1f} ms per image")

# ----------------------------------------------------------------
# HAT+ benchmark — DeGirum PySDK
# ----------------------------------------------------------------
print()
print("=" * 50)
print("BACKEND 2: AI HAT+ (Hailo via DeGirum PySDK)")
print("=" * 50)

print("Loading model...")
zoo   = dg.connect(dg.LOCAL, "degirum/hailo")
hailo = zoo.load_model(
    "mobilenet_v2--224x224_quant_hailort_hailo8l_1",
    device_id="HAILO8L"   # change to HAILO8 for 26 TOPS variant
)

print("Warming up (1 run)...")
_ = hailo(IMAGE_PATH)

print(f"Benchmarking ({N_RUNS} runs)...")
start = time.perf_counter()
for _ in range(N_RUNS):
    hailo_result = hailo(IMAGE_PATH)
hailo_time = (time.perf_counter() - start) / N_RUNS * 1000

top = hailo_result.results[0]
print(f"\nTop result: {top['label']} ({top['score']*100:.1f}%)")
print(f"Average inference time: {hailo_time:.1f} ms per image")

# ----------------------------------------------------------------
# Summary
# ----------------------------------------------------------------
speedup = cpu_time / hailo_time

print()
print("=" * 50)
print("  RESULTS SUMMARY")
print("=" * 50)
print(f"  CPU  (TensorFlow):  {cpu_time:7.1f} ms per image")
print(f"  HAT+ (Hailo):       {hailo_time:7.1f} ms per image")
print(f"  Speedup:            {speedup:7.1f}x faster on HAT+")
print()
if speedup >= 10:
    print("  The AI HAT+ is more than 10x faster than the CPU.")
elif speedup >= 5:
    print("  The AI HAT+ is significantly faster than the CPU.")
else:
    print("  The AI HAT+ shows a measurable speedup over CPU.")
print("=" * 50)
```

Run it:

```bash
python hailo_vs_cpu.py ~/test_image.jpg
```

This takes a few minutes to complete (the CPU benchmark is the slow part). Typical results on Pi 5:

```
==================================================
  RESULTS SUMMARY
==================================================
  CPU  (TensorFlow):    87.4 ms per image
  HAT+ (Hailo):          4.1 ms per image
  Speedup:              21.3x faster on HAT+
==================================================
```

---

### Step 5: Batch Classification Across Multiple Images

For a richer demo, classify a whole folder of images and display a ranked results table. This illustrates how an edge AI system could process a stream of inputs in real time.

Save as `~/hailo_demo_env/hailo_batch.py`:

```python
"""
Batch image classification on Hailo AI HAT+
Classifies all JPEG/PNG images in a folder and prints a summary table.

Usage:
    python hailo_batch.py [path/to/image/folder]
"""

import degirum as dg
import time
import sys
import os
from pathlib import Path

IMAGE_DIR = sys.argv[1] if len(sys.argv) > 1 else "."
extensions = {".jpg", ".jpeg", ".png", ".bmp"}
images = [
    p for p in Path(IMAGE_DIR).iterdir()
    if p.suffix.lower() in extensions
]

if not images:
    print(f"No images found in {IMAGE_DIR}")
    sys.exit(1)

print(f"Found {len(images)} image(s) in {IMAGE_DIR}\n")

zoo   = dg.connect(dg.LOCAL, "degirum/hailo")
model = zoo.load_model(
    "mobilenet_v2--224x224_quant_hailort_hailo8l_1",
    device_id="HAILO8L"
)

print(f"{'Image':<30} {'Top Prediction':<35} {'Confidence':>10}  {'Time':>8}")
print("-" * 88)

total_time = 0
for img_path in sorted(images):
    start  = time.perf_counter()
    result = model(str(img_path))
    elapsed = (time.perf_counter() - start) * 1000
    total_time += elapsed

    top = result.results[0]
    print(
        f"  {img_path.name:<28} {top['label']:<35} "
        f"{top['score']*100:>8.1f}%  {elapsed:>6.1f} ms"
    )

avg = total_time / len(images)
print("-" * 88)
print(f"  {len(images)} images classified   Average: {avg:.1f} ms/image   "
      f"Total: {total_time:.0f} ms")
```

Run it with a folder of images:

```bash
# Put a few images in a test folder first
mkdir ~/test_images
cp ~/test_image.jpg ~/test_images/
# add more images to ~/test_images/ as you like

python hailo_batch.py ~/test_images/
```

---

## 5.4 Troubleshooting

| Problem | Solution |
|---|---|
| `hailortcli: command not found` | `sudo apt install hailort` then reboot |
| `ModuleNotFoundError: No module named 'degirum'` | `pip install degirum` inside your venv |
| `device_id HAILO8L not found` | Run `hailortcli fw-control identify` to confirm your device arch; change `device_id` to `"HAILO8"` if needed |
| First run hangs on "Loading model" | DeGirum is downloading the `.hef` on first use — needs internet, wait ~30 seconds |
| Model runs but results look wrong | Check the image loaded correctly with `python3 -c "from PIL import Image; print(Image.open('test_image.jpg').size)"` — should show `(width, height)` |
| `tensorflow` import fails | `pip install tensorflow` — takes 10–15 min on Pi; alternatively remove the CPU benchmark sections and run HAT+ only |
| CPU benchmark is very slow | Normal — TensorFlow on Pi CPU is the point of contrast. The HAT+ benchmark is what matters. |

---

## 5.5 What to Tell Participants

When running these demos with an audience, a few framing points help:

**On MobileNetV2 as a CNN:**
> "MobileNet is a convolutional neural network — it scans across the image with small filter windows, learning to detect edges, then textures, then shapes, then whole objects. It was specifically designed to be small enough to run on mobile and edge devices. Even so, on the Pi CPU alone it takes around 80–100ms per image."

**On what the HAT+ is doing:**
> "The AI HAT+ contains a dedicated neural processing unit — silicon designed specifically to run the matrix multiplications that CNNs rely on. It doesn't run general Python code; it only runs the compiled network. That specialisation is why it's 10–20x faster, while using a fraction of the power."

**On the difference from quantum computing:**
> "Both quantum circuits and neural networks work with probabilities — but via completely different mechanisms. The CNN learns statistical patterns in training data. The quantum circuit exploits superposition and interference in physical qubit states. They're complementary tools, not competitors."

---

## 5.6 Useful Links

- DeGirum PySDK documentation: https://docs.degirum.com/pysdk/user-guide-pysdk
- DeGirum Hailo model zoo: https://github.com/DeGirum/hailo_examples/blob/main/hailo_model_zoo.md
- Hailo RPi5 examples: https://github.com/hailo-ai/hailo-rpi5-examples
- Raspberry Pi AI HAT+ documentation: https://www.raspberrypi.com/documentation/accessories/ai-hat-plus.html
- Hailo community forum: https://community.hailo.ai

---

*This guide is for educational use. MobileNet is a trademark of Google. Hailo® is a trademark of Hailo Technologies Ltd.*
---
