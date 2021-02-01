from flask import Flask, request, render_template, redirect, url_for
from text_comaprison.text_similarity_evaluator import main

app = Flask(__name__)

comparison = {}

@app.route("/")
def hello_world():
  return "Hello, World!"

@app.route('/compare_text_info')
def get_texts():
    return '''
    <p>First text given: {}</p>
    <p>Second text given: {}</p>
    <p>The similarity score is: {}</p>'''\
    .format(comparison["First text"], comparison["Second text"], \
    comparison["Similarity score"])

@app.route('/compare_texts', methods=['GET', 'POST'])
def compare_texts():
    if request.method == 'POST':
      comparison["First text"] = '"No text given yet for comparison"'
      comparison["Second text"] = '"No text given yet for comparison"'
      comparison["Similarity score"] = '"Not calculated yet"'
      first_text = str(request.form['first_text'])
      second_text = str(request.form['second_text'])
      if first_text is "" and second_text is not "":
          comparison["Second text"] = second_text
      elif second_text is "" and first_text is not "":
          comparison["First text"] = first_text
      elif first_text and second_text:
          comparison["Similarity score"] = main(first_text, second_text)
          comparison["First text"] = first_text
          comparison["Second text"] = second_text
      return redirect(url_for('get_texts'))
    return render_template("compare_texts.html")
