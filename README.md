# Suicide-Related Content Monitoring System 

## Project Overview

The Suicide-Related Content Monitoring System is a Python-based monitoring tool that automatically detects and analyzes suicide-related risk content from X(Twitter), Naver Blog, and DCInside platforms. It identifies suicide-inducing information through OpenAI GPT models and keyword-based analysis, saving results in CSV format for systematic monitoring.

## Key Features

### Multi-Platform Data Collection
- **X(Twitter)**: Real-time tweet collection via API v2
- **Naver Blog**: Blog post collection using Search API
- **DCInside**: Post collection through web crawling

### AI-Based Risk Analysis
- **OpenAI GPT-3.5-turbo** model for advanced suicide-inducing content detection
- **Keyword-based analysis** system as alternative analysis method
- Risk score calculation on 0.0-1.0 scale

### User-Customizable Settings
- Selective data collection by platform
- User-defined number of posts to collect
- Search keyword and period configuration

### Result Analysis and Storage
- Detailed analysis results saved in CSV format
- Platform-specific collection success rate and risk statistics
- Real-time progress monitoring

## Project Structure

```
suicide-related-content-monitoring-system/
├── main.py                    # Main execution file
├── requirements.txt           # Dependency package list
├── .env.example              # Environment variable setup example
├── README.md                 # Project documentation
├── config/
│   ├── __init__.py
│   └── settings.py           # System configuration management
├── crawlers/
│   ├── __init__.py
│   ├── base_crawler.py       # Base crawler class
│   ├── twitter_crawler.py    # Twitter API crawler
│   ├── naver_crawler.py      # Naver blog crawler
│   └── dcinside_crawler.py   # DCInside crawler
├── analyzers/
│   ├── __init__.py
│   ├── openai_analyzer.py    # OpenAI-based analyzer
│   └── keyword_analyzer.py   # Keyword-based analyzer
├── utils/
│   ├── __init__.py
│   ├── data_processor.py     # Data processing utilities
│   └── file_manager.py       # File storage management
├── models/
│   ├── __init__.py
│   └── data_models.py        # Data model definitions
├── results/                  # Analysis results storage directory
└── logs/                     # Log files storage directory
```

## Installation and Setup

### 1. System Requirements
- Python 3.8 or higher
- Internet connection (for API calls and web crawling)
- Minimum 4GB RAM recommended

### 2. Repository Clone and Environment Setup
```bash
git clone 
cd suicide_monitoring_system

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Package Installation
```bash
pip install -r requirements.txt
```

### 4. Environment Variable Configuration
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env file to input API keys
```

#### Required API Key Configuration
```env
# X(Twitter) API Configuration
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# Naver API Configuration
NAVER_CLIENT_ID=your_naver_client_id_here
NAVER_CLIENT_SECRET=your_naver_client_secret_here

# OpenAI API Configuration
OPENAI_API_KEY=sk-your_openai_api_key_here
```

## API Key Acquisition Methods

### X(Twitter) API
1. Access [Twitter Developer Portal](https://developer.twitter.com/)
2. Apply for developer account and get approval
3. Create project and obtain Bearer Token
4. Apply for Elevated access (for advanced features)

### Naver Search API
1. Access [Naver Developers Center](https://developers.naver.com/)
2. Register application
3. Select Search API and obtain Client ID/Secret
4. Confirm daily 25,000 call limit

### OpenAI API
1. Create account at [OpenAI Platform](https://platform.openai.com/)
2. Generate new secret key in API Keys page
3. Add payment method and purchase credits (prepaid system as of 2025)
4. Set usage limits

## Usage Instructions

### Basic Execution
```bash
python main.py
```

### Execution Process
1. **Platform Selection**: Choose platforms to collect data from (individual/all/available only)
2. **Search Configuration**: Input keywords (comma-separated)
3. **Period Setting**: Input start/end dates (YYYY-MM-DD format)
4. **Collection Amount Setting**: Set number of posts to collect per platform
5. **Automatic Execution**: Data collection → Analysis → Result storage

### Usage Example
```
Selected Platforms: X(Twitter), Naver Blog
Search Keywords: suicide, extreme choice
Collection Period: 2025-06-01 ~ 2025-06-15
Collection Amount: Twitter 100 posts, Naver Blog 50 posts
```

## Understanding Analysis Results

### Output Files
- **CSV File**: `results/suicide_monitoring_result_YYYYMMDD_HHMMSS.csv`
- **Log Files**: Generated in `logs/` directory

### Key Analysis Metrics
| Column Name | Description | Value Range |
|-------------|-------------|-------------|
| Platform | Data collection platform | Twitter/Naver Blog/DCInside |
| AI_Analysis_Score | Risk score | 0.0 - 1.0 |
| Suicide_Risk_Content | Risk determination result | Y/N |
| AI_Analysis_Reason | Determination rationale | Text description |
| Crawling_Success | Data collection success status | True/False |

### Risk Threshold Values
- **0.3 or higher**: Classified as suicide-inducing content
- **0.1-0.3**: Requires careful observation
- **Below 0.1**: Safe level

## Precautions and Ethical Considerations

### Legal Compliance
- Comply with Personal Information Protection Act
- Check platform-specific terms of service
- Follow robots exclusion standard (robots.txt)

### Ethical Usage
- Use **for research and public interest purposes only**
- Secure storage of collected data
- Protection of personally identifiable information

### Technical Limitations
- API usage quota management
- Crawling speed control (bot detection prevention)
- Dependency on network stability

## Troubleshooting

### Common Errors

#### OpenAI API Errors
```
Error 401: Incorrect API key
→ Check OPENAI_API_KEY in .env file (must start with sk-)

Error 429: Rate limit exceeded
→ API usage quota exceeded, credit purchase required
```

#### Naver API Errors
```
Error 403: Forbidden
→ Recheck Client ID/Secret, verify daily quota

Error 400: Bad Request
→ Search term encoding issue, remove special characters
```

#### DCInside Crawling Errors
```
Empty results returned
→ Possible page structure change, selector update needed

Connection timeout
→ Check network status, adjust request intervals
```

### Performance Optimization
- **Adjust Collection Amount**: Collect only necessary amounts to save API costs
- **Disable Parallel Processing**: Prevent blocking due to excessive requests
- **Use Caching**: Cache results to prevent duplicate analysis

## Updates and Maintenance

### Regular Update Items
1. **Dependency packages** latest version updates
2. **API specification changes** response
3. **Website structure changes** response (crawling parts)
4. **Security patches** application

### Version Management
```bash
# Check latest version
git pull origin main

# Update packages
pip install --upgrade -r requirements.txt
```

## Support and Contribution

### Bug Reports
- Report bugs through GitHub Issues
- Attach log files and error messages
- Describe reproducible steps

### How to Contribute
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Create Pull Request

## License

This project is distributed under the MIT License. Please check license conditions before commercial use.

## Disclaimer

This system was developed for research and public interest purposes, and users must comply with relevant laws and ethical standards when using it. Users are fully responsible for any legal or ethical issues arising from system usage.

---

**Development Version**: v1.0.0  
**Last Updated**: June 2025  
**Python Version**: 3.8+  