# Rural-Friendly Banking Website

A user-friendly banking website designed specifically for rural users, emphasizing simplicity, accessibility, and ease of use.

## Features

- Simple and intuitive user interface
- Multilingual support (English and Hindi)
- Secure authentication system
- Mobile-responsive design
- Essential banking features:
  - Balance checking
  - Fund transfers
  - Loan applications
  - Customer support

## Setup Instructions

1. Install Python 3.8 or higher

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
rural-bank/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
└── templates/         # HTML templates
    ├── index.html
    ├── dashboard.html
    ├── login.html
    └── register.html
```

## Security Features

- OTP-based authentication
- Secure password handling
- Session management
- CSRF protection

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

MIT License
