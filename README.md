# ChatPulse
a simple-chat-app
ChatPulse | a chat app made for teams using socketio and flask

<img width="1901" height="908" alt="image" src="https://github.com/user-attachments/assets/ca31a825-2e55-4cc4-8c0a-f36bb77b8f3f" />


## installation

install virtualenv

### 1 create environment 
    
    virtualenv [name]
    
### 2 activate
    
     source [name]/bin/activate
     
### 3 install dependencies

     pip install -r requirements.txt
     
## Run 

     flask run

## Docker

To run with Docker:

1. Pull the image:
   ```
   docker pull harshal825/flask-chat-app
   ```

2. Run the container:
   ```
   docker run -p 5000:5000 harshal825/flask-chat-app
   ```

Access the app at http://localhost:5000
     
