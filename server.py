import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def page():
    return os.getenv("COMMENT", "DDPS TEST TEST")

app.run(host="0.0.0.0",port=os.getenv("PORT", "8000"))