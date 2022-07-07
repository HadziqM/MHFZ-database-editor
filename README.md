# MHFZ-database-editor  <br />
## How to make app work  <br />
download latest release on https://github.com/HadziqM/MHFZ-database-editor/releases/tag/2.1 <br/>
extract then edit database.ini in database_editor folder to your postgres credential  <br />
## How to utilize app  <br />
open database_editor.exe  <br />
the label in bottom of app is kind of terminal to show output  <br />
if you got cur not defined error in console then its connection timed out <br />
press "reconnect" button to solve the issue <br />
### Course editor  <br />
- you can search your user name with "search" button  <br />
- you can checklist the course to select course you need to operate with  <br />
- use "set specific" to set value in calculator to your specific username   <br />
- use "set all" to set value in calculator to all username in database  <br />
- use "set default" to set value in calculator to be default value for your course   <br />
- set default mean whenever new username created in your database   <br />
it will have the set value automatically   <br />
### GCP editor   <br />
- you can search your character name with "search" button  <br />
- you can scan the database with "scan all" to scan not null character name  <br />
- use "set specific" to set value in input to your specific character name   <br />
- use "set all" to set value in input to all character in database  <br />
- use "add specific" to add value in input with your specific character name   <br />
- use "add all" to add value in input with all character in database  <br />
- use "sub specific" to substract your character gcp with input value  <br />
- use "sub all" to substract  gcp of all character in database with input value  <br /> <br />
**_all the subtract value cant go bellow 0, if it calculated bellow 0 it will be 0 instead_**   <br /> <br />
**_all command only work on not null gcp_**  <br />
### Transmog editor   <br />
- make sure there is skin_hist.bin in your directory (its added there as default dont worry)   <br />
- use "set specific" to unlock all transmog in game to specific character   <br />
- use "set all" to unlock all transmog to all character in database   <br />
### Gacha coin   <br />
- use "set spe prem" to set premium gacha coin in input value to specific character name   <br />
- use "set spe trial" to set trial gacha coin in input value to specific character name   <br />
- use "set all prem" to set premium gacha coin in input value to all character    <br />
- use "set all trial" to set trial gacha coin in input value to all character   <br />
### Guild Edit
- use "rp spec" to set RP from input value to specific guild name   <br />
- use "rp all" to set RP from input value to all guild in database  <br />
### Login Boost Edit
- use "search" to know your character id <br />
- use "turn off spe" to turn off specific character login boost <br />
- use "turn on spe" to reset specific character login boost <br />
- use "turn off all" to turn off all character login boost <br />
- use "turn on all" to reset all specific character login boost <br /> <br />
**_login boost may not worked and may work, fix not done yet_**
### Road Edit
- you can open csv file from your pc and upload it to postgres <br />
- check "header" if have header in your csv file <br />
- you can add add item tou your roadshop at other item section <br />
- you can decode from hexa code item by using "conv ferias" and "conv untranslated" <br />
- if you get the hex from ferias you could use "conv ferias" <br />
- if you want to add untraslated item in game, use "conv untranslated" to decode the hex <br />
### Save file edit
- you can upload savefile.bin in your local to postgres <br />
- you can upload partner.bin in your local to postgres <br /> <br />
**_be cautius that the charachter name will be overwriten with new savefile you uploaded_**
