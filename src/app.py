from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import tempfile
from src.preprocess import extract_text
from src.match_score import get_resume_details, get_job_description_details, calculate_matching_score, calculate_sbert_similarity, get_combined_score

app = FastAPI()

def save_upload_file(upload_file: UploadFile) -> str:
    """Save the uploaded file temporarily and return its path."""
    try:
        suffix = os.path.splitext(upload_file.filename)[-1]  # Get file extension
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(upload_file.file.read())  # Save content
            return temp_file.name  # Return file path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

@app.post("/match_score/")
async def match_score(resume: UploadFile = File(...), job_description: UploadFile = File(...)):
    try:
        resume_ext = os.path.splitext(resume.filename)[1].lower()
        job_desc_ext = os.path.splitext(job_description.filename)[1].lower()

        resume_text = extract_text(resume.file, resume_ext)
        job_desc_text = extract_text(job_description.file, job_desc_ext)

        print(f"Extracted Resume Text: {resume_text[:500]}")  # Print first 500 chars for debugging
        print(f"Extracted Job Description Text: {job_desc_text[:500]}")

        if not resume_text or not job_desc_text:
            raise HTTPException(status_code=400, detail="Failed to extract text from files")

        resume_info = get_resume_details(resume_text)
        jd_info = get_job_description_details(job_desc_text)

        gpt_match_score = calculate_matching_score(resume_info, jd_info)
        sbert_similarity_score = calculate_sbert_similarity(resume_text, job_desc_text)
        combined_score = get_combined_score(gpt_match_score, sbert_similarity_score)

        return {
            "resume_info": resume_info,
            "job_description_info": jd_info,
            "gpt_match_score": gpt_match_score,
            "sbert_similarity_score": sbert_similarity_score,
            "combined_score": combined_score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)