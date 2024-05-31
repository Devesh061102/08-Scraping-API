from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set Chrome options to use incognito mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

# Initialize the Chrome driver with options
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://in.indeed.com/jobs?q=data+scientist&l=Delhi')

# Create a dataframe to store job details
df = pd.DataFrame({'link': [], 'Job Title': [], 'Company': [], 'Location': [], 'Pay': [], 'Job Type': [], 'Shift and Schedule': []})

# Loop to go through each page and scrape job postings
while True:
    time.sleep(5)  # Allow time for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find job postings using updated CSS selectors
    postings = soup.find_all('div', class_='job_seen_beacon')

    # List to hold the job details for this page
    jobs_list = []

    # Extract job details and add to dataframe
    for post in postings:
        try:
            link_tag = post.find('a', class_='jcs-JobTitle')
            link = link_tag.get('href') if link_tag else None
            link_full = 'https://in.indeed.com' + link if link else 'N/A'
            link_text= str(link_full)
            name = link_tag.text.strip() if link_tag else 'N/A'
            
            company_tag = post.find('a', class_='css-1ioi40n e19afand0')
            company = company_tag.text.strip() if company_tag else 'N/A'
            
            location_tag = post.find('div', class_='companyLocation')
            location = location_tag.text.strip() if location_tag else 'N/A'
            
            salary_tag = post.find('div', class_='salary-snippet')
            salary = salary_tag.text.strip() if salary_tag else 'N/A'
            
            # Navigate to job details page
            driver.get(link_full)
            time.sleep(3)  # Allow time for the job details page to load
            job_soup = BeautifulSoup(driver.page_source, 'html.parser')
    
            
            # Extract pay, job type, shift and schedule
            pay = job_soup.find('div', {'aria-label': 'Pay'})
            pay_text = pay.find('div', {'class': 'js-match-insights-provider-tvvxwd ecydgvn1'}).text.strip() if pay else 'N/A'

            job_type = job_soup.find('div', {'aria-label': 'Job type'})
            job_type_text = job_type.find('div', {'class': 'js-match-insights-provider-tvvxwd ecydgvn1'}).text.strip() if job_type else 'N/A'

            shift = job_soup.find('div', {'aria-label': 'Shift and schedule'})
            shift_text = shift.find('div', {'class': 'js-match-insights-provider-tvvxwd ecydgvn1'}).text.strip() if shift else 'N/A'

            location_section = job_soup.find('div', {'id': 'jobLocationText'})
            location_text = location_section.find('span').text.strip() if location_section else location
            
            jobs_list.append(
                {'link': link_text, 'Job Title': name, 'Company': company, 'Location': location_text, 'Pay': pay_text, 'Job Type': job_type_text, 'Shift and Schedule': shift_text}
            )
            
            # Go back to the search results page
            driver.back()
            time.sleep(3)  # Allow time for the search results page to reload

        except Exception as e:
            print(f"Error extracting job details: {e}")

    # Concatenate the new jobs to the existing dataframe
    df = pd.concat([df, pd.DataFrame(jobs_list)], ignore_index=True)

    # Check for 'Next' button to go to the next page
    try:
        next_button = driver.find_element(By.XPATH, '//a[contains(@aria-label, "Next")]')
        next_button.click()
    except:
        break
    

# Save the dataframe to a CSV file
df.to_csv('indeed_scraped_data.csv', index=False)
print("Scraping completed and data saved to indeed_scraped_data.csv")

# Close the browser
driver.quit()
