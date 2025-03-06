The Four In A Row game server is an educational Python Django-based API designed for students to develop software and robotic clients for gameplay. It provides a simple JSON-based HTTP API for interaction, supporting both web-based and robotic players. Inspired by the Battleships API, it focuses on teaching API fundamentals. The server requires Python 3.6+ and follows REST principles with versioned endpoints (api/1.0/). The stable beta was targeted for January 2024, with ongoing improvements.

## Gemini API Integration

The Four In A Row game server now includes integration with the Gemini API. This allows for enhanced functionality and interaction with the Gemini cryptocurrency exchange.

### Configuration

To configure the Gemini API integration, you need to set the following variables in your `fourinarow/settings.py` file:

```python
GEMINI_API_KEY = 'your_gemini_api_key'
GEMINI_API_SECRET = 'your_gemini_api_secret'
GEMINI_API_BASE_URL = 'https://api.gemini.com/v1'
```

### Usage

The Gemini API endpoints are available under the `/api/gemini/` URL path. You can interact with the Gemini API using these endpoints to perform various actions such as retrieving market data, placing orders, and more.

For example, to get the current market price of Bitcoin, you can make a GET request to the following endpoint:

```
GET /api/gemini/price/btc
```

This will return the current market price of Bitcoin in JSON format.

### Error Handling

The Gemini API integration includes error handling for API requests. If an error occurs during an API request, an appropriate error message will be returned in the response.

### Parsing API Response

The API response data from the Gemini API is parsed and returned in a structured format. This allows for easy consumption of the data by your application.
