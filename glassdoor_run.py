import glassdoor_scraper as gs
import pandas as pd

path = "/home/mplus/Documents/Learn/datascience/chromedriver"
df = gs.get_jobs("data scientist", 800, True, path, 4)

df.to_csv('glassdoor_jobs.csv', index=False)
