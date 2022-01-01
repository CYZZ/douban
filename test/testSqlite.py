import sqlite3




# 连接数据库
# conn = sqlite3.connect("test.db") # 打开或者创建数据库
# print("Opended database successfully")

# 连接数据库
# conn = sqlite3.connect("test.db") # 打开或者创建数据库
# c = conn.cursor() # 获取游标
# sql = '''
#     create table company
#         (id int primary key not null,
#         name text not null,
#         age int not null,
#         address char(50),
#         salary real);
# '''
# c.execute(sql) # 执行sql语句
# conn.commit() # 提交数据库操作
# conn.close() # 关闭数据连接
#
# print("连接数据库成功")

# 3. 插入数据
# conn = sqlite3.connect("test.db") # 打开或者创建数据库
# c = conn.cursor() # 获取游标
# sql = '''
#     insert into company (id,name, age, address, salary)
#     values (1, '张三', 30, '成都', 80000);
# '''
# c.execute(sql) # 执行sql语句
# conn.commit() # 提交数据库操作
# conn.close() # 关闭数据连接

print("连接数据库成功")

# 4. 查询数据
conn = sqlite3.connect("test.db") # 打开或者创建数据库
c = conn.cursor() # 获取游标
sql = '''
    select id, name, address, salary from company
'''
cursor = c.execute(sql) # 执行sql语句
for row in cursor:
    print("id=",row[0])
    print("name=",row[1])
    print("age=",row[2])
    print("address=",row[2])
    print("salary=",row[2])

conn.close() # 关闭数据连接