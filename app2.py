import streamlit as st
from dotenv import load_dotenv
load_dotenv()   ## Load all the enviorment valiable
import google.generativeai as genai
import os

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


prompt = """You are the Youtube Video summarizer. You will taking the transcript text and summarizing the 
entire video and providing the important voce in point within 250 words. The transcript is appended here : """

## Getting the summary
def generate_gemini_content(transcript_text,prompt):
    model= genai.GenerativeModel("gemini-pro")
    response= model.generate_content(prompt+transcript_text)
    return response.text


## Extractcting the Transcript    
def extract_Transcript_detail(youtube_video_link):
    try:
        video_id = youtube_video_link.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript = ""
        for i in transcript_text:
            transcript += " "+i["text"]
        return transcript

    
    except Exception as e:
        raise e
        
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_Transcript_detail(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
