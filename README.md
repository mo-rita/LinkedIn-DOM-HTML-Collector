# LinkedIn-DOM-HTML-Collector
Automated pipeline for collecting publicly available LinkedIn profile data. Downloads DOM-processed HTML via Power Automate and parses the files with Python to extract key CRM fields such as location, job history, and start dates. Outputs a clean CSV for CRM ingestion.

LinkedIn DOM HTML Collector
This project automates the extraction of publicly available LinkedIn profile information.
 It is divided into two main stages:
Download of DOM-processed LinkedIn HTML pages from a list of URLs in a CSV


Script execution to parse the downloaded files and generate a cleaned CSV (almost) ready for CRM ingestion



Requirements
Microsoft Power Automate


Browser with Developer Tools


Python 3.10+ and packages:


beautifulsoup4


pandas



 Input CSV Format
Column
Description
1
Unique CRM identifier (Primary Key)
2
LinkedIn profile URL

No headers allowed.

 Only valid LinkedIn profile URLs supported (Sales Navigator not allowed).
Example:
12345,https://www.linkedin.com/in/example-profile/
67890,https://www.linkedin.com/in/example2/


Step 1  Power Automate HTML Download Flow
The flow loops through each line of the CSV:
Reads ID and URL


Opens browser and navigates to LinkedIn


Validates page load (avoid 404)


Opens DevTools (F12)


Executes JavaScript to download DOM-processed HTML as %ID%.html


Waits 10s and proceeds to next iteration


Browser setup:
Manually open DevTools > Console > click last line before running the flow


Download file naming rule:
<ID>.html

JavaScript executed by DevTools:
(function() {
    const html = document.documentElement.outerHTML;
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = '%ID%.html';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
})();

Wait times prevent page load issues and throttling by LinkedIn.
Placeholder for flow diagram
[POWER AUTOMATE FLOW IMAGE]

Step 2 Python Parsing Script
The script loops through all downloaded HTML files in creation order and extracts:
Location


Current job title


Current company


Previous company


Start date at current company (first position)


Default fallback strings (e.g. "firm not found") are used when data cannot be parsed.
Example file structure:
/downloads
    12345.html
    67890.html

Filename (without extension) becomes the unique CRM identifier in the resulting CSV.

Known Limitations
Issue
Impact
Skills section rendered using <ul>
Can be interpreted as job roles
Multiple roles inside same company
Positional parsing may swap fields
Profiles with hidden roles ("see all experiences")
Start date may not be captured
Missing job title or experience section
Default fallback returned

Improvements are currently in progress.

Output
CSV formatted for CRM ingestion


Same ordering as input list


Achieved performance:
 ~1000 profiles processed in ~40 seconds



Output Example
contact_id
location
current_title
current_firm
previous_firm
start_date
12345
São Paulo
Analyst
Company A
Company B
Jan 2022
...
...
...
...
...
...



Disclaimer
This automation extracts public LinkedIn information that is already displayed to the user.
 Respect LinkedIn Terms of Service and ensure proper consent when ingesting data into a CRM.
