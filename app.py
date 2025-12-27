import pandas as pd 
import google.generativeai as genai 
from dotenv import  load_dotenv 
import os
from flask import Flask,render_template,request

load_dotenv() 

app=Flask(__name__) 

genai. configure(api_key=os.getenv("GEMINI_API_KEY"))
model=genai.GenerativeModel("gemini-2.5-flash") 

df=pd.read_csv("qa_data (1) (1).csv")

context_txt=""
for _,row in df.iterrows():
    context_txt +=f"Q: {row['question']}\nA: {row['answer']}\n\n"

def ask_gemini(query):
    prompt=f"""
    you are a Q&A assistant.
    Answer ONLY using teh context below.
    if the answer if not present,say:No relevant Q&Afound 

    context:
    {context_txt} 
        Question:{query}
  """
    response=model.generate_content(prompt)
    return response.text.strip() 

@app.route("/",methods=["GET","POST"])
def home():
    answer=""
    if request.method=="POST":
        query=request.form["query"]
        answer=ask_gemini(query)
    return render_template("index.html",answer=answer)


if __name__=="__main__":
    app.run()




    
