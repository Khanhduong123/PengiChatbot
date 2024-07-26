from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import extract_fields_of_study
from compare import compare_fields
from predict import  get_chatgpt_response, create_prompt, create_data_string
# from compare import get_fields_of_study
import csv

app = FastAPI()

class UserInput(BaseModel):
    input_text: str

@app.post("/process/")
async def process_input(user_input: UserInput):
    #Extract fields of study from user input
    fields_of_study = get_fields_of_study()
    extracted_fields = extract_fields_of_study(user_input.input_text, fields_of_study)
    
    #Compare extracted fields with data
    comparison_result = compare_fields(extracted_fields)
    
    # #Generate final output
    # final_output = generate_output(comparison_result)
    
    # return {"extracted_fields": extracted_fields, "comparison_result": comparison_result,"final_output": final_output}
    return {"extracted_fields": extracted_fields, "comparison_result": comparison_result}


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
    data_path = 'D:\\software\\Hackathon\\Challenge_3\\data\\data.csv'
    with open(data_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = list(reader)
    
    chatgpt_response = get_chatgpt_response(prompt=create_prompt(create_data_string(data)))
    final_output = f"{chatgpt_response}"
    return final_output



