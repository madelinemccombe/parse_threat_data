####!/usr/bin/env python3
"""
simple dictionaries to tag data based on filetype
"""

# key is the file name in the data source
# first list item is the filetype group tag
# second list item is the Autofocus label

filetypetags = {
                "7z": ["7zip", "7zip Archive"],
                "apk": ["Android", "Android APK"],
                "class": ["JAVA", "JAVA Class"],
                "dll32": ["DLL", "DLL"],
                "dll64": ["DLL", "DLL64"],
                "dmg": ["Apple-Mac", "MacOSX DMG"],
                "doc": ["Word", "Microsoft Word 97 - 2003 Document"],
                "docx": ["Word", "Microsoft Word Document"],
                "elf": ["ELF", "ELF"],
                "elink": ["Link", "Link"],
                "exe32": ["PE", "PE"],
                "exe64": ["PE", "PE64"],
                "fat": ["Apple-Mac", "Apple's Universal binary file"],
                "jar": ["Java", "JAVA JAR"],
                "java": ["Java", "JAVA Class"],
                "macho": ["Apple-Mac", "Mach-O"],
                "macro": ["Macro", " Macro"],
                "NULL": ["NULL", "Others"],
                "pdf": ["PDF", "PDF"],
                "pkg": ["Apple-Mac", "Mac OS X app installer"],
                "ppt": ["Powerpoint", "Microsoft PowerPoint 97 - 2003 Document"],
                "pptx": ["Powerpoint", "Microsoft PowerPoint Document"],
                "rar": ["RAR Archive", "RAR Archive"],
                "rtf": ["RTF", "RTF"],
                "seven_zip": ["7zip", "7zip Archive"],
                "swf": ["Flash", "Adobe Flash File"],
                "xls": ["Excel", "Microsoft Excel 97 - 2003 Document"],
                "xlsx": ["Excel", "Microsoft Excel Document"],
                "zbundle": ["Apple-Mac", " Mac OS X app bundle in ZIP archive"]
}
