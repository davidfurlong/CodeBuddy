CodeBuddy
=========

Learn sublime text 3 shortcuts while programming.

## Shortcuts offered by package

### Text Shortcuts

- CMD + J **Join line below to the end of the current line**
- CMD + (up) **Swap line with line above**
- CMD + (down) **Swap line with line below**
- CMD + L **Select line**
- CMD + X **Delete line if no selected region, Cut behaviour**
- CMD + [ **Unindent**
- CMD + ] **Indent**
- ^ + M **Go to matching bracket**
- CMD + / **Comment Line**
- CMD + Shift + D **Duplicate Line**

### Non-text Shortcuts 

- CMD + K + B **Toggle Sidebar**
- CMD + P **Quick-open files by name**
- CMD + P + : **Goto line in current file**
- CMD + R **Goto symbol, Goto word in current file**
- Click "Find Results" left Gutter **Go to file and line**

## Compatibility

Sublime Text 3
OSX, Linux, Windows

## Dependencies

SubNotify
https://github.com/facelessuser/SubNotify

Growl (OSX)

## Sublime Text 3 Api 

Note: this call never seems to occur
```
post_text_command(view, command_name, args) 
```

https://www.sublimetext.com/docs/3/api_reference.html#sublime.Region


## Future plans

- Scrolling detection and recommendations
- Reindent

### Alternate delivery of info

Commented out are previously popups of the now native notifications, it is trivial to reinstate these in the case that none work. Contact me if struggling.

### License

MIT License, Copyright 2014 David Furlong

Note this doesn't include the unused scrolling code at the end

