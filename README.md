# Chat Application - Enfund Assignment

[Live Demo](https://chat.gautamgiri.dev "Live Demo")

A simple and efficient chat application built using **Django** and **WebSockets (channels)** to provide real-time communication. The app features a user-friendly interface, secure authentication, and modern chat functionality.

---

## AWS Lambda Functions
Instructed AWS Lambda Functions are present in `aws-lambda-functions` directory.

## Key Features

1. **Simple, User-Friendly, and Responsive UI**  
   - Designed with a clean and intuitive interface.
   - Fully responsive, optimized for desktops, tablets, and mobile devices.

2. **User Authentication and Authorization**  
   - Users can register and log in securely using **Django Authentication**.
   - Proper user role management for enhanced security.

3. **Real-Time Chatting**  
   - Powered by **Django Channels** for real-time WebSocket communication.
   - Chat messages are instantly delivered between users.

4. **User Online/Offline Status**  
   - Displays the real-time online/offline status of users in the chat interface.

5. **New User Detection**  
   - If a new user registers while another user is logged in, the system detects and informs other clients dynamically.

6. **Notification Sound Feedback**  
   - The system plays a notification sound when a user receives any message.

---

## Application Structure

### 1. **Backend**:
   - **Framework**: Django
   - **Database**: SQLite
   - **Real-Time Communication**: Django Channels with WebSockets

### 2. **Frontend**:
   - **Templates**: Django Templates with TailwindCSS for styling
   - **JavaScript**: Vanilla JS for dynamic behaviors and WebSocket handling

### 3. **Key Components**:
   - **User Authentication**:
     - Login, Signup, and Logout functionalities.
     - Password hashing for secure user data storage.
   - **Chat Management**:
     - Real-time messaging system.
     - Persistent chat history stored in the database.
   - **User Status**:
     - Online/offline status updated dynamically with WebSockets.

---

## Installation and Setup

Follow these steps to set up and run the application locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/gautamgiri-dev/enfund-chat-assignment
   cd enfund-chat-assignment
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**:  
   Open your browser and navigate to [http://localhost:8000](http://localhost:8000).

---

## Enhancements that can be done

1. Email based user authentication and email verification
2. Test complexity of password
3. File and image sharing support in chat.
4. Push notifications for new messages.

---

## Screenshots

### Login Page
![Login Page](https://via.placeholder.com/800x400?text=Login+Page)

### Chat Interface
![Chat Interface](https://via.placeholder.com/800x400?text=Chat+Interface)

### Chat Interface (Mobile)
![Chat Interface](https://via.placeholder.com/800x400?text=Chat+Interface)

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## Contributors

- **Gautam Giri**  
  Developer | [Portfolio](https://gautamgiri.dev "Gautam Giri Portfolio")

