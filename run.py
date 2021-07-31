
from datetime import datetime
import urllib.request
import pandas as pd
import zipfile
import requests
import plotly
import plotly.graph_objects as go
import folium 
from branca.element import Template, MacroElement

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

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
gp_pop_ldn.rename(columns={'Number of patients registered at GP practices in England': 'Number of patients registered at the GP practice'}, inplace=True)
gp_pop_ldn["Address"] = gp_pop_ldn[["Full Address", "Postcode"]].agg(', '.join, axis=1)
gp_pop_ldn_1 = gp_pop_ldn.drop(columns={'Organisation CodeOrganisation Code', 'National Grouping', 'Full Address'})
gp_pop_ldn_1 = gp_pop_ldn_1[["Organisation Code", "Name", "Address", "Postcode", "Contact Telephone Number", "Number of patients registered at the GP practice"]]
##Merge EPRACCUR and patients registered at GP practices data end

##Visualization Plot 1
x0 = gp_pop_ldn_1['Number of patients registered at the GP practice']
x1 = gp_pop_df_1['Number of patients registered at GP practices in England']
count_england = gp_pop_df_1['Number of patients registered at GP practices in England'].count()
count_london = gp_pop_ldn_1['Number of patients registered at the GP practice'].count()
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
    margin=dict(l=75, r=50, b=160, t=30, pad=4, autoexpand=True), hoverlabel=dict(
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
                                        x=0.322,
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

#Merge new GP practice data with data from previous timepoint to avoid uncessary Nomatin API requests
file_name = 'assets/data/gp_pop_ldn_mapped.csv'
old_data = pd.read_csv(file_name, index_col=0)
gp_pop_ldn_1 = gp_pop_ldn_1.merge(old_data[['Organisation Code','loc', 'Point', 'Latitude', 'Longitude', 'Altitude']],on='Organisation Code', how = 'left')
gp_pop_ldn_1.rename(columns={'loc_x': 'loc', 'Point_x': 'Point', 'Latitude_x': 'Latitude', 'Longitude_x': 'Longitude', 'Altitude_x': 'Altitude' }, inplace=True)
#Merge new GP practice data with data from previous timepoint to avoid uncessary Nomatin API requests end

##Get GP practice coordinates using geopy if New GP practcies added to EPRACCUR 
geolocator = Nominatim(user_agent="open_access_nhs")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

if gp_pop_ldn_1['loc'].count() != gp_pop_ldn_1['Organisation Code'].count():
    missing_data = pd.isnull(gp_pop_ldn_1["loc"])
    missing_data_df = gp_pop_ldn_1[missing_data]
    missing_data_df["loc"] = missing_data_df["Postcode"].apply(geolocator.geocode)
    missing_data_df["Point"]= missing_data_df["loc"].apply(lambda loc: tuple(loc.point) if loc else None)
    missing_data_df[['Latitude', 'Longitude', 'Altitude']] = pd.DataFrame(missing_data_df['Point'].to_list(), index=missing_data_df.index)
    gp_pop_ldn_1 = gp_pop_ldn_1.dropna()
    gp_pop_ldn_1 = pd.concat([gp_pop_ldn_1, missing_data_df], ignore_index=True)
gp_pop_ldn_1.to_csv(file_name)
##Get GP practice coordinates using geopy if New GP practcies added to EPRACCUR end 

##Visualization Plot 2
gp_prac_pop_df_1 = pd.read_csv(file_name, index_col=0)
gp_prac_pop_df_1['GP Patient Number Quintile'] = pd.qcut(gp_prac_pop_df_1['Number of patients registered at the GP practice'], 5, labels=False)
gp_prac_pop_df_1['GP Patient Number Quintile'] = gp_prac_pop_df_1['GP Patient Number Quintile']  + 1
colordict = {1: 'green', 2: 'lightgreen', 3: 'orange', 4: 'red', 5: 'darkred'}
frame = folium.Figure(width=900, height=500)
fig_2 = folium.Map(
    location=[51.5, -0.1],
    tiles="cartodbpositron",
    zoom_start=10.2).add_to(frame)
for lat, lon, name, code, address, population, number, pop_qin in zip(gp_prac_pop_df_1['Latitude'], 
gp_prac_pop_df_1['Longitude'], 
gp_prac_pop_df_1['Name'],
gp_prac_pop_df_1['Organisation Code'], 
gp_prac_pop_df_1['Address'], 
gp_prac_pop_df_1['Number of patients registered at the GP practice'],
gp_prac_pop_df_1['Contact Telephone Number'], 
gp_prac_pop_df_1['GP Patient Number Quintile']):
    folium.CircleMarker(
        [lat, lon],
        radius=0.065*((population/2)**(1./2.)+35),
        popup = folium.Popup('<b>' + 'Name: ' + '</b>'  + str(name) + '<br>'
        '<b>' + 'GP Practice Code: ' + '</b>' + str(code) + '<br>'
        '<b>' + 'Address: ' + '</b>' + str(address) + '<br>'
        '<b>' + 'Telephone Number: ' + '</b>' + str(number) + '<br>'
        '<b>' + 'Number of Patients Registered: ' + '</b>' + str(population) + '<br>', max_width=len(address)*20),
        color='b',
        key_on = pop_qin,
        threshold_scale=[0,1,2,3,4,5],
        fill_color=colordict[pop_qin],
        fill=True,
        fill_opacity=0.8
        ).add_to(fig_2)
##Visualization Plot 2 end 

##CSS styling Plot 2 legend
template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; top: 20px;'>
     
<div class='legend-title'>GP Patient Number Quintile</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='width:8px;height:8px;background:green;opacity:0.8;'></span><p>&nbsp;&nbsp;</p>
1</li>
    <li><span style='width:12px;height:12px;background:lightgreen;opacity:0.8;'></span><p>&nbsp;&nbsp;</p>
2</li>
    <li><span style='width:16px;height:16px;background:orange;opacity:0.8;'></span><p>&nbsp;&nbsp;</p>
3</li>
    <li><span style='width:20px;height:20px;background:red;opacity:0.8;'></span><p>&nbsp;&nbsp;</p>
4</li>
    <li><span style='width:24px;height:24px;background:darkred;opacity:0.8;'></span><p>&nbsp;&nbsp;</p>
5</li>
  </ul>
  <!-- <ul class='legend-labels-2'>
    <li><span style='background:lightgreen;opacity:0.8;'></span></ul><ul class='legend-text'>2</li>
  </ul>
  <ul class='legend-labels-3'>
    <li><span style='background:orange;opacity:0.8;'></span></ul><ul class='legend-text'>3</li>
  </ul>
  <ul class='legend-labels-4'>
    <li><span style='background:red;opacity:0.8;'></span></ul><ul class='legend-text'>4</li>
  </ul>
  <ul class='legend-labels-5'>
    <li><span style='background:darkred;opacity:0.8;'></span></ul><ul class='legend-text'>5</li>
  </ul> -->
</div>
<b><div class='legend-source'>Note: </b>Circle radius is relative to the number <br> of patients registered at a GP practice</br></div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 85%;
    }
  .maplegend .legend-text {
    text-align: left;
    margin-bottom: 5px;
    font-size: 85%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels {
    display: flex;
    justify-content: space-between;
    width: 100%;
  }
  .maplegend ul.legend-labels li {
    display: flex;
    align-items: center;
  }
  .maplegend ul.legend-labels li span {
    height: 24px;
    width: 24px;
    border-radius: 5em;
  }

  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""
macro = MacroElement()
macro._template = Template(template)
fig_2.get_root().add_child(macro)
##CSS styling Plot 2 legend end 

## Write out to file (.html) Plot 2
fig_2.save("assets/folium/folium_obj.html", "w")
## Write out to file (.html) Plot 2

##Save data for plot 2 to csv
gp_prac_pop_df_tosave = gp_prac_pop_df_1.drop(columns ={'Postcode', 'loc', 'Point', 'Altitude'})
gp_prac_pop_df_tosave = gp_prac_pop_df_tosave.reset_index(drop = True)
gp_prac_pop_df_tosave.index.name = 'Unique ID'
gp_prac_pop_df_tosave.to_csv("assets/data/gp_pop_london_mapped_final.csv", index=False)
##Save data for plot 2 to end

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