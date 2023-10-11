# diceRollerBot

> A discord bot that performs "checks" on a randomly generated number between 1 and 20. To "Pass" the check, the roll of the dice(s) must have a value greater than or equal to the generated number. Conversely to that to "fail" a check means rolling dice(s) whose value is less than the generated number. Modifiers (to affect the value of the dice roll) are [planned to be] toggable and based on a successful or failed check can result in general changes to user's nickname, roles and permissions are [planned to be] toggable.

## Table of Contents

* [General Information](#general-information)
* [Softwares Used](#softwares-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
* [License](#license)

## General Information

* The purpose of this project was to make a simple discord bot that generates a number between 1 and 20 and have subsequent "dice rolls" that performs "checks" on that generated number. It is motivated and inspired by the Ability/Skill check game mechanic in D&D and Baldur's Gate 3.

## Softwares Used

* Microsoft Visual Studio Code - Version 1.82.2

## Features

* /roll <ability_check>
  * Simulate's an Ability or Skill Check
* /select_class <class_name> 
  * Allows users to select from the various classes available -- enables modifiers which can either add or subtract from the values seen in the /roll command
* /display_class
  * Displays the user's class if set
* /help
  * Custom help command that displays documentation about the bot's functionality and usage of valid commands

## Planned features

* Classes that are unique to users ✅
  * Edittable for each user ✅
  * Different classes provide different modifiers when performing the /roll command ✅
* Modifiers applied based on users' class profile in discord server
* General Manipulation of members, channels and/or server
  * Adjusting roles based on success or failure of checks
  * Adjusting nicknames based on success or failure of checks
  * Kicking Members or Moving Members based on failure of certain checks
  * Event Creation

## Screenshots

* To Be Added ...
<!-- If you have screenshots you'd like to share, include them here. -->

## Project Status

[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

## Room for Improvement

* Basic Functionality has been completed for:
  * Simulating the ability/skill check via the /roll command ✅
  * User's to set their classes which subsequently affect the values of future calls to the /roll command via modifiers ✅

To do:

* Integration of .yaml file to store users' classes
* Member properties manipulation
  * Roles
  * Nicknames
  * Kicking/Moving

## Acknowledgements

* This project was inspired by the Ability Checks in the video game titled Baldurs Gate 3

## Contact

Created by [@andrewkmag](https://github.com/andrewkmag) -- feel free to contact me!

## License

### Apache 2.0 License

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
