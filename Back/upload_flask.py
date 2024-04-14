
from fileinput import filename 
from flask import *  
from flask import Flask_Uploads
from flask import Flask_WTF
app = Flask(__name__) 
  
@app.route('/')   
def main():   
    return "mmd"  
  
@app.route('/upload', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['mmd'] 
        name = request.json["name"]
        f.save("C:/Users/Seyed/Desktop/online-shop/Back/pics/" + f.filename)  
        return "True"

@app.route('/files/<path:path>')
def send_report(path):
    return send_from_directory('files', path)

if __name__ == '__main__':   
    app.run(debug=True)