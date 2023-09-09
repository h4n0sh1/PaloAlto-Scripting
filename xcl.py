import subprocess
import sys, os
import pip

try:
	import pandas as pd
except ModuleNotFoundError as e:
	print("Installing module", e.name)
	pip.main(['install', e.name])
	#subprocess.check_call([sys.executable, '-m', 'pip', 'install', e.name], stdout=subprocess.DEVNULL)

cols = ['Tags',	'Type',	'Source Zone', 'Source Address', 'Source User', 'Source HIP Profile',
	     'Destination Zone', 'Destination Address', 'Application', 'Service', 'Action']

def compare_rule(f,e,i,j,outer,inner,f1,f2):
    prompt = 1
    for col in cols:
        #print(f"{outer[col][i]}, {outer[col][j]}, {outer[col][i] != inner[col][j]}")
        if(outer[col][i] != inner[col][j]):
            if(prompt):
                print(f"\nDelta discovered in rule {outer['Name'][i]}")
                prompt = 0
            print(f"  Delta on col {col}\n    Outer Rule - {f1} = {outer[col][i]}\n    Inner Rule - {f2} = {inner[col][j]}\n")
	

def csv_diff(path1,path2):

	print(f"Reading  csv {path1} ...")
	df1 = pd.read_csv(path1)
	print(f"Reading  csv {path2} ...")
	df2 = pd.read_csv(path2)

	if (len(df2) > len(df1)):
		outer = df2
		f1=path2
		inner = df1
		f2=path1
	else:
		outer = df1
		f1=path1
		inner = df2
		f2=path2
	
	diff = []
	# Dumb non optimized look 
	for i,f in enumerate(outer['Name']):
		present = 0
		for j,e in enumerate(inner['Name']):
			if e in f or f in e:
				compare_rule(f,e,i,j,outer,inner,f1.split(os.path.sep)[-1],f2.split(os.path.sep)[-1]) #In-depth check 
				present = 1
		if not present:
			diff.append(f)
	#print(f"{path2} - Outer Diff : {diff}")
	
	diff = []
	# Dumb non optimized look
	for f in inner['Name']:
		present = 0
		for e in outer['Name']:
			if e in f or f in e:
				present = 1
		if not present:
			diff.append(f)
	#print(f"{path1} - Inner Diff : {diff}")


if __name__ == "__main__":
	#import env here
	csv_diff(path1,path2)
	print('')
	csv_diff(path1,path3)
	#diff = [f for f in df1['Name'] for e in df2['Name'] if e not in f and f not in e] 
	#print(diff)