import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Connect to database using sqlite, file is in the same folder
conn = sqlite3.connect('corona_per_state.db')

# Get cursor
cursor = conn.cursor()

# Select all rows and columns from sheet "CORONA_CASES", there is also "CORONA_DEATHS"
cursor.execute("SELECT * FROM CORONA_CASES")

# Get name of the fields... you should expect "Date", and then each state abbreviation alphabetically)
columns = [description[0] for description in cursor.description]

# Create pandas dataframe with data and columns
datas = pd.DataFrame(data=[line for line in cursor.fetchall()], columns=columns)

# Use pandas to get the Date and put it on the dataframe index, they are on the format DD/MM/YYYY
datas.Date = pd.to_datetime(datas.Date,dayfirst=True)
datas.index = datas.Date

# Add total of cases
datas['total'] = datas.sum(axis=1)

# Rearrange the columns names
columns = columns[1:]
columns.append('total')

plt.style.use('seaborn') #.context('Solarize_Light2')

# Matplotlib formatting to put the dates on the X axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
# Set an interval between labels so it won't be overcrowded
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=4))

# Plot data from each State that you wan, just change the abbreviation and title of the image
for col in columns:
    plt.plot(datas.index,datas[col])
    plt.gcf().autofmt_xdate()
    plt.grid(True)
    plt.title('Coronavirus Cases in ' + col)
    #plt.show()
    plt.savefig(col + '_cases.png', dpi=200)
    plt.close()
