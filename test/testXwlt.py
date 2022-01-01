import xlwt

workbook = xlwt.Workbook(encoding="utlf-8")
worksheet = workbook.add_sheet('sheet')
# worksheet.write(0, 0, "hello")

for i in range(1, 10):
    for j in range(1, 10):
        worksheet.write(i-1, j-1, str(i) + "*" + str(j) + "=" + str(i * j))
workbook.save('student.xls')
