import json
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from model import extract_fields_of_study
from compare import compare_fields
from predict import  get_chatgpt_response, create_prompt, create_data_string
# from compare import get_fields_of_study
import pandas as pd
import csv
from openai import OpenAI

import openai
import csv

client = OpenAI()
def read_data(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = list(reader)
    return header, data

def create_data_string(data):
    data_string = "\n".join([", ".join(row) for row in data])
    print(data_string)
    return data_string
def clean_and_process_response(response_text: str):
    # Loại bỏ các phần không cần thiết
    cleaned_response = response_text.strip().lstrip('```json').rstrip('```').strip()
    
    try:
        # Phân tích chuỗi JSON từ phản hồi đã được làm sạch
        data = json.loads(cleaned_response)
        return data
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in response")
def admin_chat(user_input, data_string, structure):

    prompt = f"""
    Given the input: "{user_input}"
    Extract years ,the name of the majors and the number of request of that major that are mentioned in the user input based on data from {data_string}.
    YOU MUST EXTRACT THE DATA FULLY AND ACCURATELY, IF THE NUMBER OF REQUEST IS 0, PLEASE RETURN 0.
    Please response your answer in format JSON:    
    {structure}
    ----------------------------------------
    
    ONLY JSON IS ALLOWED as an answer. No explanation or other text is allowed.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    extracted_fields = response.choices[0].message.content
    print(extracted_fields)

    return clean_and_process_response(extracted_fields.strip())




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class UserInput(BaseModel):
    input_text: str

@app.post("/process/")
async def process_input(user_input: UserInput):
    #Extract fields of study from user input
    fields_of_study = get_fields_of_study()
    extracted_fields = extract_fields_of_study(user_input.input_text, fields_of_study)
    print(f"Asnwer: {extracted_fields}")
    #Compare extracted fields with data
    comparison_result = ""
    if extracted_fields.lower() != "no answer":
        comparison_result = compare_fields(extracted_fields)
    
    # #Generate final output
    # final_output = generate_output(comparison_result)
    
    # return {"extracted_fields": extracted_fields, "comparison_result": comparison_result,"final_output": final_output}
    return {"extracted_fields": extracted_fields, "comparison_result": comparison_result}

@app.post("/prompt-report/")
async def process_report(user_input: UserInput):
# Đường dẫn tới file dữ liệu
    df = pd.read_csv('./data/data.csv')
    
    data_string = df.to_dict(orient="records")
    struture = """
    [
        {
            "date": number,
            "sector": string,
            "value": number
        }
    
    ]"""
        
    print(data_string)
    extract = admin_chat(user_input.input_text, data_string, struture)

    return extract
            
def get_fields_of_study():
    fields_of_study = ["Công nghệ ô tô số", "Trí tuệ nhân tạo", "Kỹ thuật phần mềm", 
                       "Hệ thống thông tin", "An toàn thông tin", "Thiết kế mỹ thuật số",
                       "Digital marketing","Kinh doanh quốc tế", "Quản trị kinh doanh",
                       "Quản trị dịch vụ du lịch và lữ hành","Logistic và quản lý chuỗi cung ứng",
                       "Tài chính","Truyền Thông đa phương tiện","Quan hệ công chúng",
                       "Ngôn ngữ Anh","Ngôn ngữ Hàn","Ngôn ngữ Nhật","Ngôn ngữ Trung","Vi mạch bán dẫn"]
    return fields_of_study


@app.get("/visualize/")
async def visualize_data():
    data_path = r'C:\Code\PengiChatbot\Challenge_3\data\data.csv'
    with open(data_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = list(reader)
    
    chatgpt_response = get_chatgpt_response(prompt=create_prompt(create_data_string(data)))
    final_output = f"{chatgpt_response}"
    return final_output



@app.get("/search/")
def search(year: Optional[int] = None, sectors: Optional[List[str]] = Query(None)):
    df = pd.read_csv('./data/data.csv')
    if year is not None and year not in df['Năm'].values:
        raise HTTPException(status_code=404, detail="Year not found")

    if sectors:
        # Kiểm tra xem tất cả các ngành có tồn tại trong dữ liệu không
        for sector in sectors:
            if sector not in df.columns:
                raise HTTPException(status_code=404, detail=f"Sector {sector} not found")

    # Lọc theo năm
    if year is not None:
        result = df[df['Năm'] == year]
    else:
        result = df

    # Lọc theo danh sách ngành
    if sectors:
        result = result[['Năm'] + sectors]

    formatted_result = []
    for _, row in result.iterrows():
        year = row['Năm']
        for sector in sectors or df.columns[1:]:
            formatted_result.append({
                "date": int(year),
                "sector": sector,
                "value": int(row[sector]) if not pd.isna(row[sector]) else None
            })

    return formatted_result

@app.get("/sectors")
def get_sectors():
    # Đọc file CSV
    df = pd.read_csv('./data/data.csv')
    # Chuyển đổi dữ liệu sang định dạng dictionary
    headers = df.columns[1:].tolist()
    return {"sectors": headers}
    return data