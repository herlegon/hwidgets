# port from RLG for pynnlib_gui

Accordion
IndeterminateProgressIndicator

- correct QCombobox:
    - when in read write
    - windows: wrong text size and top margin
    - Linux Only: keep pushed and release on an item
    - edition doesn't work because it should put the cursor and not open the popup


- HLineEdit
    * when enter key: validate current text, deselect (and focus next widget)
    * escape: undo modifications, deselect and focus out

- HButton (icon)
    * use an internal check state: rewrite


# Later
Scrollbar
ProgressIndicator
Tooltip



Links:
https://www.figma.com/community/file/1143831050419793062/apple-macos-12-design-system-for-figma


