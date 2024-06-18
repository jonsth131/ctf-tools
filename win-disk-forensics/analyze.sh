#!/bin/bash
# Windows disk analysis script
# Author: jonsth131

VERSION="1.0.0"

RED='\033[0;31m'
TURQUOISE='\033[0;36m'
GREEN='\033[0;32m'
RESET='\033[0m'

WINDOWS_DIR=$1
OUTPUT_DIR=$2

function usage() {
	echo -e "Usage: ./analyze.sh <windows_dir> <output_dir>"
}

function header() {
	echo -e "Windows disk analysis v$VERSION"
	echo -e "----------------------------"
}

function main() {
	echo -e "${TURQUOISE}Select an option:${RESET}"
	commands=("Analyze User Directory" "Dump EVTX Data" "Dump Defender Quarantine" "Dump Powershell History" "Quit")
	select command in "${commands[@]}"; do
		case $REPLY in
		1)
			analyze_user_dir
			;;
		2)
			evtx_dump
			;;
		3)
			defender_quarantine
			;;
		4)
			dump_powershell_history
			;;
		5)
			echo "Quit"
			break
			;;
		*)
			echo "Invalid option"
			;;
		esac
	done
}

function analyze_user_dir() {
	function print_files() {
		if [ ! -z "$2" ]; then
			echo -e "${TURQUOISE}$1${RESET}"
			echo -e "$2"
		fi
	}
	USERS=$(ls $WINDOWS_DIR/Users | grep -v "\\$" | grep -vi desktop.ini)
	echo -e "Analyzing $user directory"
	select user in $USERS; do
		echo -e "-------------------------------------------------------"

		DOWNLOADS=$(ls -R $WINDOWS_DIR/Users/$user/Downloads | grep -v desktop.ini)
		DESKTOP=$(ls -R $WINDOWS_DIR/Users/$user/Desktop | grep -v desktop.ini)
		DOCUMENTS=$(ls -R $WINDOWS_DIR/Users/$user/Documents | grep -v desktop.ini)
		PICTURES=$(ls -R $WINDOWS_DIR/Users/$user/Pictures | grep -v desktop.ini)
		VIDEOS=$(ls -R $WINDOWS_DIR/Users/$user/Videos | grep -v desktop.ini)
		MUSIC=$(ls -R $WINDOWS_DIR/Users/$user/Music | grep -v desktop.ini)

		print_files "Downloads" "$DOWNLOADS"
		print_files "Desktop" "$DESKTOP"
		print_files "Documents" "$DOCUMENTS"
		print_files "Pictures" "$PICTURES"
		print_files "Videos" "$VIDEOS"
		print_files "Music" "$MUSIC"

		return
	done
}

function evtx_dump() {
	if ! command -v evtx_dump.py &>/dev/null; then
		echo -e "${RED}Error: evtx_dump.py is not installed.${RESET}"
		echo -e "Please install using 'pip install python-evtx' or 'pipx install python-evtx'"
		return
	fi

	echo "Dumping EVTX data to $OUTPUT_DIR/evtx"

	if [ ! -d "$OUTPUT_DIR/evtx" ]; then
		mkdir -p $OUTPUT_DIR/evtx
	fi

	find "${WINDOWS_DIR}/Windows/System32/winevt/Logs" -type f -name "*.evtx" -print0 | while IFS= read -r -d '' file; do
		echo "Dumping ${file}"
		BASENAME=$(basename -s .evtx "${file}")
		evtx_dump.py "${file}" >"$OUTPUT_DIR/evtx/${BASENAME}.txt"
	done
}

function defender_quarantine() {
	if ! command -v defender-dump.py &>/dev/null; then
		echo -e "${RED}Error: defender-dump.py is not installed.${RESET}"
		echo -e "Please install it from https://github.com/knez/defender-dump"
		return
	fi

	echo "Dumping Windows Defender quarantine to $OUTPUT_DIR/quarantine.tar"

	defender-dump.py -d "${WINDOWS_DIR}"
	if [ -f "quarantine.tar" ]; then
		mv quarantine.tar $OUTPUT_DIR
	fi
}

function dump_powershell_history() {
	echo "Dumping Powershell history"
	if [ ! -d "$OUTPUT_DIR/powershell" ]; then
		mkdir -p $OUTPUT_DIR/powershell
	fi

	if ! command -v evtx_dump.py &>/dev/null; then
		echo -e "${RED}Error: evtx_dump.py is not installed.${RESET}"
		echo -e "Please install using 'pip install python-evtx' or 'pipx install python-evtx'"
		echo -e "Ignoring powershell history from event logs"
	else
		echo "Dumping Powershell history from event logs"
		evtx_dump.py "${WINDOWS_DIR}/Windows/System32/winevt/Logs/Microsoft-Windows-PowerShell%4Operational.evtx" | grep -oE '<Data Name="ScriptBlockText">(.*)<\/Data>' >$OUTPUT_DIR/powershell/powershell_evtx_history.txt
		cat $OUTPUT_DIR/powershell/powershell_evtx_history.txt
	fi
}

header

if [ "$#" -ne 2 ]; then
	usage
	exit 1
fi

if ! [ -d "$1" ]; then
	echo -e "${RED}Error: $1 is not a valid directory.${RESET}"
	exit 1
fi

if ! [ -d "$2" ]; then
	echo -e "${RED}Error: $2 is not a valid directory.${RESET}"
	exit 1
fi

echo -e "Windows disk directory: $WINDOWS_DIR"
echo -e "Output directory: $OUTPUT_DIR"

main
