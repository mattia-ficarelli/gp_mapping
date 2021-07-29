
from datetime import datetime
import urllib.request
import pandas as pd
import zipfile
import requests
import plotly
import plotly.graph_objects as go

#Plot 1 and 2 start
## Get EPRACCUR data from NHSD 
url = 'https://files.digital.nhs.uk/assets/ods/current/epraccur.zip'
filehandle, _ = urllib.request.urlretrieve(url)
zip_file_object = zipfile.ZipFile(filehandle, 'r')
first_file = zip_file_object.namelist()[0]
file = zip_file_object.open(first_file)
content = file.read()
csv_file = open('assets/data/epraccur_data.csv', 'wb')
csv_file.write(content)
csv_file.close()
header_list = ["Organisation Code", "Name", "National Grouping", "High Level Health Geography", "Address line 1", "Address line 2", "Address line 3", 
"Address line 4", "Address line 5","Postcode","Open Date","Close Date","Status Code","Organisation Sub-Type Code","Commissioner","Join Provider/Purchaser Date",
"Left Provider/Purchaser Date","Contact Telephone Number", "Null 1", "Null 2", "Null 3", "Amended Record Indicator", "Null 4", "Provider/Purchaser",
"Null 5", "Prescribing Setting", "Null 6"]
## Get EPRACCUR data from NHSD end 

##EPRACCUR data processing 
gp_practice_df = pd.read_csv('assets/data/epraccur_data.csv', names=header_list)
gp_practice_df.fillna('', inplace=True)
gp_practice_df['Partial Address'] = gp_practice_df[['Address line 1', 'Address line 2', 'Address line 3', 'Address line 4',]].agg(', '.join, axis=1)
gp_practice_df['Full Address'] = gp_practice_df[['Partial Address', 'Address line 5',]].agg(' '.join, axis=1)
gp_practice_df['Full Address'] = gp_practice_df['Full Address'].str.title()
gp_practice_df['Name'] = gp_practice_df['Name'].str.title()
gp_practice_df_1 = gp_practice_df.drop(columns = {"High Level Health Geography", "Address line 1", "Address line 2", "Address line 3", "Address line 4", 
"Address line 5", "Open Date", "Close Date", "Organisation Sub-Type Code", "Commissioner", "Join Provider/Purchaser Date", "Left Provider/Purchaser Date",
"Null 1", "Null 2", "Null 3", "Amended Record Indicator", "Null 4", "Partial Address", "Provider/Purchaser", "Null 5", "Null 6"})
gp_practice_df_2 =  gp_practice_df_1[gp_practice_df_1["Status Code"] == "A"]
gp_practice_df_3 =  gp_practice_df_2[gp_practice_df_2["Prescribing Setting"] == 4]
gp_practice_df_eng = gp_practice_df_3[gp_practice_df_3["National Grouping"].str.contains("YAC|YAD|YAE|YAF|W00")==False]
gp_practice_df_eng_1 = gp_practice_df_eng.reset_index(drop = True)
gp_practice_df_eng_2 = gp_practice_df_eng_1.copy()
gp_practice_df_eng_3 = gp_practice_df_eng_2.drop( columns = {"Status Code", "Prescribing Setting"})
gp_practice_df_ldn = gp_practice_df_eng_3[gp_practice_df_eng_3["National Grouping"].str.contains("Y56")==True]
gp_practice_df_ldn['Name'] = gp_practice_df_ldn['Name'].str.replace('Gp', 'GP')
gp_practice_df_ldn['Full Address'] = gp_practice_df_ldn['Full Address'].str.replace(' ,', ' ').str.replace('  ', ' ').str.replace('Gp', 'GP').map(lambda x: x.rstrip(', '))
gp_practice_df_ldn_2  = gp_practice_df_ldn[gp_practice_df_ldn["Name"].str.contains("Babylon")==False]
gp_practice_df_ldn_3 = gp_practice_df_ldn_2.reset_index(drop = True)
##EPRACCUR data processing end 

