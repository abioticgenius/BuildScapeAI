from flask import Flask, render_template, request, jsonify, url_for, session
from utils import FormUtils, ImageGenerationUtils
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/generate_image', methods=['POST'])
def generate_image():
    bedrooms = session.get('bedrooms')
    bathrooms = session.get('bathrooms')
    garage = session.get('garage')
    kitchen = session.get('kitchen')
    prompt = request.form['user_input']

    final_prompt = ImageGenerationUtils.make_final_prompt(bedrooms, bathrooms, garage, kitchen, prompt)
    image_info = ImageGenerationUtils.generate_floor_plan(final_prompt)

    if 'path' in image_info:
        image_path = url_for('static', filename=f'images/current/{os.path.basename(image_info["path"])}')
        return jsonify({'image_path': image_path})
    else:
        return jsonify({'error': image_info.get('error', 'Image generation failed.')})

@app.route('/step1', methods=['GET', 'POST'])
def step1():
    form = FormUtils.Step1Form()
    if form.validate_on_submit():
        session['bedrooms'] = form.rooms.data
        return redirect(url_for('step2'))
    return render_template('step1.html', form=form)

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    form = FormUtils.Step2Form()
    if form.validate_on_submit():
        session['bathrooms'] = form.bathrooms.data
        return redirect(url_for('step3'))
    return render_template('step2.html', form=form)

@app.route('/step3', methods=['GET', 'POST'])
def step3():
    form = FormUtils.Step3Form()
    if form.validate_on_submit():
        session['garage'] = form.garage.data
        return redirect(url_for('step4'))
    return render_template('step3.html', form=form)

@app.route('/step4', methods=['GET', 'POST'])
def step4():
    form = FormUtils.Step4Form()
    if form.validate_on_submit():
        session['kitchen'] = form.kitchen.data
        return redirect(url_for('step5'))
    return render_template('step4.html', form=form)

@app.route('/step5', methods=['GET', 'POST'])
def step5():
    form = FormUtils.Step5Form()
    if form.validate_on_submit():
        session['prompt'] = form.prompt.data
        return redirect(url_for('generate_image'))
    return render_template('step5.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)