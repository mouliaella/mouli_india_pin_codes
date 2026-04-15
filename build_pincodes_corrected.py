import csv
import os
import json
from collections import defaultdict

# 1. Configuration
input_csv = 'pincode.csv' # Rename your file to this
output_dir = "dist1"
os.makedirs(output_dir, exist_ok=True)

# 2. Data Storage
# Hierarchy: District -> List of Offices
district_map = defaultdict(list)
all_offices = []

print("Reading CSV...")

# 3. Robust CSV Reader
with open(input_csv, 'r', encoding='latin1') as f: # 'latin1' fixes common Indian Govt encoding errors
    reader = csv.DictReader(f)
    
    # Normalize headers (remove spaces/case issues)
    reader.fieldnames = [name.strip() for name in reader.fieldnames]
    
    for row in reader:
        # FILTER: Only process Telangana to save time/space
        if row.get('statename', '').upper() != 'TELANGANA':
            continue

        # Extract Available Data (Using .get() to avoid crashes)
        office = {
            "name": row.get('officename', 'Unknown'),
            "pincode": row.get('pincode', '000000'),
            "district": row.get('district', 'Unknown'),
            "division": row.get('divisionname', ''),
            "type": row.get('officetype', ''),
            "delivery": row.get('delivery', 'Unknown'),
            # Create a clean URL slug
            "slug": f"{row.get('pincode')}-{row.get('officename').replace(' ', '-').lower()}"
        }

        all_offices.append(office)
        district_map[office['district']].append(office)

print(f"Loaded {len(all_offices)} offices from {len(district_map)} districts.")

# 4. Generate "District Hub" Pages (The Navigation Layer)
# Creates a page like 'dist/jagtial-pincodes.html'
district_template = """
<!DOCTYPE html>
<html>
<head>
    <title>All Pincodes in {district} District, Telangana</title>
    <meta name="description" content="Complete list of {count} post offices in {district} district.">
    <style>
        body {{ font-family: sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }}
        .office-item {{ border-bottom: 1px solid #eee; padding: 10px 0; display: block; text-decoration: none; color: #333; }}
        .office-item:hover {{ background: #f9f9f9; color: #0056b3; }}
        .pincode {{ font-weight: bold; color: #0056b3; }}
    </style>
</head>
<body>
    <a href="index.html">Home</a> > <span>{district}</span>
    <h1>Post Offices in {district}</h1>
    <p>Found {count} offices.</p>
    <div class="list">
        {items}
    </div>

<footer style="margin-top: 40px; padding: 20px; background: #f1f1f1; text-align: center; font-size: 0.9em;">
    <a href="about.html">About Us</a> | 
    <a href="contact.html">Contact</a> | 
    <a href="privacy.html">Privacy Policy</a>
    <br><br>
    &copy; 2026 Telangana Pincode Directory. All rights reserved.
</footer>
</body>

</html>
"""

for district, offices in district_map.items():
    items_html = ""
    for off in offices:
        # Link to the individual detail page
        items_html += f'<a href="{off["slug"]}.html" class="office-item"><span class="pincode">{off["pincode"]}</span> - {off["name"]} ({off["type"]})</a>\n'
    
    page_content = district_template.format(
        district=district,
        count=len(offices),
        items=items_html
    )
    
    # Save District Page
    filename = f"{output_dir}/pincodes-in-{district.replace(' ', '-').lower()}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_content)