##Get Patients registered at GP practices data from NHSD
csv_url = "https://files.digital.nhs.uk/40/2232E5/gp-reg-pat-prac-all.csv"
req = requests.get(csv_url)
url_content = req.content
csv_file = open('assets/data/gp_pop_data.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
gp_pop_df = pd.read_csv('assets/data/gp_pop_data.csv')
gp_pop_df.rename(columns={'CODE': 'Organisation Code', 'NUMBER_OF_PATIENTS': 'Number of patients registered at GP practices in England'}, inplace=True)
gp_pop_df_1 = gp_pop_df.drop(columns = {'PUBLICATION', 'EXTRACT_DATE', 'TYPE', 'CCG_CODE', 'ONS_CCG_CODE', 'SEX', 'AGE', 'POSTCODE'})
##Get Patients registered at GP practices data from NHSD end 

##Merge EPRACCUR and patients registered at GP practices data 
gp_pop_ldn = gp_practice_df_ldn_3.join(gp_pop_df_1, rsuffix='Organisation Code')
gp_pop_ldn.rename(columns={'Number of patients registered at GP practices in England': 'Number of patients registered at GP practices in London'}, inplace=True)
gp_pop_ldn["Address"] = gp_pop_ldn[["Full Address", "Postcode"]].agg(', '.join, axis=1)
gp_pop_ldn_1 = gp_pop_ldn.drop(columns={'Organisation CodeOrganisation Code', 'National Grouping', 'Postcode', 'Full Address'})
##Merge EPRACCUR and patients registered at GP practices data end

##Visualization Plot 1
x0 = gp_pop_ldn_1['Number of patients registered at GP practices in London']
x1 = gp_pop_df_1['Number of patients registered at GP practices in England']
count_england = gp_pop_df_1['Number of patients registered at GP practices in England'].count()
count_london = gp_pop_ldn_1['Number of patients registered at GP practices in London'].count()
fig_1 = go.Figure()
fig_1.add_trace(go.Box(x=x0, 
boxmean=True,  
boxpoints= 'all', 
jitter=0.3, 
name="London", 
marker_color ="#0072CE", 
whiskerwidth=0.5, 
marker_size=3,
line_width=2))
fig_1.add_trace(go.Box(x=x1, 
boxmean=True, 
boxpoints= 'all', 
jitter=0.3, 
name="England", 
marker_color = "#003087", 
whiskerwidth=0.5, 
marker_size=3,
line_width=2))
fig_1.update_layout(
    {"plot_bgcolor": "rgba(0, 0, 0, 0)", "paper_bgcolor": "rgba(0, 0, 0, 0)"},
    font = dict(family = "Arial", size = 16),
    autosize=True,
    margin=dict(l=75, r=50, b=130, t=50, pad=4, autoexpand=True), hoverlabel=dict(
        font_size=12,
        font_family="Arial"
    ), xaxis=dict(title='Number of patients registered at individual GP practices', zeroline=False))
fig_1.add_annotation(dict(font=dict(family = "Arial",size=15),
                                        x=0.33,
                                        y=-0.40,
                                        showarrow=False,
                                        text="Number of GP practices in England: %s" %count_england,
                                        textangle=0,
                                        xanchor='right',
                                        xref="paper",
                                        yref="paper"))
fig_1.add_annotation(dict(font=dict(family = "Arial",size=15),
                                        x=0.323,
                                        y=-0.46,
                                        showarrow=False,
                                        text="Number of GP practices in London: %s" %count_london,
                                        textangle=0,
                                        xanchor='right',
                                        xref="paper",
                                        yref="paper"))   
##Visualization Plot 1 end 
                                      
## Write out to file (.html) Plot 1
config = {"displayModeBar": False, "displaylogo": False}
plotly_obj = plotly.offline.plot(
    fig_1, include_plotlyjs=False, output_type="div", config=config
)
with open("_includes/plotly_obj.html", "w") as file:
    file.write(plotly_obj)
## Write out to file (.html) Plot 1 end 

# Grab timestamp
data_updated = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Write out to file (.html)
html_str = (
    '<p><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16"><path fill-rule="evenodd" d="M1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0zM8 0a8 8 0 100 16A8 8 0 008 0zm.5 4.75a.75.75 0 00-1.5 0v3.5a.75.75 0 00.471.696l2.5 1a.75.75 0 00.557-1.392L8.5 7.742V4.75z"></path></svg> Latest Data: '
    + data_updated
    + "</p>"
)
with open("_includes/update.html", "w") as file:
    file.write(html_str)