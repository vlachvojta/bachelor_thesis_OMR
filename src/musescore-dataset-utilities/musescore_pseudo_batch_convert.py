
import os
import sys

rel_dir = os.path.dirname(os.path.relpath(__file__))
sys.path.append(os.path.join(rel_dir, '..', 'dataset-utilities'))
from common import Common  # noqa: E402


def run_command(command: str):
    print(f'running: {command}')
    os.system(command)



def main():
    in_ext = 'mscz'
    out_ext = 'png'
    in_dir = '.'

    files = os.listdir(in_dir)
    files = [os.path.join(in_dir, f) for f in files if f.endswith(in_ext)]

    # print(len(files))
    # print(files)


    for file_in in files:
        file_out = Common.change_file_extesion(file_in, out_ext)
        # print(f'{file_in} -> {file_out}')

        command = f'MuseScore4.exe {file_in} -o {file_out}'
        run_command(command)


# Get-ChildItem $in_dir -Filter *.$in_ext | 
# ForEach-Object { 
# 	if (-not(Test-Path "$($DIR)$($_).$out_ext")) 
# 		{ 
# 			echo $_ ; 
# 			musescore4 $_.FullName --export-to "$($_.FullName).$out_ext"
# 		} 
# 	else
# 		{
# 			echo "already exists" 
# 		} 
# 	}

commandos = ' MuseScore4.exe 100000_p00.mscz -o 100000_p00.png'

if __name__ == "__main__":
    main()
