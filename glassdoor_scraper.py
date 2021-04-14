from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path, slp_time, glassdoor_location=''):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')

    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path="/home/mplus/Documents/Learn/datascience/chromedriver", options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&sc.locationSeoString=california&locId=2280&locT=S'
    driver.get(url)
    
    try:
        driver.find_element_by_xpath('.//button[@data-test="search-bar-submit"]').click()
    except NoSuchElementException:
        pass

    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        # try:
        #     driver.find_element_by_class_name("selected").click()
        # except ElementClickInterceptedException:
        #     pass

        # time.sleep(.1)

        # try:
        #     # driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  #clicking to the X.
        #     driver.find_element_by_css_selector('[alt="Close"]').click()
        # except NoSuchElementException:
        #     pass

        
        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("react-job-listing")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  

            try:
                # driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  #clicking to the X.
                driver.find_element_by_css_selector('[alt="Close"]').click()
            except NoSuchElementException:
                pass

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(1)
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//div[contains(@class, "e1tk4kwz1")]').text
                    try:
                        company_name =  company_name[:(company_name.index('\n'))]
                    except:
                        pass
                    location = driver.find_element_by_xpath('.//div[contains(@class, "e1tk4kwz5")]').text
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "e1tk4kwz4")]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element_by_xpath('.//span[contains(@class, "css-16kxj2j")]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element_by_xpath('.//span[@data-test="detailRating"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                # print("Job Description: {}".format(job_description[:500]))
                print("Job Description: {}".format(job_description))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                company_overview = driver.find_element_by_xpath('.//div[@id="EmpBasicInfo"]').text

                try:
                    size = company_overview[(company_overview.index('Size\n')+len('Size\n')):company_overview.index('\nFounded')]
                except ValueError:
                    size = -1

                try:
                    size = company_overview[(company_overview.index('Size\n')+len('Size\n')):company_overview.index('\nType')]
                except ValueError:
                    size = -1

                try:
                    founded = company_overview[(company_overview.index('Founded\n')+len('Founded\n')):company_overview.index('\nType')]
                except ValueError:
                    founded = -1

                try:
                    type_of_ownership = company_overview[(company_overview.index('Type\n')+len('Type\n')):company_overview.index('\nIndustry')]
                except ValueError:
                    type_of_ownership = -1

                try:
                    industry = company_overview[(company_overview.index('Industry\n')+len('Industry\n')):company_overview.index('\nSector')]
                except ValueError:
                    industry = -1

                try:
                    sector = company_overview[(company_overview.index('Sector\n')+len('Sector\n')):company_overview.index('\nRevenue')]
                except ValueError:
                    sector = -1

                try:
                    revenue = company_overview[(company_overview.index('Revenue\n')+len('Revenue\n')):company_overview.index('\nVisit')]
                except ValueError:
                    revenue = -1

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1

                
            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            #add job to jobs

        # #Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//li[contains(@class, "e1gri00l3")]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.