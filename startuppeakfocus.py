"""
Run an autopeakfocus (should be done before OOF)
"""
catp= Catalog("/home/astro-util/astridcats/wband_pointing.cat")
source="2253+1608"
AutoPeakFocus(source)

Break("Check and enter solutions")

