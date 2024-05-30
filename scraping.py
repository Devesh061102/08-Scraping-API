from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Navigate to Indeed website
driver.get('https://www.indeed.com/')

# Input job title "data scientist"
input_job_name = driver.find_element(By.XPATH, '//*[@id="text-input-what"]')
input_job_name.send_keys('data scientist')

# Input location "Delhi"
input_location = driver.find_element(By.XPATH, '//*[@id="text-input-where"]')
input_location.clear()  # Clear the location field first
input_location.send_keys('Delhi')
input_location.send_keys(Keys.RETURN)

time.sleep(5)  # Wait for the page to load

# Create a DataFrame to store job details
df = pd.DataFrame({'Link': [], 'Job Title': [], 'Company': [], 'Location': [], 'Salary': [], 'Date': []})

# Loop through each page of job listings
while True:
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    # Find all job postings
    postings = soup.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result clickcard')
    
    # Extract details for each job posting
    for post in postings:
        link = post.find('a', class_='jobtitle turnstileLink').get('href')
        link_full = 'https://www.indeed.com' + link
        name = post.find('h2', class_='title').text.strip()
        company = post.find('span', class_='company').text.strip()
        try:
            location = post.find('div', class_='location accessible-contrast-color-location').text.strip()
        except:
            location = 'N/A'
        date = post.find('span', class_='date').text.strip()
        try:
            salary = post.find('span', class_='salaryText').text.strip()
        except:
            salary = 'N/A'
        
        # Append job details to the DataFrame
        df = df.append(
            {'Link': link_full, 'Job Title': name, 'Company': company, 'Location': location, 'Salary': salary, 'Date': date},
            ignore_index=True
        )

    # Check if there is a 'Next' button to navigate to the next page
    try:
        button = soup.find('a', attrs={'aria-label': 'Next'}).get('href')
        driver.get('https://www.indeed.com' + button)
        time.sleep(5)  # Wait for the next page to load
    except:
        break  # Exit the loop if no 'Next' button is found

# Process date and sort the DataFrame
df['Date_num'] = df['Date'].apply(lambda x: x[:2].strip())

def integer(x):
    try:
        return int(x)
    except:
        return x

df['Date_new'] = df['Date_num'].apply(integer)
df.sort_values(by=['Date_new', 'Salary'], inplace=True)

# Reorder columns and save to CSV
df = df[['Link', 'Job Title', 'Company', 'Location', 'Salary', 'Date']]
df.to_csv('indeed_scraped_data.csv', index=False)

# Close the WebDriver
driver.quit()
