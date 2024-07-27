import matplotlib.pyplot as plt
requests_2024 = [877, 806, 1002, 841, 810, 790, 851, 840, 862, 760, 750, 780, 790, 762, 801, 758, 741, 730, 610]
majors = ["Công nghệ ô tô số", "Trí tuệ nhân tạo", "Kỹ thuật phần mềm", 
                       "Hệ thống thông tin", "An toàn thông tin", "Thiết kế mỹ thuật số",
                       "Digital marketing","Kinh doanh quốc tế", "Quản trị kinh doanh",
                       "Quản trị dịch vụ du lịch và lữ hành","Logistic và quản lý chuỗi cung ứng",
                       "Tài chính","Truyền Thông đa phương tiện","Quan hệ công chúng",
                       "Ngôn ngữ Anh","Ngôn ngữ Hàn","Ngôn ngữ Nhật","Ngôn ngữ Trung","Vi mạch bán dẫn"]
plt.figure(figsize=(14, 8))
plt.bar(majors, requests_2024, color='skyblue')
plt.xlabel('Chuyên ngành', fontsize=14)
plt.ylabel('Số lượng yêu cầu', fontsize=14)
plt.title('Số lượng yêu cầu của từng chuyên ngành trong năm 2024', fontsize=16)
plt.xticks(rotation=90)
plt.show()