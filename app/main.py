from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import URL
from app.schemas import URLCreateRequest, URLCreateResponse
from app.shortener import encode, decode

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

basehost = "http://localhost:8000"


@app.post("/shorten", response_model=URLCreateResponse)
def create_short_url(request: URLCreateRequest, db: Session = Depends(get_db)):
    new_url = URL(original_url=str(request.url))
    db.add(new_url)
    db.commit()
    db.refresh(new_url) 

    short_code = encode(new_url.id)

    return URLCreateResponse(
        short_code=short_code,
        short_url=f"{basehost}/{short_code}",
        original_url=new_url.original_url,
    )


@app.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    try:
        url_id = decode(short_code)
    except ValueError:
        raise HTTPException(status_code=404, detail="Invalid short url")

    url_entry = db.query(URL).filter(URL.id == url_id).first()
    if url_entry is None:
        raise HTTPException(status_code=404, detail="Invalid short url")

    return RedirectResponse(url=url_entry.original_url)



