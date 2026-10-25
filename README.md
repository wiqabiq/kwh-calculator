# KWH Calculator

A simple desktop application for estimating electricity meter readings based on historical KWH consumption.

## Features

- **Meter Reading Estimation:** Predict electricity meter readings for a selected date.
- **Historical Consumption:** Calculate total consumption between two meter readings.
- **Average Daily Usage:** Estimate average daily KWH consumption.
- **Past and Future Predictions:** Estimate readings before or after the latest recorded reading.
- **Input Validation:** Detect invalid dates and meter readings.
- **Resizable Interface:** A clean, user-friendly graphical interface built with Python and Tkinter.
- **Windows Support:** Available as a standalone Windows executable.
- **macOS Build:** Planned through automated GitHub Actions builds.

## How It Works

The calculator uses two recorded meter readings to calculate average daily consumption.

**Example:**

| Reading | Value |
|---|---:|
| Previous date | 20.05.2025 |
| Previous reading | 12,000 KWH |
| Latest date | 25.10.2026 |
| Latest reading | 16,342 KWH |
| Prediction date | 30.10.2026 |
| Estimated reading | 16,383.51 KWH |

Predictions assume that average daily consumption remains constant. Actual electricity usage may vary.

## Technology

- Python
- Tkinter and ttk
- Python `datetime` module
- PyInstaller for packaging standalone applications
- GitHub Actions for automated builds

## Running from Source

1. Install Python.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

   ```bash
   python kwh_gui.py
   ```

## Project Status

The Windows desktop application is functional. Cross-platform packaging and the macOS build are in progress.

## Disclaimer

This application provides estimates, not official meter readings or electricity bills. Results depend on historical consumption and should be treated as approximations.

## License

No license has been selected yet.
