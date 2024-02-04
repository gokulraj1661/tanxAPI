# REST API for a Price Alert System (tanX.fi Backend Project)

This is a basic RESTful API where we can create alert for a cryptocoin which generates e-mail when it reached the target value.
Other than this we can delete the alert we created.There is another endpoint which is usefull to fetch all alerts with status and implemented with pagination concept.
Used SqlAlchemy for Database.Applied Redis as a cache layer to get alerts from database.
## Table of Contents

- **Installation**
- **Endpoints**
  - **Creating a new Alert**
  - **Fetching Alerts**
  - **Delete Alert By gmail**
  - **Protected Endpoint with Basic Authentication**
- **Authentication **
- **Images of Solution for sending alerts**



## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/gokulraj1661/FarmwiseAITask.git
    cd FarmwiseAITask
    ```

2. Set up a virtual environment:
    ```bash
    pip install virtualenv
    virtualenv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```


## Endpoints

1. **Creating a new Alert:**

   - **URL:** `http://127.0.0.1:5000/alerts/create`
   - **Method:** `POST`
   - **Parameters:**
     - `user_email` (string): Email of the User.
     - `target_price` (float): Target price for triggering the Alert.
     - `symbol` (string): Type of Cryptocoin according to Binance Websocket.
     - `status` (string): active or trigerred.
       

2. **Fetching Alerts:**

   - **URL:** `http://127.0.0.1:5000/alerts/getalerts?page=1`
   - **Method:** `GET`
   - **Redis cache layer add to optimise requests**
3. **Delete Alert By gmail:**

   - **URL:** `http://127.0.0.1:5000/alerts/delete/<email>`
   - **Method:** `DELETE`


## Authentication 

With the help of HTTPBasicAuth, developed a login page where it allows the endpoints access when they pass through the login page. For this API, the username and password are specified here:

- **Username:** `Username`
- **Password:** `password`

## Running the application

```bash
cd app
python main.py

```
## Images of Solution for sending alerts

