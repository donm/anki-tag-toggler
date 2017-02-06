# Tag Toggler 1.2.2 (2017-02-06)
# Copyright: Don March <don@ohspite.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Tag Toggler is an Anki 2 add-on for quickly adding tags while reviewing.

# Based in part on Quick Tagging by Cayenne Boyer
# (https://github.com/cayennes/Quick_Tagging)

########################################
## CONFIGURATION INSTRUCTIONS

## There are two variables to edit--tag_dialog_shortcut and tag_shortcuts.

## Lines with a leading `#` are comments and have no effect.  Lines with a
## single `#` are code examples that you can use by removing the leading `#`.

## You can overwrite some previously existing shortcuts, but it's easiest if
## you pick keys that are unused or that are shortcuts when reviewing cards
## only (defined in Reviewer._keyHandler).  Some keys (such as 'A' for Add or
## 'B' for Browse are defined elsewhere; the effect of adding Tag Toggle
## functionality to these keys is not well defined.

## Keybindings are strings that specify modifiers plus the primary key that
## triggers the action.  If the primary key is a letter, it must be uppercase.

## You can specify keybindings that include any combination of the following
## modifier keys: Meta, Ctrl, Alt, Shift.  When including modifiers they must
## be listed in that order (Meta, Ctrl, Alt, Shift), omitting any that you
## don't want to use.

## Examples of correct and incorrect keybindings:
##
##     'T'                     # correct (T key without any modifiers)
##     'Shift+T                # correct (T key while holding Shift)
##     'Meta+Ctrl+Alt+Shift+T' # correct
##     'Ctrl+Shift+T'          # correct
##
##     't'                     # incorrect (letter keys must be uppercase)
##     'Shift+Ctrl+T'          # incorrect (wrong modifier order)
##     'ctrl+shift+T'          # incorrect (case is significant)

## If you are unsure how to bind a particular key combination, you can
## uncomment the following line in the tagKeyHandler function:
##
##     showInfo(key_sequence)
##
## When reviewing cards, this will catch and display all key combinations that
## are pressed.

########################################
## CONFIGURATION OPTIONS

## Change `tag_dialog_shortcut` to the key you want to open a dialog to
## quickly edit tags.  Set `tag_dialog_shortcut = None` to disable the
## shortcut.
tag_dialog_shortcut = 'T'
# tag_dialog_shortcut = 'Shift+T'
# tag_dialog_shortcut = None

## Add items to the `tag_shortcuts` dict to create shortcuts that modify
## tags. The dict keys are the key for the keyboard shortcut, and each should
## refer to a dict to specify the command.  Valid keys in that dict are
## 'tags', 'action', and 'after'.
##
## 'tags': Specify tags to modify in a string; separate multiple tags in the
## string with spaces.
##
## 'action': How to modify tags; options are 'add' (the default), 'delete',
## and 'toggle' (delete tag if present, add it if absent).
##
## 'after': What to do to a card after modifying the tags; options are
## 'bury-card', 'bury-note', 'suspend-card' or 'suspend-note'.  Also 'suspend'
## and 'bury, which are the same as the '-note' versions.
##
## Example keybinding to add tags:
##    'h': {'tags': 'hard'}
## 'add' is the default action, so this is the same:
##    'h': {'tags': 'hard', 'action': 'add'}
## Modify multiple tags by separating them with spaces:
##    'h': {'tags': 'hard marked'}
## Keybinding to delete tags (if they are present):
##    'h': {'tags': 'hard marked', 'action': 'delete'}
## Keybinding to toggle tag:
##    'Shift+H': {'tags': 'hard', 'action': 'toggle'}
## Bury a card after adding a tag:
##    'Shift+T': {'tags': 'TODO', 'after': 'bury-card'}
## Suspend a note after adding a tag:
##    'Shift+E': {'tags': 'easy', 'after': 'suspend-note'}
## Use all modifier keys to do the same thing:
##    'Meta+Ctr+Alt+Shift+E': {'tags': 'easy', 'after': 'suspend-note'}

tag_shortcuts = {
#    'Shift+H': {'tags': 'hard', 'action': 'toggle'},
#    'Shift+T': {'tags': 'TODO', 'after': 'bury-note'},
#    'Shift+A': {'tags': 'easy', 'after': 'suspend-card'},
}

## END CONFIGURATION
########################################

# Testing:

# As far as I know, there is no easy way to automatically test this.  Here are
# some keybindings to add to `tag_shortcuts` that cover most cases.  (Be sure
# to test `tag_dialog_shortcut` as well).

# The first two should cause a graceful error when Anki is starting up.
    # 'Z': {'tags': 'test-a', 'action': 'blah'},
    # 'Shift+Z': {'tags': 'test-a', 'after': 'blah'},
    # 'Z': {'tags': 'test-a'},
    # 'Shift+Z': {'tags': 'test-b'},
    # 'X': {'tags': 'test-a', 'action': 'delete'},
    # 'Shift+X': {'tags': 'test-b', 'action': 'delete'},
    # 'C': {'tags': 'test-a test-b'},
    # 'Alt+C': {'tags': 'test-a test-b', 'action': 'delete'},
    # 'Alt+Shift+C': {'tags': 'test-a test-b', 'action': 'toggle'},
    # 'Alt+Z': {'tags': 'test-a test-b', 'after': 'bury-card'},
    # 'Alt+Shift+Z': {'tags': 'test-a test-b', 'after': 'suspend-card'},
    # 'Meta+Ctrl+Alt+Shift+Z': {'tags': 'lots-of-modifier-keys'}


from PyQt4.QtCore import Qt
from PyQt4.QtGui import QKeySequence

