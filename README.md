Tag Toggler is an add-on for Anki 2 that lets you quickly add and edit tags
while reviewing.  You can customize keyboard shortcuts for editing all tags on
the current card, as well as quickly adding, deleting, or toggling specific
preset tags.  Optionally, you can bury or suspend the note after applying the
tags.

For example, here are some ways that I use the add-on:
- Toggle a 'hard' tag on the current card:

`    'H': {'tags': 'hard', 'action': 'toggle'}`

- Add a 'TODO' tag and bury the current card:

`    'T': {'tags': 'TODO', 'after': 'bury'}`

- Add an 'easy' tag and suspend the current card:

`    'A': {'tags': 'easy', 'after': 'suspend'}`

Tag Toggler was inspired by the [Quick
Tagging](https://github.com/cayennes/Quick_Tagging) add-on by Cayenne Boyer.

## Setup ##

Install the addon from the [Anki add-on
page](https://ankiweb.net/shared/addons/) by pasting the code 874498171 into
Anki (*Tools > Add-ons > Browse & Install...*).  After launching Anki,
customize the keybindings by editing the source code found under *Tools >
Add-ons*.

Customization is fairly straightforward, with instructions in the source code.

