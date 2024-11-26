Here’s a suggested **`README.md`** file for your project:

---

# **AI-Powered Flashcard Learning System**

This is a web-based **AI-powered flashcard learning system** designed to help users efficiently learn and review flashcards. It features a user-friendly interface, a robust backend, and smart scheduling for flashcard reviews.

---

## **Features**
### **1. Create Flashcards**
- Add new flashcards with a question and answer.
- Stores data in a SQLite database for persistence.
- Accessible via the frontend or backend API.

### **2. Review Flashcards**
- Flashcards are suggested for review based on a **spaced repetition algorithm**, ensuring optimal retention.
- If no card is due, the system selects the one closest to its next review time.
- Smart logic ensures no card is repeated consecutively.

### **3. Update Flashcard Review**
- Marks flashcards as either "Remembered" or "Forgot."
- Adjusts the next review time dynamically based on the user’s response:
  - Success increases the interval for the next review.
  - Failure resets the interval to a shorter duration.

### **4. Delete Flashcards**
- Users can delete unwanted flashcards directly from the review interface.

---

## **Technical Stack**

### **Backend**
- **Framework**: Flask
- **Database**: SQLite
- **API Features**:
  - `GET /flashcards`: Retrieve all flashcards.
  - `GET /flashcards/review`: Retrieve the next flashcard for review.
  - `POST /flashcards`: Create a new flashcard.
  - `POST /flashcards/<id>/review`: Update the review status of a flashcard.
  - `DELETE /flashcards/<id>`: Delete a flashcard.
- **Smart Scheduling**:
  - Implements spaced repetition using intervals in hours.
  - Ensures the same card is not shown consecutively.

### **Frontend**
- **Framework**: React
- **Styling**: Bootstrap
- **Features**:
  - **CreateFlashcard Component**: Add new flashcards to the system.
  - **ReviewFlashcard Component**: Review, update, or delete flashcards.
- **Integration**:
  - Axios is used to interact with the backend APIs.

---

## **Installation**

### **1. Backend Setup**
1. Clone the repository:
   ```bash
   git clone git@github.com:Sohil5220/flashcards.git
   cd flashcards/flashcard-backend
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```bash
   flask run
   ```

### **2. Frontend Setup**
1. Navigate to the frontend directory:
   ```bash
   cd ../flashcard-frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React development server:
   ```bash
   npm start
   ```

---

## **Usage**
1. Open the frontend app in your browser (`http://localhost:3000`).
2. Use the **Create Flashcard** section to add new cards.
3. Review flashcards in the **Review Flashcard** section:
   - Mark them as "Remembered" or "Forgot."
   - Delete cards if no longer needed.
4. The backend ensures intelligent scheduling and management.

---

## **Future Enhancements**
- Add user authentication for personalized flashcard management.
- Support for multimedia flashcards (images, audio).
- Enhanced analytics to track learning progress.

---

## **Screenshots**

### **1. Home Screen**
- Create and review flashcards.
![Home Screen](link_to_screenshot)

### **2. Review Flashcard**
- Mark flashcards or delete them directly.
![Review Flashcard](link_to_screenshot)

---
