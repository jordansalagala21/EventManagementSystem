# Event Management System (EVM) Web Application

The Event Management System (EVM) is a Django-based web application designed to streamline event management processes. This application provides features for organizing events, managing vendors, tracking volunteers, and handling ticket bookings efficiently.

## Features

- **User Authentication**: Users can register, login, and logout securely to access the application's functionalities.
- **Dashboard**: Provides an overview of total events, vendors, funds raised, and ticket sales.
- **Event Management**: Admins can add, view, edit, and manage events with details such as name, organizer, date, time, venue, and theme.
- **Vendor Management**: Allows the addition and management of vendors associated with events, including their purpose, contact information, and costs.
- **Ticket Booking**: Users can book event tickets with options for paid and free events. Payment integration is facilitated through Razorpay.
- **SMS Confirmation**: Sends SMS confirmation to users upon successful ticket booking using Twilio integration.
- **Volunteer Management**: Admins can add, view, and manage volunteers interested in contributing to events.
- **CSV Export**: Provides functionality to export participant details to a CSV file for record-keeping and analysis.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/evm-project.git
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up credential variables:**

    - Fill in the required environment variables such as `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`, `RAZORPAY_KEY`, `RAZORPAY_SECRET`, etc.

4. **Run migrations:**

    ```bash
    python manage.py makemigrations 
    python manage.py migrate 
    ```

5. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

6. **Access the application at `http://localhost:8000/`.**

## Usage

- Register as a user or login if already registered.
- Explore the dashboard for insights into events, vendors, and funds raised.
- Add, view, edit, and manage events through the admin interface.
- Book event tickets and receive SMS confirmations upon successful booking.
- Manage volunteers and vendors associated with events.
- Export participant details to a CSV file for analysis.

## Contributing

Contributions are welcome! Please follow the [Contribution Guidelines](CONTRIBUTING.md) before making any contributions.

## License

This project is licensed under the [MIT License](LICENSE).
