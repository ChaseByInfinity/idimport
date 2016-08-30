from id import * 

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        if request.form['fname'] and request.form['lname'] and request.form['card_id']:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            
            if file.filename == '':
                flash('No selected snapshot')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                fname = request.form['fname']
                lname = request.form['lname']
                card_id = request.form['card_id']
            
                student = Student(fname, lname, str(filename), 'G', datetime.now(), card_id)
                db.session.add(student)
                db.session.flush()
                db.session.commit()
            
                flash('You\'re in. Welcome to the ID Lab.')
                return render_template('index.html')
        else:
            flash('You must fill out all fields')
    return render_template('index.html')



