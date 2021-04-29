import re


totalText='Khoảng 1.300.000.000 kết quả (0,45 giây)'
total = int(re.sub("[', ]", "",
		re.search("(([0-9]+[', ])*[0-9]+)",
		totalText).group(1)))
print(total)