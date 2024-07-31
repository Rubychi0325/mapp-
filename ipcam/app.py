from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/import', methods=['GET', 'POST'])
def import_csv():
    csv_data = []  # 初始化為空列表
    if request.method == 'POST':
        if 'file' not in request.files:
            return "沒有選擇檔案"
        
        file = request.files['file']
        
        if file.filename == '':
            return "沒有選擇檔案"
        
        if file and file.filename.endswith('.csv'):
            csv_content = file.read().decode('utf-8')
            csv_data = list(csv.reader(csv_content.splitlines()))
        else:
            return "僅支援CSV格式的檔案"
    
    return render_template('import.html', csv_data=csv_data)

if __name__ == '__main__':
    app.run(debug=True)