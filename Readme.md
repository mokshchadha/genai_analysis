# Political Survey Analysis App

A Streamlit application for analyzing political survey data using either Ollama (local) or Google's Gemini Pro API. This app provides insights, visualizations, and detailed analysis of political survey data through an intuitive web interface.

## Prerequisites

Before setting up the application, ensure you have the following installed on your Mac:

- Python 3.8 or higher
- Homebrew (for installing Ollama)
- Git (for cloning the repository)

## Installation Steps

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python (if not already installed)

```bash
brew install python
```

### 3. Install Ollama (Optional - only if you plan to use local models)

```bash
brew install ollama
```

### 4. Create and Setup Python Virtual Environment

```bash
# Navigate to your preferred directory
mkdir political-survey-analysis
cd political-survey-analysis

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 5. Install Required Python Packages

```bash
pip install streamlit pandas requests plotly google-generativeai
```

### 6. Clone or Create Project Files

Create a new file called `app.py` and copy the application code into it.

## Configuration

### Setting up Ollama (Optional)

1. Start the Ollama service:
```bash
ollama serve
```

2. Pull your desired model (example with Llama 2):
```bash
ollama pull llama2
```

### Setting up Gemini Pro (Optional)

1. Visit the [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Keep this key handy for when you run the application

## Running the Application

1. Ensure your virtual environment is activated:
```bash
source venv/bin/activate
```

2. Start the Streamlit app:
```bash
streamlit run app.py
```

The application should automatically open in your default web browser at `http://localhost:8501`

## Using the Application

1. Select your preferred AI provider (Ollama or Gemini Pro) in the sidebar
   - For Ollama: Ensure the service is running locally
   - For Gemini Pro: Enter your API key in the sidebar

2. Upload your CSV file containing political survey data
   - Required columns: Gender, Party support percentages
   - Optional: Historical data, demographic information

3. Choose your analysis type:
   - Gender-based Analysis
   - Historical Comparison
   - Demographic Trends
   - Custom Query

4. Add any additional context (optional)

5. Click "Analyze" to generate insights

## Data Format Requirements

Your CSV file should include the following columns:
- Gender
- Support (numerical values)
- Party (categorical values)
- Additional demographic information (optional)

Example CSV format:
```csv
Gender,Party,Support,Age_Group
Male,Democratic,45.2,18-29
Female,Republican,38.7,30-44
...
```

## Troubleshooting

### Common Issues and Solutions

1. **Ollama Connection Error**
   ```
   Error: Connection refused
   ```
   Solution: Ensure Ollama is running with `ollama serve`

2. **Gemini API Key Error**
   ```
   Error: API key not found
   ```
   Solution: Double-check your API key in the sidebar

3. **CSV Format Error**
   ```
   Error: Required columns not found
   ```
   Solution: Ensure your CSV follows the required format

### Memory Issues

If you encounter memory issues with large datasets:

```bash
export PYTHONUNBUFFERED=1
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=1024
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please open an issue in the repository or contact the maintainers.

## Acknowledgments

- Streamlit for the web framework
- Ollama for local LLM support
- Google for Gemini Pro API
- Plotly for visualization capabilities

## Project Status

This project is actively maintained. Check back for updates and new features.