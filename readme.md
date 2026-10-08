

# How to run?
Please have the following installed
- NPM and NodeJS 24+
- Python 3

## Frontend
```
cd frontend
npm install
npm run dev
```


## Backend Setup
```
cd backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Run Backend
```
uvicorn main:app --reload
```

## To show backend API (Swagger)
```
http://127.0.0.1:8000/docs
```

## To show website
```
http://127.0.0.1:5173
```