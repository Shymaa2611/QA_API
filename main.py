from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from qamodels import QuestionAnswer,Base
from transformers import T5ForConditionalGeneration, T5Tokenizer
DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "No result"}

""" def create_question(question: str, answer: str):
    session = Session()
    db_question = QuestionAnswer(question=question, answer=answer)
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    session.close()
    return {"status_code": 200, "message": "success"}
 """

def get_answer(question:str):
   checkpoint_path = 'model'
   checkpoint_path_tokenizer='tokenizer'
   tokenizer = T5Tokenizer.from_pretrained(checkpoint_path)
   model = T5ForConditionalGeneration.from_pretrained(checkpoint_path_tokenizer)
   input_text = question
   input_ids = tokenizer.encode(input_text, return_tensors='pt')
   output_ids = model.generate(input_ids, max_length=50, num_beams=4, early_stopping=True)
   output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True) 
   return output_text



#@app.get("/get_qa/")
def get_data(question:str):
   # answer=get_answer(question)
    if question:
        question_data = {"question": question, "answer":"There is No Answer !"}
        return question_data
    else:
        return "There is No Question !"

if __name__=="main":
    question="whatis the computer science"
    answer=get_data(question)
    print(answer)
