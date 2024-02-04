# REST API for a Price Alert System (tanX.fi Backend Project)

This is a basic RESTful API where we can create alert for a cryptocoin which generates e-mail when it reached the target value.
Other than this we can delete the alert we created.There is another endpoint which is usefull to fetch all alerts with status and implemented with pagination concept.
Used SqlAlchemy for Database.Applied Redis as a cache layer to get alerts from database.
## Table of Contents

- **Run without docker**
- **Endpoints**
  - **Creating a new Alert**
  - **Fetching Alerts**
  - **Delete Alert By gmail**
  - **Protected Endpoint with Basic Authentication**
- **Authentication **
- **Images of Solution for sending alerts**



## Run Without Docker

1. Clone the repository:
    ```bash
    git clone https://github.com/gokulraj1661/tanxAPI.git
    cd tanxAPI
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

4. Running the application

   ```bash
     python app.py

   ```
   As Dealing with Redis we have to start a redis server parelley when running the application.


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


## Images of Solution for sending alerts
![Screenshot 2024-02-04 070149](https://github.com/gokulraj1661/tanxAPI/assets/90254712/06d651ce-d452-4ec8-884f-2c803bc91215)
## Create Alert
![Screenshot 2024-02-04 070210](https://github.com/gokulraj1661/tanxAPI/assets/90254712/c3998f44-a775-4285-92f8-b60fdd7eb8a7)
## Get Alert with page segmentaion and filter
![Screenshot 2024-02-04 070308](https://github.com/gokulraj1661/tanxAPI/assets/90254712/23daffc7-3ad4-44c1-b9b6-bef42b355404)
## Teminal Output Of Sending mail
![Screenshot 2024-02-04 071822](https://github.com/gokulraj1661/tanxAPI/assets/90254712/f8db37db-c1d8-4ecb-8ffb-badd748b56d8)
## Mail Recived After Target Reached
![Screenshot 2024-02-04 070332](https://github.com/gokulraj1661/tanxAPI/assets/90254712/6632c04c-aa80-4efc-b073-b194dce5b066)
![Screenshot 2024-02-04 070359](https://github.com/gokulraj1661/tanxAPI/assets/90254712/e9c44fca-669c-4196-ad46-60977f8aaa06)
## Delete Alert
![Screenshot 2024-02-04 070435](https://github.com/gokulraj1661/tanxAPI/assets/90254712/9c4e26c9-346f-4100-bd7a-d013dc6801d9)


