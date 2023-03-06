$DIR = "H:\Vojta_TODO_uklidit\bp_dataset_musescore\Musescore-unzipped\1_musicxml\0\0_2\"

echo "Hellou"

echo $DIR

Get-ChildItem $DIR -Filter *.mscz | 
ForEach-Object { 
	if (-not(Test-Path "$($DIR)$($_).musicxml")) 
		{ 
			echo $_ ; .\MuseScore4.exe --export-to "$($_.FullName).musicxml" $_.FullName 
		} 
	else
		{
			echo "already exists" 
		} 
	}