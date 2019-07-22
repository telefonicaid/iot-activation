#!/bin/sh

show_menus() {
	clear
	echo #########################################
	echo "      SELECT CLOUD"
	echo #########################################
	echo "1. AWS"
	echo "0. Exit"
}

read_options(){
	local option
	read -p "Enter option: " option
	case $option in
		1) echo "1. AWS option..."; cd cloud/aws; sh AWS.sh ; exit 0;;
		0) echo "0. Exit option..."; exit 0;;
		*) echo "Invalid option..." && sleep 2
	esac
}

while true
do 
	show_menus
	read_options
done
