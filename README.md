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

## How it works

How it works:
Our project has three main areas that work together to create the final project.

Data Gathering:

We have some script created in python that scrape popular sports news sites such as ESPN, AP, and SI. We gather the text content and the URL to these pages. In a production application, a crawler would be running continuously gathering data and articles from relevant sources to provide feedback to the user, but in our use case we have a manual call we make to gather this data and store it. Our storage function, called update_content, takes these articles as a list and performs a few computations on them. First, it stores them all in our mock articles database (a set of .json files) so we have a reference to the actual article text. This serves as our documents database. It also updates an inverted index with terms so that we can track what articles contain which terms. Finally, when new documents are added, it precomputes tf-idf weights, vectorizes them, and stores them in a .pkl also in our data folder.

Document Retrieval:

Our document retrieval utilizes the computed tf-idf vectors per document and calculates the similarity to a user query vector. We then order the documents by similarity and return them in a batch with a size designated by the frontend. In addition to tf-idf we have a user inputted filtering system using upvotes and downvotes that the user can provide. This allows the user to further refine the information that they find relevant. This works by weighting terms in articles that they provide feedback on. If an article gets an upvote, those terms get a slight boost in weight and vice versa for downvotes. Articles with boosted terms will thus result in a higher cosine similarity vector and thus float to the top of the relevance ranking for documents retrieved by a user query (along side the similarity that comes from the actual query). We use the term query to define how we match to the users interests by keyword, but it doesn't imply a user typed search, rather the query is constructed using the terms the users add as relevant.

User Interface:

Our UI has two locations, the main viewing page called the home page, and then a profile page. The frontend is a react app that sends requests to a Flask server to provide data. The end points are defined in app.py. The home page has the main viewing area for the article text and the upvote/downvote buttons to provide feedback. The profile page allows the user to set interested teams and key terms. Note that in our projects we have manual data gathering based on the teams added as well a button to update the key terms. In a production application, as previously mentioned, both of these things would happen automatically when interests are added. The key terms you see displayed in the middle are the terms used to construct the user query. There is also a scrollable field to the left of the profile screen that allows you to select your favorite teams easily.


# Submission Resources
- Code Repository: https://github.com/ngomes16/FanFocus
- TextData Entry: https://textdata.org/submissions/67251a2a22ea54f14be32116
- Video Presentation: https://mediaspace.illinois.edu/media/t/1_t8r72tbv

