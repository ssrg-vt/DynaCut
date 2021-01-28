<h1> This tool adds VMAs to the CRIU snapshot folder </h1>

Input :

<ul>
<li> Path to the dump folder </li>
<li> Start address of the VMA region in HEX </li>
<li> End address of the VMA region in HEX </li>
<li> Number of 4k pages to be added </li>

Example:

```
sudo python3 criu-add-vmas.py /home/abhijit/criu-dump/dump3/ 0x1000 0x5000 4
```
