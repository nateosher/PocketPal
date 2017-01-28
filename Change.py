# Change.py
# Home of the CalculateChange function, which checks 

def CalculateChange(oldDate, newDate):
	sign = "-" if oldDate[6] > newDate[6] else "+"
	dif = str(abs(oldDate[6] - newDate[6]))
	if dif == "0":
		prefix = "No change in number of articles in last "
	elif dif == "1":
		prefix = sign + dif + " article in last "
	else:
		prefix = sign + dif + " articles in last "

	date_hash = {
		0 : "year",
		1 : "month",
		2 : "day",
		3 : "hour",
		4 : "minute",
		5 : "second"
	}

	for i in range(6):
		if oldDate[i] != newDate[i]:
			if newDate[i] - oldDate[i] == 1:
				return prefix + date_hash[i]
			else:
				return prefix + str(newDate[i] - oldDate[i]) + " " + date_hash[i] + "s"