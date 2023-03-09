# $DIR = "D:\OneDrive - Vysoké učení technické v Brně\skola\BP\datasets\musescore_pipeline_44\1_musicxml_using_MuseScore4_native_CLI"
$DIR = "..\..\..\datasets\musescore_pipeline_44\1_musicxml_using_MuseScore4_native_CLI\"

echo "Hellou"

echo $DIR

Get-ChildItem $DIR -Filter *.mscz | 
ForEach-Object { 
	if (-not(Test-Path "$($DIR)$($_).musicxml")) 
		{ 
			echo $_ ; 
			musescore4 --export-to "$($_.FullName).musicxml" $_.FullName 
		} 
	else
		{
			echo "already exists" 
		} 
	}