from aqt import mw
from aqt.utils import getTag, tooltip, showInfo
from aqt.reviewer import Reviewer
from anki.hooks import wrap


def tagKeyHandler(self, event, _old):
    """Wrap default _keyHandler with new keybindings."""
    key = event.key()

    if key == Qt.Key_unknown:
        _old(self, event)
    # only modifier pushed
    if (key == Qt.Key_Control or
        key == Qt.Key_Shift or
        key == Qt.Key_Alt or
        key == Qt.Key_Meta):
        _old(self, event)

    # check for combination of keys and modifiers
    modifiers = event.modifiers()
    if modifiers & Qt.ShiftModifier:
        key += Qt.SHIFT
    if modifiers & Qt.ControlModifier:
        key += Qt.CTRL
    if modifiers & Qt.AltModifier:
        key += Qt.ALT
    if modifiers & Qt.MetaModifier:
        key += Qt.META

    key_sequence = QKeySequence(key).toString(QKeySequence.PortableText)

    ## Uncomment this to display keybinding strings for keys that are pressed
    ## when reviewing cards:

    # showInfo(key_sequence)

    note = mw.reviewer.card.note()
    if tag_dialog_shortcut and key_sequence == tag_dialog_shortcut:
        mw.checkpoint(_("Edit Tags"))
        edit_tag_dialog(note)
    elif key_sequence in tag_shortcuts:
        binding = tag_shortcuts[key_sequence]
        if 'action' not in binding:
            binding['action'] = 'add'

        same_card_shown = False
        if ('after' in binding and
            binding['after'] in ['suspend', 'suspend-note']):
            mw.checkpoint("Edit Tags and Suspend Note")
            tooltip_message = 'Suspended note and edited tags: {}'
            self.mw.col.sched.suspendCards(
                [card.id for card in self.card.note().cards()])
        elif 'after' in binding and binding['after'] in ['bury', 'bury-note']:
            mw.checkpoint("Edit Tags and Bury Note")
            tooltip_message = 'Buried note and edited tags: {}'
            mw.col.sched.buryNote(note.id)
        elif 'after' in binding and binding['after'] == 'suspend-card':
            mw.checkpoint("Edit Tags and Suspend Card")
            tooltip_message = 'Suspended card and edited tags: {}'
            self.mw.col.sched.suspendCards([self.card.id])
        elif 'after' in binding and binding['after'] == 'bury-card':
            mw.checkpoint("Edit Tags and Bury Card")
            tooltip_message = 'Buried card and edited tags: {}'
            mw.col.sched.buryCards([self.card.id])
        else:
            mw.checkpoint(_("edit Tags"))
            tooltip_message = 'Edited tags: {}'
            same_card_shown = True

        tag_edits = edit_note_tags(note, binding['tags'], binding['action'])
        reset_and_redraw(same_card_shown)
        tooltip(tooltip_message.format(tag_edits))
    else:
        _old(self, event)


def edit_tag_dialog(note):
    """Prompt for tags and add the results to note."""
    prompt = _("Edit tag list:")
    (tag_string, dialog_status) = getTag(mw, mw.col, prompt, default=note.stringTags())
    if dialog_status != 0:  # means "Cancel"
        note.setTagsFromStr(tag_string)
        note.flush()
        reset_and_redraw(same_card_shown=True)
        tooltip('Tags set to: "{}"'.format(tag_string))


def reset_and_redraw(same_card_shown=False):
    """Rebuild the scheduler and redraw the card."""
    in_answer_state = (mw.reviewer.state == "answer")
    if same_card_shown:
        mw.reviewer.card.load()
        mw.reviewer.cardQueue.append(mw.reviewer.card)
    mw.moveToState("review")

    if in_answer_state and same_card_shown:
        try:
            mw.reviewer._showAnswer()
        except:
            pass


def edit_note_tags(note, tags, action='add'):
    """Apply action to each space separated tag in the string `tags`."""
    tag_list = mw.col.tags.split(tags)
    additions = []
    deletions = []
    for tag in tag_list:
        if action == 'delete':
            if note.hasTag(tag):
                note.delTag(tag)
                deletions.append(tag)
        elif action == 'toggle':
            if note.hasTag(tag):
                note.delTag(tag)
                deletions.append(tag)
            else:
                note.addTag(tag)
                additions.append(tag)
        else:  # action == 'add'
            if not note.hasTag(tag):
                note.addTag(tag)
                additions.append(tag)
    note.flush()

    messages = []
    if additions:
        messages.append("added: \"{}\"".format(" ".join(additions)))
    if deletions:
        messages.append("removed: \"{}\"".format(" ".join(deletions)))
    if messages:
        return "\n".join(messages)
    else:
        return "(no changes)"


def shortcuts_are_okay():
    error_message = (
        "The Tag Toggle add-on will not be started.\n\n"
        "Check the configuration for an undefined '{}' "
        "value '{}' in tag_shortcuts:\n\n"
        "{}")

    def check_command(command, command_type, options):
        if command_type in command:
            value = command[command_type]
            if value not in options:
                showInfo(error_message.format(command_type, value, command))
                return False
        return True

    for shortcut in tag_shortcuts:
        command = tag_shortcuts[shortcut]
        if not check_command(command, 'action', ['add', 'delete', 'toggle']):
            return False
        if not check_command(command, 'after',
                             ['bury', 'bury-card', 'bury-note',
                              'suspend', 'suspend-card', 'suspend-note']):
            return False

    return True


if shortcuts_are_okay():
    Reviewer._keyHandler = wrap(Reviewer._keyHandler, tagKeyHandler, "around")
