# refactor:
    ✅ Frame
    Card
    ✅ Divider
        (HorizontalDivider)
        (VerticalDivider)
    GroupBox

    ✅ Label
    ✅ Title
    ✅ subtitle
    ✅ description
    ✅ comment

    ✅ CheckBox
    ✅ RadioButton
    ✅ Switch

    ✅ LineEdit
    Unselectable read-only lineedit
    ✅ PlainTextEdit
    ✅ Overlay Vertical Scrollbar

    ✅ ComboBox

    SpinBox
    DoubleSpinBox

    Button
    ButtonGroup
    StrongButton


    Progress
    IndeterminateProgress
    RadialProgress
    ScrollBar
    SpinBox

    -  - flat icon button

    -  - flat icon + text button

    -  - flat button

    -  - button





differenciates buttons:
button
toggle_button

icon_button
toggle icon button

button_group

| Type               | Description                                                              |
| ------------------ | ------------------------------------------------------------------------ |
| **IconButton**     | Only an icon, flat, no background by default. Can toggle selected state. |
| **TextButton**     | Only text, flat, can be a toggle (selected or unselected).               |
| **TextIconButton** | Icon + text, flat, can be a toggle.                                      |


| Role                 | Implementation                                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Primary/strong**   | e.g., “Start Processing”, “Render”, “Export” → fully colored background (primary color), filled shape, high emphasis. Usually **not toggleable**. |
| **Checkable/toggle** | e.g., “Snap”, “Magnet”, “Loop” → flat button, icon/text color changes when selected, optional highlight outline or background on hover.           |


| Button Type               | Used For                | Visual Style                                                             |
| ------------------------- | ----------------------- | ------------------------------------------------------------------------ |
| **Strong Primary Action** | Render, Process, Export | **Filled**, bold color, icon+text                                        |
| **Secondary Action**      | Preview, Add Media      | Tonal or Outlined, icon+text                                             |
| **Toggle Tool**           | Edit modes              | Icon-only or icon+text; **tonal filled when active**, outlined when idle |
| **Low-Priority Action**   | Undo, Cancel            | Text buttons                                                             |


BaseButton(QPushButton)
 ├─ FlatButton(BaseButton)           # flat, text or icon, toggleable
 │    ├─ IconButton(FlatButton)
 │    ├─ TextButton(FlatButton)
 │    └─ TextIconButton(FlatButton)
 └─ StrongButton(BaseButton)         # filled, high emphasis, action
       └─ Optional: Icon/Text/Combo



Perfect — now we’re moving from “Material 3 mobile/desktop style” to **desktop video editor style**, which is a very different UX philosophy. Let’s carefully design this.

I’ll go step by step so the implementation will be clean and professional.

---

# 1️⃣ **Button Types for Video Editor**

We need 3 core button types:

| Type               | Description                                                              |
| ------------------ | ------------------------------------------------------------------------ |
| **IconButton**     | Only an icon, flat, no background by default. Can toggle selected state. |
| **TextButton**     | Only text, flat, can be a toggle (selected or unselected).               |
| **TextIconButton** | Icon + text, flat, can be a toggle.                                      |

---

# 2️⃣ **Differentiating Button Roles**

In video editing apps, buttons have different “strength” depending on their role:

| Role                 | Implementation                                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Primary/strong**   | e.g., “Start Processing”, “Render”, “Export” → fully colored background (primary color), filled shape, high emphasis. Usually **not toggleable**. |
| **Checkable/toggle** | e.g., “Snap”, “Magnet”, “Loop” → flat button, icon/text color changes when selected, optional highlight outline or background on hover.           |

**Guideline:**

* **Strong action button:** always filled, clearly visible.
* **Toggle buttons:** flat, no background or subtle hover, selected state changes icon/text color.

---

# 3️⃣ **Behavior Rules**

### **Flat buttons (toggle or not)**

* **Default:** icon/text neutral color (grey)
* **Hover:** slightly brighter icon/text (or subtle background)
* **Pressed:** brighter or inverted icon/text
* **Toggled/selected:** accent color (e.g., primary blue)

### **Strong buttons (primary action)**

* Filled background (primary color)
* White text/icon
* Hover: slightly darker/lighter background
* Pressed: even darker/lighter background

---

# 4️⃣ **Button Group Support**

* Already using `QButtonGroup` → good!
* Toggle buttons in a group: only **one selected at a time**.
* Flat buttons in a group: just change color when selected.

---

# 5️⃣ **Implementation Plan**

We can create a **clean class hierarchy**:

```
BaseButton(QPushButton)
 ├─ FlatButton(BaseButton)           # flat, text or icon, toggleable
 │    ├─ IconButton(FlatButton)
 │    ├─ TextButton(FlatButton)
 │    └─ TextIconButton(FlatButton)
 └─ StrongButton(BaseButton)         # filled, high emphasis, action
       └─ Optional: Icon/Text/Combo
```

### **Toggle behavior**

* FlatButton can be checkable (`setCheckable(True)`)
* Selected state changes icon/text color
* Use QSS or `update_style()` for runtime color changes

---

# 6️⃣ **Color Rules (for video editor dark UI)**

Assuming dark theme (common in video editing):

| Type      | Normal       | Hover      | Pressed    | Selected   |
| --------- | ------------ | ---------- | ---------- | ---------- |
| Flat      | #888888      | #ffffff    | #cccccc    | #2196F3    |
| Strong    | #2196F3 bg   | #1976D2 bg | #1565C0 bg | #2196F3 bg |
| Text/Icon | Same as flat | same       | same       | accent     |

* Flat buttons: **no background**, only icon/text color changes.
* Strong buttons: **background filled**, text/icon white.

---

# 7️⃣ **Next Step**

I can now generate a **single-file PySide6 demo** for your **desktop video editor** buttons:

* Flat Icon Button (toggleable)
* Flat Text Button (toggleable)
* Flat Text+Icon Button (toggleable)
* Strong Button (filled)
* Demonstrate toggle groups
* Dark theme

This will be **ready to copy & run**, no Material 3 background hacks.

---

Do you want me to **generate the full Python demo file now**?
