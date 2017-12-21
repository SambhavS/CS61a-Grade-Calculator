from bs4 import BeautifulSoup
"""
Okpy Grade Calculator for CS61a Fall 2017

Note: Make Sure To Use Python3

Instructions: 
Please save your okpy html page as an html document and put it in this folder.
Make sure it is saved as 'index.html'
Run the program by calling | $python3 calc.py | in your terminal.

Made by Sambhav Sunkerneni
"""

#Initializations
participation, hw, exam, extra_cred, projects = 0, 0, 0, 0, 0
uncomplete_scores, point_scores, part_scores = {}, {}, {}
grade_to_score = [
	"A+  ≥ 296",
	"A   ≥ 280",
	"A-  ≥ 265",
	"B+  ≥ 245",
	"B   ≥ 225",
	"B-  ≥ 205",
	"C+  ≥ 195",
	"C   ≥ 185 ",
	"C-  ≥ 175",
	"D+  ≥ 170",
	"D   ≥ 165",
	"D-  ≥ 160"]

#Setup Beautiful Soup
with open("index.html") as fp:
    soup = BeautifulSoup(fp,"lxml")
rows = soup.find_all("tr")[1:]

#Analyze Each Assignment
for row in rows:
	vals = row.find_all("a")
	name = vals[0].contents[0].lower().strip()
	if len(vals) == 2:
		grade_tag = vals[1]
		grade = grade_tag.contents[0]
		score = float(grade[grade.index(":") + 1 :])
		if ("quiz" in name) or ("check-off" in name) or ("free participation point" in name) or ("lab" in name):
			participation += score
			part_scores[name] = score
		else:
			point_scores[name] = score
			if "homework" in name:
				hw += score
			elif "contest" in name or "ec" in name:
				extra_cred += score
			elif "midterm" in name or "final" in name:
				exam += score
			else:
				print("Error: Unsure Where This Item Goes")
				print(name, score)
	elif len(vals) == 1:
		uncomplete_scores[name] = 0
	elif name == "homework 1":
		#Special Case For Homework 1
		grade_tag1, grade_tag2 = vals[1], vals[2]
		point_scores[name] = score
		grade1 = grade_tag1.contents[0]
		grade2 = grade_tag2.contents[0]
		score1 = float(grade1[grade1.index(":") + 1 :])
		score2 = float(grade2[grade2.index(":") + 1 :])
		hw += max(score1,score2)
	else:
		#Projects
		grade_tags = vals[1:]
		scores = {}
		for tag in grade_tags:
			info = tag.contents[0]
			colon = info.index(":")
			label = str(info[:colon]).strip()
			score = float(info[colon+1:])
			scores[label] = score
		project_score = 0
		if "Revision" in scores and "Composition" in scores:
			project_score += max(scores["Revision"],scores["Composition"])
			scores["Revision"], scores["Composition"] = 0, 0
		for val in scores.values():
			project_score += val
		point_scores[name] = project_score
		projects += project_score

#Adjustments
participation = min(participation,10)
overall_list = [hw, exam, extra_cred, projects, participation]
overall_dict = {"hw (out of 25)":hw,"exam (out of 165)":exam, "extra_cred (out of 0)":extra_cred, "projects (out of 100)":projects, "participation (out of 10)":participation}
final_points = sum(overall_list)
def get_grade(score):
	if score >=296:
		return "A+"
	elif score >= 280:
		return "A"
	elif score >= 265:
		return "A-"
	elif score >= 245:
		return "B+"
	elif score >= 225:
		return "B"
	elif score >= 205:
		return "B-"
	elif score >= 195:
		return "C+"
	elif score >= 185:
		return "C"
	elif score >= 175:
		return "C-"
	elif score >= 170:
		return "D+"
	elif score >= 165:
		return "D"
	elif score >= 160:
		return "D-"
	else:
		return "F"

def setup():
	print()
	ready = input("Please save your okpy html page as an html document and put it in this folder. Make sure it is saved as 'index.html' If you have done that, enter 1. Otherwise enter 2. ")
	if ready != '1':
		print()
		print("Bye! Re-run the program once you have added your html page.")
		print()
	else:
		main(True)

def main(first):
	print()
	if first:
		print("Your Final Score is",final_points,"out of 300.("+get_grade(final_points)+")")
	print("Enter the number that corresponds to the data you would like to see:")
	print("1 : All Scores")
	print("2 : Scores For Each Category")
	print("3 : Score to Grade Table")
	print("4 : Exit")
	choice = int(input("Your Numerical Choice: "))
	print()
	if(choice == 4):
		print("Goodbye & good luck!")
	else:
		if choice == 1:
			print()
			print("Point Scores")
			for key,val in point_scores.items():
				print(key,val)
			print()
			print("Participation Scores")
			for key,val in part_scores.items():
				print(key,val)
			print()
			print("Uncompleted Assignment Scores")
			for key,val in uncomplete_scores.items():
				print(key,val)
		elif choice == 2:
			for key, val in overall_dict.items():
				print(key,val)
		elif choice == 3:
			for pair in grade_to_score:
				print(pair)
		main(False)

#Main Call
setup()
