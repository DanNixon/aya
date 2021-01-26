EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 3
Title "Aya"
Date "2021-01-27"
Rev "1"
Comp ""
Comment1 "Split QMK Keyboard"
Comment2 "https://github.com/DanNixon/aya"
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 4000 1500 1050 450 
U 601213E8
F0 "Right Hand Side" 50
F1 "side.sch" 50
F2 "HAND_SELECT" I R 5050 1600 50 
F3 "VCC" I R 5050 1700 50 
F4 "GND" I R 5050 1800 50 
$EndSheet
$Sheet
S 1500 1500 1000 500 
U 60124365
F0 "Left Hand Side" 50
F1 "side.sch" 50
F2 "HAND_SELECT" I R 2500 1600 50 
F3 "VCC" I R 2500 1700 50 
F4 "GND" I R 2500 1800 50 
$EndSheet
Wire Wire Line
	2500 1600 2600 1600
Wire Wire Line
	2600 1600 2600 1700
Wire Wire Line
	2600 1700 2500 1700
Wire Wire Line
	5050 1600 5150 1600
Wire Wire Line
	5150 1600 5150 1800
Wire Wire Line
	5150 1800 5050 1800
$EndSCHEMATC
