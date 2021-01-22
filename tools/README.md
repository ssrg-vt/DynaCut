<h1>Readme for the tools</h1> 

<h2>criu-data-parser.py:</h2>

This tool parses JSON files created using the CRIT tool and prints out process image information

Input: Path to the CRIU dump folder

<h3>Pre-requisites:</h3> 

CRIT decoded "MM" image file and the CRIT decoded "PAGEMAP" image file

The CRIT decoded "MM" image file should be named: mm_dump.json

The CRIT decoded "PAGEMAP" image file should be named: pagemap_dump.json

Example: 
```
python3 criu-data-parser.py /home/abhijit/criu-dump/dump6
```

<h2>criu-modify-binary.py:</h2>
This tool modifies a CRIU pages-1.img file to restore a modified version of the process

Input: Path to the CRIU dump folder and the address of the variable that needs to be modified

<h3>Pre-requisites:</h3> 

CRIT decoded "MM" image file and the CRIT decoded "PAGEMAP" image file

The CRIT decoded "MM" image file should be named: mm_dump.json

The CRIT decoded "PAGEMAP" image file should be named: pagemap_dump.json

Example: 
```
python3 criu-data-parser.py /home/abhijit/criu-dump/dump6 0x404044
```