# 5. Generate "Detail" Pages (The Money Pages)
# Creates 6,000+ pages like 'dist/505327-jagtial-ho.html'
detail_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Pin Code of {name}, {district}</title>
    <style>
        body {{ font-family: sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }}
        .card {{ background: #f4f4f4; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .ad-slot {{ height: 100px; background: #eee; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center; margin: 20px 0; }}
    </style>
</head>
<body>
    <nav><a href="pincodes-in-{dist_slug}.html">Back to {district}</a></nav>
    
    <h1>{name} - Pincode {pincode}</h1>
    
    <div class="ad-slot">AdSense Here</div>

    <div class="card">
        <p><strong>District:</strong> {district}</p>
        <p><strong>State:</strong> Telangana</p>
        <p><strong>Division:</strong> {division}</p>
        <p><strong>Status:</strong> {delivery}</p>
    </div>

    <h3>Location</h3>
    <iframe 
        width="100%" 
        height="300" 
        frameborder="0" 
        style="border:0"
        src="https://maps.google.com/maps?q={pincode}+{name}+post+office&output=embed">
    </iframe>

<footer style="margin-top: 40px; padding: 20px; background: #f1f1f1; text-align: center; font-size: 0.9em;">
    <a href="about.html">About Us</a> | 
    <a href="contact.html">Contact</a> | 
    <a href="privacy.html">Privacy Policy</a>
    <br><br>
    &copy; 2026 Telangana Pincode Directory. All rights reserved.
</footer>
</body>
</html>
"""

print("Generating 6000+ detail pages...")
for off in all_offices:
    dist_slug = off['district'].replace(' ', '-').lower()
    
    html = detail_template.format(
        name=off['name'],
        pincode=off['pincode'],
        district=off['district'],
        division=off['division'],
        delivery=off['delivery'],
        dist_slug=dist_slug
    )
    
    with open(f"{output_dir}/{off['slug']}.html", 'w', encoding='utf-8') as f:
        f.write(html)

print("Success! Upload the 'dist' folder.")

# ... [Paste this at the bottom of your existing script] ...

# 6. Generate the Root Homepage (index.html)
print("Generating Homepage...")

# Sort districts alphabetically for a better user experience
sorted_districts = sorted(district_map.keys())

# Simple Homepage Template
home_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telangana Pincode Directory - Search by District</title>
    <meta name="description" content="Complete list of all post offices and pincodes in Telangana, organized by district.">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; max-width: 900px; margin: 0 auto; background-color: #f9f9f9; }}
        h1 {{ color: #2c3e50; text-align: center; margin-bottom: 40px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }}
        .district-card {{ 
            background: white; 
            padding: 20px; 
            border-radius: 8px; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
            text-align: center; 
            text-decoration: none; 
            color: #333; 
            transition: transform 0.2s;
            border: 1px solid #e0e0e0;
        }}
        .district-card:hover {{ transform: translateY(-5px); border-color: #0056b3; color: #0056b3; }}
        .count {{ display: block; font-size: 0.9em; color: #666; margin-top: 5px; }}
    </style>
</head>
<body>

    <h1>Telangana Pincode Directory</h1>
    
    <div class="grid">
        {district_links}
    </div>

 <footer style="margin-top: 40px; padding: 20px; background: #f1f1f1; text-align: center; font-size: 0.9em;">
    <a href="about.html">About Us</a> | 
    <a href="contact.html">Contact</a> | 
    <a href="privacy.html">Privacy Policy</a>
    <br><br>
    &copy; 2026 Telangana Pincode Directory. All rights reserved.
</footer>
</body>
</html>
"""

# Build the grid of links
links_html = ""
for dist in sorted_districts:
    # Calculate file name: 'pincodes-in-jagtial.html'
    file_name = f"pincodes-in-{dist.replace(' ', '-').lower()}.html"
    count = len(district_map[dist])
    
    links_html += f"""
    <a href="{file_name}" class="district-card">
        <strong>{dist}</strong>
        <span class="count">{count} Offices</span>
    </a>
    """

# Render and Save
final_home_html = home_template.format(district_links=links_html)

with open(f"{output_dir}/index.html", 'w', encoding='utf-8') as f:
    f.write(final_home_html)

print("Success! 'index.html' created. You can now open dist/index.html in your browser.")

# 7. Generate sitemap.xml (CRITICAL for Google Indexing)
print("Generating Sitemap...")

base_url = "https://telangana-pincodes.netlify.app" # CHANGE THIS after you deploy
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

# Add Home
sitemap_content += f"""
  <url>
    <loc>{base_url}/index.html</loc>
    <priority>1.0</priority>
  </url>
"""

# Add Districts
for dist in sorted_districts:
    slug = f"pincodes-in-{dist.replace(' ', '-').lower()}.html"
    sitemap_content += f"""
      <url>
        <loc>{base_url}/{slug}</loc>
        <priority>0.8</priority>
      </url>
    """

# Add All 6,300 Detail Pages
for off in all_offices:
    sitemap_content += f"""
      <url>
        <loc>{base_url}/{off['slug']}.html</loc>
        <priority>0.6</priority>
      </url>
    """

sitemap_content += '</urlset>'

with open(f"{output_dir}/sitemap.xml", 'w', encoding='utf-8') as f:
    f.write(sitemap_content)

print("Success! sitemap.xml generated.")

# ... [Paste this at the very bottom of your script] ...

# 8. Generate Legal Pages (Required for AdSense)
print("Generating Legal Pages...")

legal_styles = """
    <style>
        body { font-family: 'Segoe UI', sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; color: #333; }
        h1 { color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        h2 { margin-top: 30px; color: #0056b3; }
        .nav { margin-bottom: 30px; padding-bottom: 10px; border-bottom: 1px solid #eee; }
        a { color: #0056b3; text-decoration: none; }
    </style>
"""

legal_nav = '<div class="nav"><a href="index.html">Home</a> > <span>Legal</span></div>'

# --- Page 1: About Us ---
about_html = f"""
<!DOCTYPE html>
<html>
<head><title>About Us - Telangana Pincode Directory</title>{legal_styles}</head>
<body>
    {legal_nav}
    <h1>About Us</h1>
    <p>Welcome to the <strong>Telangana Pincode Directory</strong>, your reliable source for postal code information across the state.</p>
    
    <h2>Our Mission</h2>
    <p>Our goal is to simplify the search for accurate postal data in Telangana. Whether you are sending a courier, filling out a government form, or verifying an address, we provide the precise 6-digit Pincode you need.</p>
    
    <h2>Data Accuracy</h2>
    <p>Our data is sourced directly from public government records (Open Government Data Platform India - data.gov.in) and is regularly updated to reflect changes in districts and mandals. However, users are advised to double-check critical information with their local post office.</p>
<footer style="margin-top: 40px; padding: 20px; background: #f1f1f1; text-align: center; font-size: 0.9em;">
    <a href="about.html">About Us</a> | 
    <a href="contact.html">Contact</a> | 
    <a href="privacy.html">Privacy Policy</a>
    <br><br>
    &copy; 2026 Telangana Pincode Directory. All rights reserved.
</footer>
</body>
</html>
"""

# --- Page 2: Contact Us (Serverless Version) ---
contact_html = f"""
<!DOCTYPE html>
<html>
<head><title>Contact Us - Telangana Pincode Directory</title>{legal_styles}</head>
<body>
    {legal_nav}
    <h1>Contact Us</h1>
    <p>Have a question, found an error, or want to report a missing village? We are here to help.</p>
    
    <h2>Email Support</h2>
    <p>You can reach out to us directly via email:</p>
    <p><strong>Email:</strong> <a href="mailto:mouliaella@gmail.com">mouliaella@gmail.com</a></p>
    <p><em>(Please allow 24-48 hours for a response.)</em></p>
    
    <h2>Mailing Address</h2>
    <p>Telangana Pincode Directory Team<br>Jagtial, Telangana, India - 505327</p>
<footer style="margin-top: 40px; padding: 20px; background: #f1f1f1; text-align: center; font-size: 0.9em;">
    <a href="about.html">About Us</a> | 
    <a href="contact.html">Contact</a> | 
    <a href="privacy.html">Privacy Policy</a>
    <br><br>
    &copy; 2026 Telangana Pincode Directory. All rights reserved.
</footer>
</body>
</html>
"""

# --- Page 3: Privacy Policy (AdSense Standard) ---
privacy_html = f"""
<!DOCTYPE html>
<html>
<head><title>Privacy Policy - Telangana Pincode Directory</title>{legal_styles}</head>
<body>
    {legal_nav}
    <h1>Privacy Policy</h1>
    <p>Last Updated: April 2026</p>
    
    <h2>1. Information We Collect</h2>
    <p>We do not collect personal information (like names or phone numbers) from our visitors. We only collect anonymous usage data (log files) to improve the site experience.</p>
    
    <h2>2. Cookies and Web Beacons</h2>
    <p>We use cookies to store information about visitors' preferences. This includes third-party cookies from Google to serve ads based on your visits to this and other websites.</p>
    
    <h2>3. Google AdSense</h2>
    <p>Google, as a third-party vendor, uses cookies to serve ads on our site. Google's use of the DART cookie enables it to serve ads to our users based on their visit to our site and other sites on the Internet. Users may opt-out of the use of the DART cookie by visiting the Google ad and content network privacy policy.</p>

<footer style="margin-top: 40px; padding: 20px; background: #f1f1f1; text-align: center; font-size: 0.9em;">
    <a href="about.html">About Us</a> | 
    <a href="contact.html">Contact</a> | 
    <a href="privacy.html">Privacy Policy</a>
    <br><br>
    &copy; 2026 Telangana Pincode Directory. All rights reserved.
</footer>
</body>
    
</html>
"""

# Save files
with open(f"{output_dir}/about.html", 'w', encoding='utf-8') as f: f.write(about_html)
with open(f"{output_dir}/contact.html", 'w', encoding='utf-8') as f: f.write(contact_html)
with open(f"{output_dir}/privacy.html", 'w', encoding='utf-8') as f: f.write(privacy_html)

print("Success! Legal pages generated.")
