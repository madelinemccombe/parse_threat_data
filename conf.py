# daily sample file data
samples_output = 'estackfiles/samplecounts.json'
samples_source = 'inputfiles/samplecount.xlsx'
samples_sheetname = 'day'
malware_source = 'inputfiles/malwaresamplecount.xlsx'
malware_sheetname = 'Day_mal'
sample_elkindex = 'samplecounts'

# filetype sample file data
filetypes_output = 'estackfiles/filecounts.json'
filetypes_source = 'inputfiles/malwarefiletype.xlsx'
filetypes_sheetname = 'malwaretypeday'
filetype_elkindex = 'samplecounts'

# Sig samples with filetype
sigfiletypes_output = 'estackfiles/sigcounts.json'
sigfiletypes_source = 'inputfiles/dailyAVsig.xlsx'
sigfiletypes_sheetname = 'Daily Sig count per filetype'
sigfiletype_elkindex = 'sigfiletypecounts'

# malware samples with application
app_output = 'estackfiles/appcounts.json'
app_source = 'inputfiles/malwareapplication.xlsx'
app_sheetname = 'MalAppDay'
app_elkindex = 'appcounts'