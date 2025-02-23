# Pheidippides API

## Overview

This project is an interval integration for telex built with FastAPI receiving daily recommendations on books to read based on a selected genre. It uses two public APIs to yeild results, they are google book API and open library API.

## Features

- 📚 Daily Book Recommendations
- ✅ Input validation using Pydantic models.
- 📝 API documentation (auto-generated by FastAPI)
- 🔒 CORS middleware enabled

## Project Structure

```
pheidippides-api/
├── api/
│   ├── routes/
│   │   ├── __init__.py
│   │   └── integration.py
|   ├── __init__.py
│   └── router.py           # API router configuration
├── core/
│   ├── __init__.py
│   └── config.py           # Application settings
├── tests/
│   ├── __init__.py
│   └── test_url.py       # API endpoint tests
├── main.py                 # Application entry point
├── requirements.txt        # Project dependencies
└── README.md
```

## Technologies Used

- Python 3.12
- FastAPI
- Pydantic
- pytest
- uvicorn
- httpx

## Installation

1. Clone the repository:

```bash
git clone <repo-link>
cd pheidippides-api
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt # On Linux: venv/bin/activate
```

## Running the Application

1. Start the server:

```bash
uvicorn main:app
```

2. Access the API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Books

- `GET /integration.json` - JSON output required be telex.
- `POST /tick` - Endpoint used by telex to make requests.
- `PUT /` - Get integration details.


Available genres:

- fantasy
- mystery
- horror
- romance
- dystopian
- adventure
- biography
- history
- comedy
- nigerian

<!-- ## Running Tests

```bash
pytest
``` -->

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add new-feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open a Pull Request

<!-- ## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. -->

## Support

For support, please open an issue in the GitHub repository.

---


# How to use on Telex

Choose any provider (such as render or fly.io) to deploy the endpoint, thereby making it available publicly.

To setup on Telex, create an app then enter the publicly available /integration.json link for it to be registed on telex

![adding integration to telex](screenshots/image.png)

On clicking the manage app option tou should have this

![available integration](screenshots/image-1.png)

Click on connect app, then proceed to setting to configure your desired genre and notification interval (it follows a crontab syntax), then save settings

![configuring settings](screenshots/image-2.png)

Go to channels, to configure the app under a specific channel meant for receiving said notifications

![test channel](screenshots/image-3.png)

click on configure apps, then turn it on for that specific channel

![test channel integration configuration](screenshots/image-4.png)

Once your interval is set interval is reached, telex would call you /tick url integration, so a channel notification like the one shown below would be achieved

![test channel notification](screenshots/image-5.png)

![working integration](/screenshots/telex-invite-image.png)