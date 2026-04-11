from flask import Flask, render_template, request, send_file
from io import BytesIO
import re
import textwrap

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ImportError:
    canvas = None
    letter = None

import config
import aicontent
import blog

def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__)
app.config.from_object(config.config['development'])
app.register_error_handler(404, page_not_found)


def _safe_filename(value):
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", (value or "generated-output").strip().lower())
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "generated-output"


def _strip_markdown(text):
    if not text:
        return ""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*[-*]\s+", "- ", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    return text


@app.route('/download-pdf', methods=["POST"])
def download_pdf():
    if canvas is None or letter is None:
        return "PDF export requires reportlab. Install it with: pip install reportlab", 500

    title = (request.form.get('title') or "Generated Output").strip()
    content = (request.form.get('content') or "").strip()
    category = (request.form.get('category') or "content").strip()

    if not content:
        return "No content found to export.", 400

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    page_width, page_height = letter
    x_margin = 48
    y = page_height - 55

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(x_margin, y, title[:95])
    y -= 24

    pdf.setFont("Helvetica", 11)
    clean_text = _strip_markdown(content)
    for paragraph in clean_text.splitlines():
        lines = textwrap.wrap(paragraph, width=98) if paragraph.strip() else [""]
        for line in lines:
            if y < 55:
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = page_height - 55
            pdf.drawString(x_margin, y, line)
            y -= 16

    pdf.save()
    buffer.seek(0)

    filename = f"{_safe_filename(category)}-output.pdf"
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())



@app.route('/product-description', methods=["GET", "POST"])
def productDescription():

    if request.method == 'POST':
        submission = request.form['productDescription']
        query = "Generate a detailed product description for: {}".format(submission)
        openAIAnswer = aicontent.openAI(query)
        prompt = 'AI Suggestions for {} are:'.format(submission)

    return render_template('product-description.html', **locals())



@app.route('/job-description', methods=["GET", "POST"])
def jobDescription():

    if request.method == 'POST':
        submission = request.form['jobDescription']
        query = "Create a detailed job description for: {}".format(submission)
        openAIAnswer = aicontent.openAI(query)
        prompt = 'AI Suggestions for {} are:'.format(submission)

    return render_template('job-description.html', **locals())



@app.route('/tweet-ideas', methods=["GET", "POST"])
def tweetIdeas():

    if request.method == 'POST':
        submission = request.form['tweetIdeas']
        query = "Generate twitter content for: {}".format(submission)
        openAIAnswer = aicontent.openAI(query)
        prompt = 'AI Suggestions for {} are:'.format(submission)

    return render_template('tweet-ideas.html', **locals())



@app.route('/cold-emails', methods=["GET", "POST"])
def coldEmails():

    if request.method == 'POST':
        submission = request.form['coldEmails']
        query = "Write a cold email to potential clients about: {}".format(submission)
        openAIAnswer = aicontent.openAI(query)
        prompt = 'AI Suggestions for {} are:'.format(submission)

    return render_template('cold-emails.html', **locals())



@app.route('/social-media', methods=["GET", "POST"])
def socialMedia():

    if request.method == 'POST':
        submission = request.form['socialMedia']
        query = "Generate social media content for: {}".format(submission)
        openAIAnswer = aicontent.openAI(query)
        prompt = 'AI Suggestions for {} are:'.format(submission)

    return render_template('social-media.html', **locals())


@app.route('/business-pitch', methods=["GET", "POST"])
def businessPitch():

    if request.method == 'POST':
        submission = request.form['businessPitch']
        query = "Create a business proposal for: {}".format(submission)
        openAIAnswer = aicontent.openAI(query)
        prompt = 'AI Suggestions for {} are:'.format(submission)

    return render_template('business-pitch.html', **locals())


@app.route('/video-ideas', methods=["GET", "POST"])
def videoIdeas():

    if request.method == 'POST':
        submission = request.form['videoIdeas']
        query = "Generate video ideas for: {}".format(submission)
        openAIAnswer = aicontent.openAI(query)
        prompt = 'AI Suggestions for {} are:'.format(submission)

    return render_template('video-ideas.html', **locals())


@app.route('/video-description', methods=["GET", "POST"])
def videoDescription():

    if request.method == 'POST':
        submission = request.form['videoDescription']
        query = "Generate video content for: {}".format(submission)
        openAIAnswer = aicontent.openAI(query)
        prompt = 'AI Suggestions for {} are:'.format(submission)

    return render_template('video-description.html', **locals())

@app.route('/blog-ideas', methods=["GET", "POST"])
def generateBlogTopics():

    if request.method == 'POST':
        submission = request.form['blogIdeas']
        query = "Generate blog topics on: {}. \n \n 1.  ".format(submission)
        openAIAnswer = aicontent.openAI(query)
        prompt = 'AI Suggestions for {} are:'.format(submission)

    return  render_template('blog-ideas.html', **locals())











if __name__ == '__main__':
    app.run(debug=True)
