from openai import AzureOpenAI, APITimeoutError, APIConnectionError, RateLimitError
import os
import time
from src.preprocess import extract_text
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv() 

# Initialize Azure OpenAI client with minimal configuration
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-15-preview"
)

# Load SBERT model for embeddings
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

def handle_rate_limit(e, max_retries=3, initial_delay=60):
    """Handle rate limit errors with exponential backoff."""
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            time.sleep(delay)
            return True
        except Exception:
            delay *= 2  # Exponential backoff
    return False

def extract_information(text, prompt):
    """Uses GPT-4 to extract structured information from a given text."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                messages=[
                    {"role": "system", "content": "You are an AI assistant skilled in extracting structured data from text."},
                    {"role": "user", "content": f"{prompt}\n{text}"}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content.strip()
        except RateLimitError as e:
            print(f"Rate limit hit (attempt {attempt + 1}/{max_retries}). Waiting...")
            if not handle_rate_limit(e):
                return "Error: Rate limit exceeded. Please try again later."
        except Exception as e:
            print(f"Error extracting information: {e}")
            if attempt == max_retries - 1:
                return "Error: Failed to extract information. Please try again later."
            time.sleep(2 ** attempt)  # Exponential backoff

def get_resume_details(resume_text):
    """Extracts skills, education, and experience from a resume using GPT-4."""
    prompt = """
    Extract key details from the resume:
    - List of skills mentioned
    - Education details (Degree, Major, University, Year of Graduation)
    - Work experience (Companies, Duration, Roles)
    Provide structured JSON output.
    """
    return extract_information(resume_text, prompt)

def get_job_description_details(jd_text):
    """Extracts required skills, qualifications, and experience from a job description using GPT-4."""
    prompt = """
    Extract key details from the job description:
    - List of required skills
    - Required education level
    - Preferred experience (if any)
    Provide structured JSON output.
    """
    return extract_information(jd_text, prompt)

def calculate_matching_score(resume_info, jd_info):
    """Calculates a matching score between resume and job description based on extracted data."""
    if not resume_info or not jd_info:
        return 0
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                messages=[
                    {"role": "system", "content": "You are an AI assistant skilled in job-resume matching."},
                    {"role": "user", "content": f"Compare the following resume details and job description. Assign a matching score (0-100) based on skills, education, and experience relevance.\n\nResume Details: {resume_info}\n\nJob Description: {jd_info}\n\nReturn only the score."}
                ],
                temperature=0.2
            )
            try:
                return int(response.choices[0].message.content.strip())
            except ValueError:
                return 0
        except RateLimitError as e:
            print(f"Rate limit hit (attempt {attempt + 1}/{max_retries}). Waiting...")
            if not handle_rate_limit(e):
                return 0
        except Exception as e:
            print(f"Error calculating matching score: {e}")
            if attempt == max_retries - 1:
                return 0
            time.sleep(2 ** attempt)  # Exponential backoff
    return 0

def calculate_sbert_similarity(resume_text, jd_text):
    """Calculates similarity score using SBERT embeddings."""
    resume_embedding = sbert_model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = sbert_model.encode(jd_text, convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(resume_embedding, jd_embedding).item() * 100
    return round(similarity_score, 2)

def get_combined_score(gpt_score, sbert_score):
    """Computes the final combined score as an average of GPT-4 and SBERT scores."""
    return round((gpt_score + sbert_score) / 2, 2)

if __name__ == "__main__":
    sample_resume = "../tests/sample_resume_1.pdf"  # Change to actual file path
    sample_job_desc = "../tests/job_description_1.txt"  # Change to actual file path
    
    resume_text = extract_text(sample_resume)
    job_desc_text = extract_text(sample_job_desc)
    
    resume_info = get_resume_details(resume_text)
    jd_info = get_job_description_details(job_desc_text)
    
    gpt_match_score = calculate_matching_score(resume_info, jd_info)
    sbert_similarity_score = calculate_sbert_similarity(resume_text, job_desc_text)
    combined_score = get_combined_score(gpt_match_score, sbert_similarity_score)
    
    print("Extracted Resume Info:\n", resume_info)
    print("\nExtracted Job Description Info:\n", jd_info)
    print("\nGPT-4 Matching Score:", gpt_match_score)
    print("SBERT Similarity Score:", sbert_similarity_score)
    print("Final Combined Score:", combined_score)