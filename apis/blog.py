from fastapi import APIRouter,Depends,status,HTTPException,Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import  Form, UploadFile, File, Request, Depends
from fastapi.templating import Jinja2Templates
from typing import List
from sqlalchemy.orm import Session
from db.database import get_db
from db.schemas.blog_schema import Blog,Section
import os 
import shutil
from fastapi.responses import JSONResponse

templates = Jinja2Templates(directory="templates")
UPLOAD_FOLDER = "media"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def form_view(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@router.post("/submit/")
async def submit(
    title: str = Form(),
    email: str = Form(),
    section_types: list[str] = Form(...),
    contents: list[str] = Form(...),
    files: list[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    blog = Blog(title=title, email=email)
    db.add(blog)
    db.commit()
    db.refresh(blog)

    saved_files = []
    file_idx = 0
    content_idx = 0  # 👈 NEW

    for sec_type in section_types:
        if sec_type in ["image", "video"]:
            file = files[file_idx]
            path = f"media/{file.filename}"
            with open(path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            saved_files.append(path)
            section = Section(
                type=sec_type,
                file_path=path,
                content=None,
                blog_id=blog.id
            )
            file_idx += 1
        else:  # Assume it's "text"
            section = Section(
                type=sec_type,
                content=contents[content_idx],
                file_path=None,
                blog_id=blog.id
            )
            content_idx += 1

        db.add(section)

    db.commit()
    return {"message": "Blog created successfully", "blog_id": blog.id}

@router.get("/view-all", response_class=HTMLResponse)
def view_all_blogs(request: Request, db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return templates.TemplateResponse("view_all.html", {"request": request, "blogs": blogs})

@router.get("/blogs/")
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()

    result = []
    for blog in blogs:
        sections_data = [
            {
                "id": sec.id,
                "type": sec.type,
                "content": sec.content,
                "file_path": sec.file_path
            }
            for sec in blog.sections
        ]
        result.append({
            "id": blog.id,
            "title": blog.title,
            "email": blog.email,
            "sections": sections_data
        })

    return JSONResponse(content=result)