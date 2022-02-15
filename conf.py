# common config info
elastic_url_port = '10.48.58.252:9200'
input_dir = "inputfiles"
output_dir = 'metrics_threat_output'
output_filename = 'threat_samples'

# start and stop dates
# update
start_date = '2019-08-01'
stop_date = '2019-10-31'

# metrics_samples.py input filename and worksheet name
# update
input_file_data = {
    'verdict_all_all': ['filetypecountall_201908.xlsx', 'Day'],
    'verdict_all_NO245': ['samplefiletypecountNO245_201908.xlsx', 'Day'],
    'verdict_mal_all': ['malwarefiletypeall_201908.xlsx', 'Day'],
    'verdict_mal_NO245': ['malwarefiletypeNO245_201908.xlsx', 'Day'],
}

# metrics_apps.py input filename and worksheet name
# update
app_input_file = 'malwareapplication_201908.xlsx'
app_input_worksheet = 'Day'
app_output_file = 'threat_apps'

# metrics_sigs.py input filename and worksheet name
# update
sig_input_file = 'Sig_per_day_per_file.csv'
sig_input_worksheet = 'Day'
sig_output_file = 'threat_sigs'

# file name mappings raw, filegroup, and Autofocus naming
filetypetags = {
    "7z": ["7zip", "7zip Archive"],
    "apk": ["Android", "Android APK"],
    "bat": ["Script", "batch"],
    "class": ["Java", "JAVA Class"],
    "csv": ["CSV", "Comma-Separated Values"],
    "dex": ["Android", "Android DEX"],
    "dll": ["DLL", "DLL"],
    "dll32": ["DLL", "DLL"],
    "dll64": ["DLL", "DLL64"],
    "dmg": ["MacOSX", "MacOSX DMG"],
    "doc": ["Word", "Microsoft Word 97 - 2003 Document"],
    "docx": ["Word", "Microsoft Word Document"],
    "elf": ["ELF", "ELF"],
    "elink": ["Link", "Link"],
    "exe": ["PE", "PE"],
    "exe32": ["PE", "PE"],
    "exe64": ["PE", "PE64"],
    "fat": ["MacOSX", "Apple's Universal binary file"],
    "hta": ["HTML", "HTML Application"],
    "iqy": ["Excel Query", "Microsoft Web Query File"],
    "iso": ["ISO", "ISO"],
    "jar": ["Java", "JAVA JAR"],
    "java": ["Java", "JAVA Class"],
    "java_class": ["Java", "JAVA Class"],
    "js": ["Script", "JScript"],
    "lnk": ["Link", "Link"],
    "macho": ["MacOSX", "Mach-O"],
    "macro": ["Macro", " Macro"],
    "msi": ["Windows", "Windows Installer Package"],
    "NULL": ["Other", "Other"],
    "perl": ["Script", "Perl Script"],
    "pdf": ["PDF", "PDF"],
    "pdns": ["DNS", "Other"],
    "pkg": ["MacOSX", "Mac OS X app installer"],
    "ppt": ["Powerpoint", "Microsoft PowerPoint 97 - 2003 Document"],
    "pptx": ["Powerpoint", "Microsoft PowerPoint Document"],
    "ps1": ["PowerShell", "PowerShell"],
    "python": ["Python", "Python Script"],
    "rar": ["RAR Archive", "RAR Archive"],
    "rtf": ["RTF", "RTF"],
    "seven_zip": ["7zip", "7zip Archive"],
    "shell": ["Shell Script", "Shell Script"],
    "slk": ["Symbolic Link", "Microsoft Symbolic Link file"],
    "swf": ["Flash", "Adobe Flash File"],
    "unknown": ["Other", "Other"],
    "vbs": ["VBScript", "VBScript"],
    "xls": ["Excel", "Microsoft Excel 97 - 2003 Document"],
    "xlsx": ["Excel", "Microsoft Excel Document"],
    "zip": ["Zip", "zip Archive"],
    "zbundle": ["MacOSX", " Mac OS X app bundle in ZIP archive"]
}

sigfiletypes = {
    "7z": ["7zip", "7zip Archive"],
    "APK": ["Android", "Android APK"],
    "JAVA_CLASS": ["Java", "JAVA Class"],
    "dll32": ["DLL", "DLL"],
    "dll64": ["DLL", "DLL64"],
    "DMG": ["MacOSX", "MacOSX DMG"],
    "doc": ["Word", "Microsoft Word 97 - 2003 Document"],
    "docx": ["Word", "Microsoft Word Document"],
    "ELF": ["ELF", "ELF"],
    "elink": ["Link", "Link"],
    "PE": ["PE", "PE"],
    "exe64": ["PE", "PE64"],
    "fat": ["MacOSX", "Apple's Universal binary file"],
    "jar": ["Java", "JAVA JAR"],
    "java": ["Java", "JAVA Class"],
    "MACHO": ["MacOSX", "Mach-O"],
    "macro": ["Macro", " Macro"],
    "NULL": ["Other", "Other"],
    "PDF": ["PDF", "PDF"],
    "PKG": ["MacOSX", "Mac OS X app installer"],
    "ppt": ["Powerpoint", "Microsoft PowerPoint 97 - 2003 Document"],
    "pptx": ["Powerpoint", "Microsoft PowerPoint Document"],
    "RAR": ["RAR Archive", "RAR Archive"],
    "RAR5": ["RAR Archive", "RAR Archive"],
    "rtf": ["RTF", "RTF"],
    "RTDNS": ["RTDNS", "RTDNS"],
    "seven_zip": ["7zip", "7zip Archive"],
    "FLASH": ["Flash", "Adobe Flash File"],
    "xls": ["Excel", "Microsoft Excel 97 - 2003 Document"],
    "xlsx": ["Excel", "Microsoft Excel Document"],
    "zbundle": ["MacOSX", " Mac OS X app bundle in ZIP archive"],
    "OFFICE": ["MSFT Office", "Unknown"],
    "DNS": ["DNS", "Unknown"],
    "RAVEN": ["RAVEN", "Unknown"],
    "OPENOFFICE": ["MSFT Office", "Unknown"],
    "APP": ["APP", "Unknown"],
    "SWFZWS": ["SWFZWS", "Unknown"],
    "OLD_PDF": ["OLD_PDF", "Unknown"],
    "Script": ["Script", "Unknown"]
}
