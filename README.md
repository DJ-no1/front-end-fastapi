# URL Intelligence Dashboard

A Streamlit-based frontend for URL analysis and security intelligence.

## Features

- 🔍 URL Analysis and Security Scoring
- ⚡ Performance Metrics
- 📄 Content Analysis
- 🛠️ Technology Stack Detection
- 🌐 Domain Information
- 🚀 Quick Connectivity Testing

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd front-end-fastapi
```

### 2. Install Dependencies

```bash
pip install -r frontend_requirements.txt
```

### 3. Environment Configuration

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and update the configuration:
   ```
   API_BASE_URL=http://your-api-url:8000
   ```

### 4. Run the Application

```bash
streamlit run streamlit_frontend.py
```

The application will be available at `http://localhost:8501`

## Environment Variables

- `API_BASE_URL`: The base URL of your FastAPI backend service

## Usage

1. Enter a URL in the input field
2. Choose between "Full Analysis" or "Quick Connectivity Test"
3. Click "Analyze" to get detailed results
4. Review the analysis across different tabs:
   - Security analysis
   - Performance metrics
   - Content information
   - Technology stack
   - Domain details

## Security

- The `.env` file contains sensitive configuration and is excluded from version control
- Always use the `.env.example` template for new deployments
- Never commit actual API keys or sensitive URLs to the repository

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License
