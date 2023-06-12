from flask import Flask, render_template, request
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['csvfile']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join('static', filename))
            return render_template('uploadCSV.html', message="CSV file uploaded successfully.")
    return render_template('uploadCSV.html')


@app.route("/data", methods=['GET', 'POST'])
def get_data_from_csv():
    if request.method == 'POST':
        file = request.files['csvfile']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join('static', filename))
            data = []
            with open(os.path.join('static', filename)) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    data.append(row)
            return render_template('get_data_from_csv.html', data=data)
    return render_template('get_data_from_csv.html')



@app.route("/search", methods=['GET', 'POST'])
def search_image_by_name():
    return render_template('search_image_by_name.html')


@app.route("/searchimage", methods=['GET', 'POST'])
def search_image_by_name_output():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/people.csv'))
        temp_path = ''
        for row in csv_reader:
            if name == row['Name']:
                temp_path = '../static/' + row['Picture']
        if temp_path:
            return render_template('search_image_by_name.html', image_path=temp_path, message="Found")
        else:
            return render_template('search_image_by_name.html', error="Picture not found!")


@app.route("/searchbysal", methods=['GET', 'POST'])
def search_person_by_salary():
    csv_reader = csv.DictReader(open('static/people.csv'))
    temp_path = []

    for row in csv_reader:
        if row['Salary'] == '' or row['Salary'] == ' ':
            row['Salary'] = 99000
        if int(float(row['Salary'])) < 99000 and row['Picture'] != ' ':
            temp_path.append('static/' + row['Picture'])
            print(temp_path)
            print(int(float(row['Salary'])))

    print(len(temp_path))
    if temp_path:
        return render_template('search_image_whose_salary_lessthan_99000.html', image_path=temp_path, message="Found")
    else:
        return render_template('search_image_whose_salary_lessthan_99000.html', error="Picture not found!")


@app.route("/edit", methods=['GET', 'POST'])
def edit_details_by_name():
    return render_template('edit_details_by_name.html')


@app.route("/editdetails", methods=['GET', 'POST'])
def editdetails_form():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/people.csv'))
        temp_name = ''
        for r in csv_reader:
            if name == r['Name']:
                temp_name = name
        if temp_name != '':
            return render_template('display_details_after_edit_by_name.html', name=temp_name)
        else:
            return render_template('display_details_after_edit_by_name.html', error="No Record Found!")


@app.route("/updatedetails", methods=['GET', 'POST'])
def display_updated_details():
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        salary = request.form['salary']
        grade = request.form['grade']
        room = request.form['room']
        picture = request.files['picture']  
        keyword = request.form['keyword']
        cnt = 0

        temp = [name, state, salary, grade, room, picture.filename, keyword]  
        line = []

        with open('static/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                if name == r[0]:
                    line.append(temp)
                else:
                    line.append(r)
                cnt += 1

        with open('static/people.csv', 'w') as csv_write:  
            csv_writer = csv.writer(csv_write)
            csv_writer.writerows(line)

        if cnt != 0:
            return render_template('display_details_after_edit_by_name.html', update="One Record Updated Successfully.")
        else:
            return render_template('display_details_after_edit_by_name.html', error="No Record Found!")
        
@app.route("/remove", methods=['GET', 'POST'])
def remove_details_by_name():
    return render_template('remove_by_name.html')


@app.route("/removedetails", methods=['GET', 'POST'])
def remove_details_message_display():
    if request.method == 'POST':
        name = request.form['name']
        cnt = 0
        line = list()
        with open('static/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for row in csv_reader:
                line.append(row)
                if name == row[0]:
                    line.remove(row)
                    cnt += 1

        csv_write = open('static/people.csv', 'w')
        for i in line:
            for j in i:
                csv_write.write(j + ',')
            csv_write.write('\n')

        if cnt:
            return render_template('removedetails_validation.html', message="Record removed successfully.")
        else:
            return render_template('removedetails_validation.html', error="Record not found.")


@app.route("/uploadpic", methods=['GET', 'POST'])
def upload_pic():
    return render_template('uploadpic.html')


@app.route("/uploadnew", methods=['GET', 'POST'])
def upload_new():
    if request.method == 'POST':
        file = request.files['img']
        file.save('static/' + file.filename)
        return render_template('uploaddisp.html', msg="Image uploaded successfully.")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
