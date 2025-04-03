# Coding Platform Question Fetcher

This application fetches coding questions from various platforms (LeetCode, GeeksforGeeks, HackerRank, etc.) and provides a user interface to view and filter questions by company and difficulty.

## Features

- Fetches questions from multiple coding platforms
- Filters questions by company and difficulty
- Provides statistics and visualizations
- Interactive web interface
- RESTful API endpoints

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Project Structure

```
.
├── leetcode_api.py      # Flask API server
├── streamlit_app.py     # Streamlit web interface
├── requirements.txt     # Python dependencies
├── .env                # Environment variables
├── .streamlit/         # Streamlit configuration
├── setup.py           # Package setup
├── runtime.txt        # Python version specification
├── Procfile          # Deployment configuration
├── packages.txt      # System dependencies
└── leetcode_data/    # Directory for storing data
```

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask API server:
```bash
python leetcode_api.py
```

2. In a new terminal, start the Streamlit app:
```bash
streamlit run streamlit_app.py
```

3. Access the web interface at: http://localhost:8502
4. The API server will be running at: http://localhost:5000

### API Endpoints

- `GET /api/companies`: Get list of supported companies
- `GET /api/questions/<company>`: Get company-specific questions
- `GET /api/summary/<company>`: Get summary of company-specific questions

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 