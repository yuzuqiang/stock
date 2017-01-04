def get_shcodes():
	sfile = open('codes.csv', 'r')
	codes =[] 
	for line in sfile:
		codes.append(line.split(',', 8)[0].strip(' '))
	sfile.close()

	print(codes)
	dfile = open('codes','w')
	for each in codes:
		print(each,file=dfile) 
	dfile.close()
	return codes

if __name__ == '__main__':
	get_shcodes()
