# ORE Python Setup Guide

> How to set up and run the Open Source Risk Engine (ORE) on a fresh machine.

---

## Prerequisites

| Requirement | Details |
|:---|:---|
| **OS** | Windows 10/11, macOS, or Linux |
| **Python** | Python 3.9 – 3.12 (check with `python --version`) |
| **pip** | Bundled with Python (check with `pip --version`) |
| **Git** | Only needed if cloning the repo from source |

---

## Quick Start (Recommended): Pre-built Python Module

This is the simplest approach — no C++ compilation required.

### Step 1: Clone or Copy the Repository

```bash
git clone https://github.com/OpenSourceRisk/Engine.git
cd Engine/Examples/ORE-Python
```

Or copy the entire `Engine` folder to the target machine.

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` appear before your prompt.

### Step 4: Install ORE

```bash
pip install open-source-risk-engine
```

This installs the pre-compiled `ORE` Python module (includes QuantLib and QuantExt).

### Step 5: Verify the Installation

```bash
python -c "from ORE import *; print('ORE imported successfully')"
```

If this prints `ORE imported successfully`, you are ready to go.

### Step 6: Run the Example

```bash
python ore.py
```

This will:
1. Load configuration from `Input/ore.xml`
2. Read the portfolio from `Input/portfolio_swap.xml`
3. Run NPV, cashflow, and curves analytics
4. Write results to `Output/`

> [!IMPORTANT]
> Run `ore.py` **from within** the `ORE-Python` directory. The XML configs use relative paths like `../../Input/market_20160205_flat.txt` that resolve relative to the working directory.

---

## Project Structure

```
Engine/
├── Examples/
│   ├── Input/                          # Shared market data & curves
│   │   ├── market_20160205_flat.txt    # Market snapshot (rates, FX, etc.)
│   │   ├── fixings_20160205.txt        # Historical fixings
│   │   ├── curveconfig.xml             # Curve construction rules
│   │   ├── conventions.xml             # Market conventions
│   │   ├── todaysmarket.xml            # Market configuration
│   │   └── pricingengine.xml           # Pricing engine selection
│   │
│   ├── ORE-Python/                     # ★ Main working directory
│   │   ├── ore.py                      # Main script (NPV analysis)
│   │   ├── run.py                      # Alternative runner
│   │   ├── Input/
│   │   │   ├── ore.xml                 # Engine configuration
│   │   │   ├── portfolio_swap.xml      # Trade definitions
│   │   │   └── simulation.xml          # Monte Carlo settings
│   │   ├── Output/                     # Results written here
│   │   └── Notebooks/                  # Jupyter notebook examples
│   │
│   └── Exposure/                       # Additional swap examples
│       ├── run_swap.py
│       ├── run_ccs.py                  # Cross-Currency Swap
│       ├── run_equity.py               # Equity Swap
│       ├── run_commodity.py            # Commodity Swap
│       ├── run_cmsspread.py            # CMS Spread Swap
│       ├── run_swaption.py             # Swaption
│       └── Input/                      # Portfolios for each example
```

---

## Configuration Quick Reference

### `Input/ore.xml` — What Analytics to Run

| Analytic | Active? | Description |
|:---|:---:|:---|
| `npv` | **Y** | Compute Net Present Value of all trades |
| `cashflow` | **Y** | Generate detailed cash flow schedule |
| `curves` | **Y** | Export constructed yield curves |
| `simulation` | N | Monte Carlo simulation (resource-intensive) |
| `xva` | N | CVA/DVA/FVA calculations (requires simulation) |

Set `<Parameter name="active">Y</Parameter>` to enable an analytic.

### `Input/portfolio_swap.xml` — Trade Definitions

The default trade is a **20-year EUR Interest Rate Swap**:
- **Notional**: €20,000,000
- **Fixed Leg**: Receive 2.0% annually
- **Floating Leg**: Pay EUR-EURIBOR-6M semi-annually
- **Dates**: March 2016 → March 2036

### Key Outputs

| File | Content |
|:---|:---|
| `Output/npv.csv` | Net Present Value per trade |
| `Output/flows.csv` | Projected cash flow schedule |
| `Output/curves.csv` | Yield curve data points |

---

## Running Additional Swap Examples

The `Exposure` directory contains more complex examples. To run them:

```bash
cd ../Exposure
python run_swap.py
python run_ccs.py        # Cross-Currency Swap
python run_equity.py     # Equity Swap
python run_commodity.py  # Commodity Swap
python run_cmsspread.py  # CMS Spread Swap
python run_swaption.py   # Swaption
```

> [!NOTE]
> These examples run **full simulations** (Monte Carlo) and XVA analytics, so they take longer than `ore.py`.

---

## Jupyter Notebooks

ORE includes interactive Jupyter notebooks for deeper exploration:

```bash
pip install jupyterlab
cd Examples/ORE-Python
jupyter lab
```

Notebooks are in `Notebooks/Example_1` through `Example_9`.

---

## Alternative: Building from Source (Advanced)

If you need to modify the C++ engine or build the SWIG bindings yourself:

### Prerequisites
- CMake ≥ 3.15
- C++17 compiler (MSVC 2019+, GCC 9+, Clang 10+)
- Boost libraries
- SWIG (for Python bindings)

### Build Steps

```bash
cd Engine
mkdir build && cd build
cmake .. -DORE_BUILD_SWIG=ON
cmake --build . --config Release
```

Then set your `PYTHONPATH` to find the built module:

```bash
# Linux/macOS
export PYTHONPATH=$HOME/Engine/build/ORE-SWIG

# Windows (PowerShell)
$env:PYTHONPATH = "C:\path\to\Engine\build\ORE-SWIG"
```

---

## Troubleshooting

| Problem | Solution |
|:---|:---|
| `ModuleNotFoundError: No module named 'ORE'` | Ensure the virtual environment is **activated** and `pip install open-source-risk-engine` was run inside it. Verify with `pip list \| findstr open-source`. |
| `RuntimeError: Failed to open file Input/ore.xml` | You must run the script from the `ORE-Python` directory (or the directory containing the `Input` folder). The script uses relative paths. |
| Multiple `.venv` directories causing confusion | Only use **one** virtual environment. The recommended location is `ORE-Python/.venv`. Delete any stale `.venv` folders in subdirectories like `Input/.venv`. |
| XVA analytic crashes | XVA requires simulation to be enabled and run first. Keep `simulation` and `xva` set to `N` in `ore.xml` unless you are running the full `run.py` workflow. |
| VS Code not finding ORE module | Set the Python interpreter in VS Code to `.venv/Scripts/python.exe` via `Ctrl+Shift+P` → "Python: Select Interpreter". |

---

## VS Code Configuration (Optional)

For a smooth IDE experience, create these files in `ORE-Python/`:

**`.vscode/settings.json`**
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe"
}
```

**`.vscode/launch.json`**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: ORE",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        }
    ]
}
```

This ensures pressing **F5** runs the script with the correct working directory and virtual environment.
