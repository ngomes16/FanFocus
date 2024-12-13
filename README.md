# FanFocus

## Set Up Project

1. **Ensure Python and Node.js are installed**  
   - Download and install Python 
   - Download and install Node.js
  
2. **Navigate to the project folder**  
   - Use your terminal or command prompt to navigate to the root directory of the project.

3. **Set up a virtual environment**  
   - Run the following command to create a virtual environment:  
     ```bash
     python -m venv venv_name
     ```
   - Activate the virtual environment:
     - For Windows:  
       ```bash
       venv_name\Scripts\activate
       ```
     - For macOS/Linux:  
       ```bash
       source venv_name/bin/activate
       ```

4. **Install Python dependencies**  
   - Run the following command:  
     ```bash
     pip install -r requirements.txt
     ```
   - If this doesn't work for any reason, you may need to install each dependency individually as specified in the `requirements.txt` file.

5. **Set up the React front-end**  
   - Open a **separate terminal** and navigate to the `fanfocus` folder:  
     ```bash
     cd fanfocus
     ```
   - Run the following command to install Node.js dependencies:  
     ```bash
     npm install
     ```
   - Start the React application:  
     ```bash
     npm start
     ```
     A new browser window should open automatically. If it doesn't, navigate to [http://localhost:3000/](http://localhost:3000/) in your browser.

6. **Start the Flask back-end**  
   - In the original Python terminal, run the Flask application:  
     ```bash
     python app.py
     ```

## How to use software

The software has two pages: the home page, which displays the articles, and the profile page, where you can add teams, interests, fetch articles, and update interests.

1. **Adding Teams**: You can add teams by simply selecting them from the sidebar.
2. **Adding Interests**: You can add interests by typing them in the search bar and then pressing the "add" button.
3. **Removing Items**: To remove an item, click on the item.
4. **Fetching Articles**: Once you've finalized the teams you want to search articles for, click the "fetch articles" button. This will trigger the process in the backend.
5. **Updating Interests**: After fetching the articles, you can modify the list of interests to your liking and click "update key terms".
6. **Navigating Back to Home**: To go back to the home screen, click the icon in the top left corner.
7. **Reading Articles**: On the home page, you can go through articles by clicking the up and down arrows.

NOTE: There is a default user used for testing purposes. For our purposes, it was "one"

