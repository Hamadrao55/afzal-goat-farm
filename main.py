from fastapi import FastAPI, Depends, Form, Request, responses
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, database

# Auto-create tables in Supabase
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def dashboard(request: Request, db: Session = Depends(database.get_db)):
    goats = db.query(models.Goat).all()
    
    # Calculate Total Income and Expenses
    income = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.type == "Income").scalar() or 0
    expenses = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.type == "Expense").scalar() or 0
    net_balance = income - expenses
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "goats": goats, 
        "income": income, 
        "expenses": expenses, 
        "net_balance": net_balance
    })

@app.post("/add_goat")
def add_goat(tag_id: str = Form(...), breed: str = Form(...), weight: float = Form(...), db: Session = Depends(database.get_db)):
    new_goat = models.Goat(tag_id=tag_id, breed=breed, weight=weight)
    db.add(new_goat)
    db.commit()
    return responses.RedirectResponse(url="/", status_code=303)

@app.post("/add_finance")
def add_finance(description: str = Form(...), amount: float = Form(...), type: str = Form(...), db: Session = Depends(database.get_db)):
    new_tx = models.Transaction(description=description, amount=amount, type=type)
    db.add(new_tx)
    db.commit()
    return responses.RedirectResponse(url="/", status_code=303)