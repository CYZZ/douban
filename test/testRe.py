# 正则表达式
import re

# 创建模式对象
pat = re.compile("AA")
m = pat.search("CBAAA") # 找到第一个匹配的

m = re.search("asd", "fdjkfdjklasd")

print(m)
print(re.findall("[A-Z]", "fadjkaadjkfldajfFFkl;dAAAA"))
print(type(re.findall("", "")))

print(re.findall("[A-Z]+", "ADFfdadfREQREHGFDAfdaRE"))

print(re.sub("a", "A", "abcdefgasd")) # 找到a 用A替换
a = r"adfkda\fda\a"
print(a)



