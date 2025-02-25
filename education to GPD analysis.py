import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
    DS 2001
    Group 8 Final Project
    Global Education vs GDP
'''


'''
    Final Project Investigates the correlation between GDP and Education for a given Country
    Global Education Dataset measured in OOSR (Out of School Rates) for different demographics, as well as Literacy Rate measure by 15-24 year olds
    GDP Dataset shows multiple countries GDP per capita. GDP per capita is gross domestic product divided by midyear population
'''
Asian_Countries =[
    "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan",
    "Brunei", "Cambodia", "China", "Cyprus", "Georgia", "India", "Indonesia",
    "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait",
    "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia",
    "Myanmar (Burma)", "Nepal", "North Korea", "Oman", "Pakistan",
    "Palestine", "Philippines", "Qatar", "Saudi Arabia", "Singapore",
    "South Korea", "Sri Lanka", "Syria", "Tajikistan", "Thailand",
    "Timor-Leste", "Turkey", "Turkmenistan", "United Arab Emirates",
    "Uzbekistan", "Vietnam", "Yemen"
]
North_American_Countries = [
    "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada",
    "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "El Salvador",
    "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico",
    "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia",
    "Saint Vincent and the Grenadines", "Trinidad and Tobago", "United States"
]

South_American_Countries =  ["Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador",
    "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"]

European_Countries = [ "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina",
    "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia",
    "Finland", "France", "Germany", "Greece", "Hungary", "Iceland",
    "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania",
    "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands",
    "North Macedonia", "Norway", "Poland", "Portugal", "Romania",
    "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden",
    "Switzerland", "Ukraine", "United Kingdom", "Vatican City"]

Australian_Countries = [ "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia",
    "Nauru", "New Zealand", "Palau", "Papua New Guinea", "Samoa",
    "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"]

African_Countries = ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
    "Congo (Congo-Brazzaville)", "Djibouti", "Egypt", "Equatorial Guinea",
    "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana",
    "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya", "Lesotho",
    "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania",
    "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria",
    "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone",
    "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo",
    "Tunisia", "Uganda", "Zambia", "Zimbabwe"]

def read_file(filename, header):
    data = pd.read_csv(filename, header = header, encoding = "ISO-8859-1") #Special encoding to be able to open different CSV files
    return data

def logarithmic_data_processing(dataframe,gdp_column_name):

    # Parameters: Dataframe and GDP Column name
    # Function: Log to remove skew from the GDP Dataset
    # Returns: New Dataframe, 2 Histograms, One before log, one after
    # GDP datasets are often skewed with only a few having extremely high GDP's while the others are clustered together.

    dataframe[gdp_column_name].hist(bins = 30, color = "lightcoral", edgecolor = "black")
    plt.title("Histogram of GDP per Capita (2022) Prior to Log Transform")
    plt.xlabel("GDP")
    plt.ylabel("Frequency")
    plt.show()
    dataframe[gdp_column_name] = np.log(dataframe[gdp_column_name])

    dataframe[gdp_column_name].hist(bins = 30, color =  "yellowgreen", edgecolor = "black")
    plt.title("Histogram of GDP per Capita (2022) After to Log Transform")
    plt.xlabel("GDP")
    plt.ylabel("Frequency")
    plt.show()

    return dataframe

def top_bottom_performers(dataframe, category):

    # Organize Performance of Each Country based on the ratio of OSSR to GDP
        # Higher OSSR/GDP means that for a strong economy, there are still many unenrolled students
        # Lower OSSR/GDP means that the edcuation system and GDP are working efficiently
        # The dataset will be inversed, where the Top are more inefficeint than the bottom

    #Create a new column that shows the category (OSSR or Literacy) / GDP
    dataframe["Category / GDP"] = dataframe[category] / dataframe["2022"]

    #Create a Rank column
    if category == "Youth_15_24_Literacy_Rate_Male" or category == "Youth_15_24_Literacy_Rate_Female":
        dataframe["Rank"] = dataframe["Category / GDP"].rank(ascending=False)
    else:
        dataframe["Rank"] = dataframe["Category / GDP"].rank(ascending = True) #By setting it equal to True the values with lower ratios will be ranked higher

    #Sort by rank

    dataframe = dataframe.sort_values("Rank")

    return dataframe

def country_comparison(dataframe,country1, country2):

    #Parameters: 2 Strings for each of the country names
    #Function: Allows for Detailed Comparison of Specific 2 Countries. Creates Bar Plot showing Difference in GPD, Enrollment, and Literacy. These statistics will also be compared to an average value
    #Returns: Multiple Bar Graphs and Statistics

    #Collecting Average Values

    Avg_Primary_Male = (sum(dataframe["OOSR_Primary_Age_Male"])) / len(dataframe)
    Avg_Primary_Female = (sum(dataframe["OOSR_Primary_Age_Female"])) / len(dataframe)
    Avg_Upper_Secondary_Male = (sum(dataframe["OOSR_Upper_Secondary_Age_Male"])) / len(dataframe)
    Avg_Upper_Secondary_Female = (sum(dataframe["OOSR_Upper_Secondary_Age_Female"])) / len(dataframe)
    Avg_Youth_Literacy_Male = (sum(dataframe["Youth_15_24_Literacy_Rate_Male"])) / len(dataframe)
    Avg_Youth_Literacy_Female = (sum(dataframe["Youth_15_24_Literacy_Rate_Female"])) / len(dataframe)
    Avg_Country_GDP = (sum(dataframe["2022"])) / len(dataframe)

    #Isolating Row based on parameters

    Country1_row = dataframe[dataframe["Country Name"] == country1]
    Country2_row = dataframe[dataframe["Country Name"] == country2]

    #Find Values for Each Country

    # Extract Values

    #Values were taken out of pandas not as scalar and had to use .iloc[0] to extract scalar values
    #Sourced from Google

    Country1_Primary_Male = Country1_row["OOSR_Primary_Age_Male"].values[0]
    Country1_Primary_Female = Country1_row["OOSR_Primary_Age_Female"].values[0]
    Country1_Upper_Secondary_Male = Country1_row["OOSR_Upper_Secondary_Age_Male"].values[0]
    Country1_Upper_Secondary_Female = Country1_row["OOSR_Upper_Secondary_Age_Female"].values[0]
    Country1_Youth_Literacy_Male = Country1_row["Youth_15_24_Literacy_Rate_Male"].values[0]
    Country1_Youth_Literacy_Female = Country1_row["Youth_15_24_Literacy_Rate_Female"].values[0]
    Country1_GDP = Country1_row["2022"].values[0]

    Country2_Primary_Male = Country2_row["OOSR_Primary_Age_Male"].values[0]
    Country2_Primary_Female = Country2_row["OOSR_Primary_Age_Female"].values[0]
    Country2_Upper_Secondary_Male = Country2_row["OOSR_Upper_Secondary_Age_Male"].values[0]
    Country2_Upper_Secondary_Female = Country2_row["OOSR_Upper_Secondary_Age_Female"].values[0]
    Country2_Youth_Literacy_Male = Country2_row["Youth_15_24_Literacy_Rate_Male"].values[0]
    Country2_Youth_Literacy_Female = Country2_row["Youth_15_24_Literacy_Rate_Female"].values[0]
    Country2_GDP = Country2_row["2022"].values[0]

    colors = ["forestgreen", "dodgerblue", "forestgreen", "dodgerblue", "Gold", "Gold"]
    #Return Male and Female Primary Age and GDP Bar Graph
    data = {
        "Category": [
            "Primary Male OOSR " + country1,
            "Primary Male OOSR " + country2,
            "Primary Female OOSR " + country1,
            "Primary Female OOSR " + country2,
            "Avg Primary Male OOSR",
            "Avg Primary Female OOSR"
        ],
        "Values": [
            Country1_Primary_Male,
            Country2_Primary_Male,
            Country1_Primary_Female,
            Country2_Primary_Female,
            Avg_Primary_Male,
            Avg_Primary_Female,
        ]
    }

    #pandas plotting code sourced from Google

    plot_df = pd.DataFrame(data)
    ax = plot_df.plot(x = "Category", y = "Values", kind = "bar", color = colors, edgecolor = "black")
    ax.set_title("Comparison of Primary OOSR between " + country1 + " and " + country2 )
    plt.tight_layout()
    plt.show()

    #Return Male and Female Upper Secondary Age and GDP Bar Graph

    data = {
        "Category": [
            "Secondary Male OOSR " + country1,
            "Secondary Male OOSR " + country2,
            "Secondary Female OOSR " + country1,
            "Secondary Female OOSR " + country2,
            "Avg Secondary Male OOSR",
            "Avg Secondary Female OOSR"
        ],
        "Values": [
            Country1_Upper_Secondary_Male,
            Country2_Upper_Secondary_Male,
            Country1_Upper_Secondary_Female,
            Country2_Upper_Secondary_Female,
            Avg_Upper_Secondary_Male,
            Avg_Upper_Secondary_Female,
        ]
    }

    # pandas plotting code sourced from Google

    plot_df = pd.DataFrame(data)
    ax = plot_df.plot(x = "Category", y = "Values", kind="bar", color = colors, edgecolor = "black")
    ax.set_title("Comparison of Secondary OOSR between " + country1 + " and " + country2)
    plt.tight_layout()
    plt.show()

   #GDP Comparison
    data = {
        "Category": [
            "GDP " + country1,
            "GDP " + country2,
            "Avg GDP"
        ],
        "Values": [
            Country1_GDP,
            Country2_GDP,
            Avg_Country_GDP
        ]
    }

    # pandas plotting code sourced from Google

    plot_df = pd.DataFrame(data)
    ax = plot_df.plot(x = "Category", y = "Values", kind="bar", color = colors, edgecolor = "black")
    ax.set_title("Comparison of GDP between " + country1 + " and " + country2)
    plt.tight_layout()
    plt.show()

def lin_regression(data):
    """

    :param data:
    :return:
    """
    gdp_per_capita = data["2022"]
    lit_male = data["Youth_15_24_Literacy_Rate_Male"]
    lit_female = data["Youth_15_24_Literacy_Rate_Female"]
    oosrp_male = data["OOSR_Primary_Age_Male"]
    oosrp_female = data["OOSR_Primary_Age_Female"]
    oosrs_male = data["OOSR_Upper_Secondary_Age_Male"]
    oosrs_female = data["OOSR_Upper_Secondary_Age_Female"]
    def plot(ylim_min, ylim_max, data_used,title,ylabel):

        reg = np.polyfit(gdp_per_capita, data_used, deg=1)
        trend = np.polyval(reg, gdp_per_capita)
        plt.scatter(x=gdp_per_capita, y=data_used)
        plt.plot(gdp_per_capita, trend, "red")
        plt.ylim(ylim_min,ylim_max)
        plt.title(title)
        plt.xlabel("GDP per capita(thousands US$)")
        plt.ylabel(ylabel)
        plt.xlim(5.8,10.3)
        plt.show()


    plot(45,100,lit_male,"Linear Regression of Countries GDP per capita vs Male literacy rates","Male literacy rate")
    plot(45,100,lit_female,"Linear Regression of Countries GDP per capita vs Female literacy rates","Female literacy rate")
    plot(0,50,oosrp_male, "Linear Regression of Countries GDP per capita vs Out of School rates primary(male)", "Male Out of school rate primary")
    plot(0,50,oosrp_female, "Linear Regression of Countries GDP per capita vs Out of School rates primary(female)", "Female Out of school rate primary")
    plot(0,100, oosrs_male, "Linear Regression of Countries GDP per capita vs Out of School rates Secondary(male)", "Male Out of school rate secondary")
    plot(0,100, oosrs_female, "Linear Regression of Countries GDP per capita vs Out of School rates Secondary(female)", "Female Out of school rate secondary")

def GDP_Literacy(dataframe,Asia,Africa,North_America,South_America,Australia, Europe):
    dataframe["Rank"] = dataframe["2022"].rank(ascending = True)
    dataframe1 = dataframe.sort_values(by = "Rank", ascending = False)
    dataframe["Rank2"] = ((dataframe["Youth_15_24_Literacy_Rate_Male"] + dataframe["Youth_15_24_Literacy_Rate_Female"])/2).rank(ascending = True)
    dataframe2 = dataframe.sort_values(by = "Rank2", ascending = False)
    GDP_column_top_10 = dataframe1["Country Name"][:10]
    Literacy_Top_10 = dataframe2["Country Name"][:10]

    #print(GDP_column_top_10)
    #print(Literacy_Top_10)
    Asia_GDP = 0
    North_America_GDP = 0
    South_America_GDP = 0
    Africa_GDP = 0
    Australia_GDP = 0
    Europe_GDP = 0

    Asia_Literacy = 0
    North_America_Literacy = 0
    South_America_Literacy = 0
    Africa_Literacy = 0
    Australia_Literacy = 0
    Europe_Literacy = 0

    for country in GDP_column_top_10:
        if country in Asia:
            Asia_GDP += 1
        elif country in Africa:
            Africa_GDP += 1
        elif country in Europe:
            Europe_GDP += 1
        elif country in North_America:
            North_America_GDP += 1
        elif country in South_America:
            South_America_GDP += 1
        elif country in Australia:
            Australia_GDP += 1

    for country in Literacy_Top_10:
        if country in Asia:
            Asia_Literacy += 1
        elif country in Africa:
            Africa_Literacy += 1
        elif country in Europe:
            Europe_Literacy += 1
        elif country in North_America:
            North_America_Literacy += 1
        elif country in South_America:
            South_America_Literacy += 1
        elif country in Australia:
            Australia_Literacy += 1

    continents_labels = ["Europe","South America", "Asia", "Australia", "North America","Africa"]
    literacy_values = [Europe_Literacy,South_America_Literacy,Asia_Literacy,Australia_Literacy,North_America_Literacy,Africa_Literacy]
    gdp_values = [Europe_GDP,South_America_GDP,Asia_GDP,Australia_GDP,North_America_GDP, Africa_GDP]

    plt.bar(continents_labels,gdp_values, edgecolor = "black", width = 0.35, color = "navy")
    plt.ylabel("Amount of Countries with Top 10 GDP per Capita")
    plt.title("Frequency of Continents having Countries with Top 10 GDP per Capita")
    plt.grid()
    plt.show()

    plt.bar(continents_labels,literacy_values, edgecolor = "black", width = 0.35, color = "violet")
    plt.ylabel("Amount of Countries with Top 10 Literacy Rates")
    plt.title("Frequency of Continents with Top 10 Literacy Rates")
    plt.grid()
    plt.show()

    return Asia_Literacy, Asia_GDP, Africa_Literacy, Africa_GDP, Australia_GDP, Australia_Literacy, North_America_Literacy, North_America_GDP, South_America_GDP, South_America_Literacy, Europe_Literacy, Europe_GDP

def main():

    #Read files in

    # Local Education Filename : Global_Education.csv
    # Local GDP Filename: gdp_per_capita.csv

    Education_Data_Raw = read_file("Global_Education.csv", 0)
    GDP_Data_Raw = read_file("gdp_per_capita.csv", 2)

    # Cleaning
        # First Clean individual Datasets, then merge them by matching countries
        # Education Dataset is only interested in Primary Age and Upper Secondary Age OOSR rates, Male/Female Literacy Rate, and respective country name
        # Only use countries that have a Literacy Rate greater than 0. Countries with Literacy Rate = 0 taken to be errors due to lack of data
    Education_Data = Education_Data_Raw[(Education_Data_Raw["Youth_15_24_Literacy_Rate_Male"] > 0) | (Education_Data_Raw["Youth_15_24_Literacy_Rate_Female"] > 0)][["Countries and areas", "OOSR_Primary_Age_Male", "OOSR_Primary_Age_Female", "OOSR_Upper_Secondary_Age_Male","OOSR_Upper_Secondary_Age_Female", "Youth_15_24_Literacy_Rate_Male", "Youth_15_24_Literacy_Rate_Female"]]

        # GDP dataset only interested in most recent year and respective country name
        # Only use countries that have a GDP value above 0. Countries with values of zero are taken to be errors due to lack of data

    GDP_Data = GDP_Data_Raw[(GDP_Data_Raw["2022"] > 0)][["Country Name", "2022"]]

    # Merging Datasets
        # Merging based on countries still within both datasets after individual cleaning
        # Merged using pandas

    Education_GDP_Merged = pd.merge(Education_Data, GDP_Data, left_on="Countries and areas", right_on="Country Name")
    #print(Education_GDP_Merged.to_string())
    #print(Education_GDP_Merged.to_string())
    Education_GDP_Merged_Logged = logarithmic_data_processing(Education_GDP_Merged,"2022")

    Ranked_Primary_Male = top_bottom_performers(Education_GDP_Merged,"OOSR_Primary_Age_Male")["Country Name"].to_string()
    Ranked_Primary_Female = top_bottom_performers(Education_GDP_Merged,"OOSR_Primary_Age_Female")["Country Name"].to_string()
    Ranked_Secondary_Male = top_bottom_performers(Education_GDP_Merged,"OOSR_Upper_Secondary_Age_Male")["Country Name"].to_string()
    Ranked_Secondary_Female = top_bottom_performers(Education_GDP_Merged,"OOSR_Upper_Secondary_Age_Male")["Country Name"].to_string()
    Ranked_Literacy_Male = top_bottom_performers(Education_GDP_Merged,"Youth_15_24_Literacy_Rate_Male")["Country Name"].to_string()
    Ranked_Literacy_Female = top_bottom_performers(Education_GDP_Merged,"Youth_15_24_Literacy_Rate_Male")["Country Name"].to_string()

    #Print whole dataset to terminal
    #print(Ranked_Literacy_Female)
    #Country Comparison
    country_comparison(Education_GDP_Merged_Logged,"United States", "Sudan")

    #lin_regression(Education_GDP_Merged)
    x = GDP_Literacy(Education_GDP_Merged, Asian_Countries, African_Countries, North_American_Countries, South_American_Countries, Australian_Countries, European_Countries)
    #print(x)
    print("Asian GDP Count:", x[0], "Asian Literacy Count:", x[1])
    print("African GDP Count:", x[2], "African Literacy Count:" ,x[3])
    print("Australia GDP Count:", x[4], "Australia Literacy Count:", x[5])
    print("North American GDP Count:", x[6], "North American Literacy Count:", x[7])
    print("South American GDP Count:", x[8], "South American Literacy Count:", x[9])
    print("Europe GDP Count:", x[10], "Europe Literacy Count:", x[11])

    #country_comparison2(Education_GDP_Merged, "United States", "Sudan")
main()