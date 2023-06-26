from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)


bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)

output = {}
table = 'visitor'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def survey():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    visits = request.form['visits']
    recommendation = request.form['response']
    time = request.form['time']
    country = request.form['country']
    city = request.form['city']
    email = request.form['email']
    comments = request.form['comments']
    guest_image = request.form['image']

    insert_sql = "INSERT INTO visitor VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if guest_image.filename == "":
        return "Please enter a file"
    try:
        cursor.execute(insert_sql, (firstname, lastname, visits, recommendation, time,
                                    country, city, email, comments))
        db_conn.commit()
        guest_name = " " + firstname + " " + lastname
        # Upload image in s3
        guest_img_file_name = "guest-" + lastname + "_image-file"
        s3 = boto3.resource('s3')

        try:
            print('Data inserted in MySQL RDS... uploading image to S3')
            s3.bucket(custombucket).put_object(
                Key=guest_img_file_name, Body=guest_image)
            bucket_location = boto3.client(
                's3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location, custombucket, guest_img_file_name)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=guest_name)


if __name__ == '__main__':
    app.run(debug=True)
