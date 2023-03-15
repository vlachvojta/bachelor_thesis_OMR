param ($in_ext, $out_ext, $in_dir='.') #, $out_dir='out')

echo "Welcome to simple powershel script with parameters"
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
# echo "output directory: $out_dir"

# $DIR = "D:\OneDrive - Vysoké učení technické v Brně\skola\BP\datasets\musescore_pipeline_44\1_musicxml_using_MuseScore4_native_CLI"

Get-ChildItem $in_dir -Filter *.$in_ext | 
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