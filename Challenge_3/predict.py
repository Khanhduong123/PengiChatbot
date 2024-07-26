import csv
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI()

def read_data(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = list(reader)
    return header, data

def create_data_string(data):
    data_string = "\n".join([", ".join(row) for row in data])
    return data_string

def create_prompt(data_string):
    
    prompt = f"""
    Report the number of requests on each majors on the year 2024 based on data from {data_string}.
    
    Please create a HISTOGRAM CHART showing the number of requests for each major in 2024. 
    AND WHEN YOU LABEL THE COLUMNS OF THE HISTOGRAM, LABEL AS FOLLOWS:
    majors = ["Công nghệ ô tô số", "Trí tuệ nhân tạo", "Kỹ thuật phần mềm", 
                       "Hệ thống thông tin", "An toàn thông tin", "Thiết kế mỹ thuật số",
                       "Digital marketing","Kinh doanh quốc tế", "Quản trị kinh doanh",
                       "Quản trị dịch vụ du lịch và lữ hành","Logistic và quản lý chuỗi cung ứng",
                       "Tài chính","Truyền Thông đa phương tiện","Quan hệ công chúng",
                       "Ngôn ngữ Anh","Ngôn ngữ Hàn","Ngôn ngữ Nhật","Ngôn ngữ Trung","Vi mạch bán dẫn"]
    Think step by step, you are a professional business analyst. From the histogram you plot above, propose marketing strategies to further strengthen the top popular specialties.
    PLEASE GENERATE THE RESPONSE IN VIETNAMESE.
    """
    return prompt

def get_chatgpt_response(prompt):
    # openai.api_key = "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"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt}
        ],
        
    )
    
    return response.choices[0].message.content.strip()

# def generate_output(comparison_result):
#     head,data = read_data('D:\\software\\Hackathon\\Challenge_3\\data\\data.csv')
#     chatgpt_response = get_chatgpt_response(prompt=create_prompt(create_data_string(data)))
    
#     final_output = f"Final output based on data\n\n{chatgpt_response}"
#     return final_output

