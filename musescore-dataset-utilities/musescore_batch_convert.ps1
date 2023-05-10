# PowerShell script for automatic converting files using MuseScore Command line interface
# Author: Vojtěch Vlach
# Contact: xvlach22@vutbr.cz

param ($in_ext, $out_ext, $in_dir='.')

if ($in_ext -eq $null){
	$in_ext = read-host -Prompt "Please enter the INPUT files extension"
} else {
	echo "input files extension: $in_ext"
}
if ($out_ext -eq $null){
	$out_ext = read-host -Prompt "Please enter the OUTPUT files extension"
} else {
	echo "output files extension: $out_ext"
}

echo "directory with input files: $in_dir"

Get-ChildItem $in_dir -Filter *.$in_ext -Recurse | 
Sort-Object @{expression = {$_.fullname}} -descending | 
ForEach-Object { 
	if (-not(Test-Path "$($DIR)$($_).$out_ext")) 
		{ 
			echo $_ ; 
			musescore4 $_.FullName --export-to "$($_.FullName).$out_ext"
		} 
	else
		{
			echo "already exists" 
		} 
	}