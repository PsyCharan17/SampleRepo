import requests
from bs4 import BeautifulSoup
import io, base64
from pypdf import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi


def extract_transcript(video_id):
    video_id = video_id[video_id.find('=')+1:]
    print(video_id)
    text = ""
    val = YouTubeTranscriptApi.get_transcript(video_id)
    for i in val:
        text += i["text"]
    return text

def extract_data_from_pdf(base64_pdf_string):
    pdf_file = base64.b64decode(base64_pdf_string)
    file = io.BytesIO(pdf_file)
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text_temp = page.extract_text()
        text += text_temp
    return text

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.get_text()
    return text