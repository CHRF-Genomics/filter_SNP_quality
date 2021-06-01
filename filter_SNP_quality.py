'''
To filter high-quality SNPs from a VCF file. It uses the Quality score (QUAL) of the VCF file to filter. Also, discards any SNPs with mixed or ambiguous bases. 
Although, we have not used these criteria. But, with little modification, the script can also filter using Mapping quality (MQ) and Read_ratio (from DP4) data in a VCF file. 

Written by Arif Tanmoy (arif.tanmoy@chrfbd.org).
Last updated: 01 JUNE 2021
'''
from argparse import (ArgumentParser, FileType)

def parse_args():
	"Parse the input arguments, use '-h' for help"
	commands = ArgumentParser(description='Filter VCF file for unambiguous bases and high quality.')
	commands.add_argument('--vcf', type=str, required=True,
						help='Mapped raw VCF file, with DP4 scores. (Required)')
	commands.add_argument('--phr', type=int, required=False, default=20,
						help='Minimum Phred-Score. Default 20.')
	commands.add_argument('--output', type=str, required=False, default='Filtered_for_phylo.vcf',
						help='Output file.')
	return commands.parse_args()
args = parse_args()

phrdQ = float(args.phr)

with open(args.output, 'w') as output:
	for line in open(args.vcf, 'r'):
		if line.startswith("#") == True:
			output.write(line)
		else:
			element = line.split("\t")
			phrd = float(element[5])
			info = element[7]
			mapqual = float(info.split('MQ=')[1].split(';')[0])
			hqread = info.split('DP4=')[1].split(';')[0].split(',')
			read = float((int(hqread[2])+int(hqread[3]))/(int(hqread[0])+int(hqread[1])+int(hqread[2])+int(hqread[3])))
			readALTf = int(hqread[2])
			readALTr = int(hqread[3])
			FMT_read_dep = int(element[9].split(':')[2])
			# **Discard**: Following the values
			# 2nd: Ambiguous base (>1 base); Phred_quality =<20;
			if (len(element[4])==1) and (phrd > phrdQ):
				output.write(line)
			else:
				continue
output.close()
