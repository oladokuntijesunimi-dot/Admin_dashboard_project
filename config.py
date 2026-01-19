import os
from dotenv import load_dotenv

load_dotenv()

class Config:
   # Use the model you specified.
   # Fallback to 'llama-3.3-70b-versatile' if that specific custom ID isn't public.
   MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"
   GROQ_API_KEY = os.getenv("GROQ_API_KEY")
   TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

   
