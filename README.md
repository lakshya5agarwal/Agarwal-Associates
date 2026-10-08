# Radius Systems Project

## Overview
The Radius Systems project implements a simple HTTP server using Python's `http.server` module. It is designed to handle GET and POST requests, allowing users to submit contact leads and view them through an admin dashboard. The server interacts with an SQLite database to store and retrieve the leads.

## Project Structure
```
radius-systems
├── server.py          # Main server implementation
├── database.db        # SQLite database for storing contact leads
├── requirements.txt   # Python dependencies
├── .gitignore         # Files and directories to ignore in Git
└── README.md          # Project documentation
```

## Setup Instructions
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd radius-systems
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. **Run the server**:
   Start the server by executing:
   ```
   python server.py
   ```
   The server will be running at `http://localhost:3000`.

## Usage
- **Submit a Contact Lead**: You can submit a contact lead through the designated form on the website.
- **View Leads**: Access the admin dashboard at `http://localhost:3000/admin` to view all submitted leads.

## Database
The project uses an SQLite database (`database.db`) to store contact leads. The database contains a table named `contact_leads` with the following fields:
- `id`: Unique identifier for each lead
- `full_name`: Name of the contact
- `email`: Email address of the contact
- `company`: Company name
- `phone`: Phone number
- `solution_requirement`: Description of the solution required
- `created_at`: Timestamp of when the lead was created

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.