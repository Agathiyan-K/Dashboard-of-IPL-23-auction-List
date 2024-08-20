import streamlit as st
import pandas as pd
import plotly.express as px

# Read the dataset
file_id = '1of6Mee8v3__yhpbodnkhrhSFPBinOCCB'
file_path = f'https://drive.google.com/uc?id={file_id}'
df = pd.read_csv(file_path)

# Concatenate specialism and player names into a new column
df['Label'] = df['Specialism'] + ': ' + df['Name']
df['Label_Age'] = df['Age Group'] + ': ' + df['Name']

# Unique Reserve Prices
unique_reserve_prices = df['Reserve Price Rs Lakh'].unique()

# Sidebar for user input
st.sidebar.title("Select Options")

# Dropdown for selection
chart_dropdown = st.sidebar.selectbox(
    'Select Chart Type',
    ['Specialism vs Country Origin', 'Age Group vs Country Origin', 'Bubble Chart', 'Selected Player Details',
     'Sunburst Chart', 'Horizontal Bar Chart']
)

if chart_dropdown == 'Specialism vs Country Origin':
    # Treemap Chart
    st.title('Specialism vs Country Origin')
    selected_value = st.sidebar.selectbox('Select Origin', ['Country', 'State Association'])
    filtered_data = df[df['Country'] != 'India'] if selected_value == 'Country' else df[df['State Association'] != 'FOREIGNER']
    path = ['Country', 'Label'] if selected_value == 'Country' else ['State Association', 'Label']
    title = f'Specialism vs {"Country Origin" if selected_value == "Country" else "State Association"} (excluding {"India" if selected_value == "Country" else "FOREIGNER"})'
    fig = px.treemap(filtered_data, path=path, title=title)
    st.plotly_chart(fig)

elif chart_dropdown == 'Age Group vs Country Origin':
    # Sunburst Chart
    st.title('Age Group vs Country Origin')
    selected_value = st.sidebar.selectbox('Select Origin', ['Country', 'State Association'])
    filtered_data = df[df['Country'] != 'India'] if selected_value == 'Country' else df[df['State Association'] != 'FOREIGNER']
    path = ['Age Group', 'Country', 'Label_Age']
    title = f'Age Group vs {"Country Origin" if selected_value == "Country" else "State Association"} (excluding {"India" if selected_value == "Country" else "FOREIGNER"})'
    fig = px.sunburst(filtered_data, path=path, title=title)
    st.plotly_chart(fig)

elif chart_dropdown == 'Bubble Chart':
    # Bubble Chart
    st.title('Bubble Chart')
    selected_country_state = st.sidebar.selectbox('Select Origin', ['Country', 'State Association'])
    selected_caps = st.sidebar.selectbox('Select Caps', ['Test caps', 'ODI caps', 'T20 caps', 'IPL'])
    filtered_data = df[df['Country'] != 'India'] if selected_country_state == 'Country' else df[(df['Country'] == 'India') | (df['State Association'] != 'FOREIGNER')]
    title = f'Bubble Chart: Age vs {selected_caps}'
    filtered_data = filtered_data[(filtered_data['IPL'] != 0)]
    fig = px.scatter(filtered_data, x='Age', y=selected_caps, size='ODI caps', color='Country',
                     hover_name='Name', title=title)
    st.plotly_chart(fig)

elif chart_dropdown == 'Selected Player Details':
    # Bar Chart for selected player details
    st.title('Selected Player Details')
    selected_reserve_prices = st.sidebar.multiselect('Select Reserve Prices', unique_reserve_prices, [unique_reserve_prices[0]])
    selected_specialisms = st.sidebar.multiselect('Select Specialisms', df['Specialism'].unique(), list(df['Specialism'].unique()))
    selected_countries = st.sidebar.multiselect('Select Countries', df['Country'].unique(), list(df['Country'].unique()))
    filtered_data = df[df['Reserve Price Rs Lakh'].isin(selected_reserve_prices)]
    if selected_specialisms:
        filtered_data = filtered_data[filtered_data['Specialism'].isin(selected_specialisms)]
    if selected_countries:
        filtered_data = filtered_data[filtered_data['Country'].isin(selected_countries)]
    fig = px.bar(filtered_data, x='Name', y=['Test caps', 'ODI caps', 'T20 caps', 'IPL'],
                 title=f'Player/s on {", ".join(map(str, selected_reserve_prices))} Lakh Reserve Price Range',
                 labels={'value': 'Number of Caps'},
                 hover_data={'value': ':.0f'},
                 template='plotly_dark')
    st.plotly_chart(fig)

elif chart_dropdown == 'Sunburst Chart':
    # Sunburst Chart based on checklist selections
    st.title('Sunburst Chart')
    selected_countries = st.sidebar.multiselect('Select Countries', df['Country'].unique(), list(df['Country'].unique()))
    selected_specialisms = st.sidebar.multiselect('Select Specialisms', df['Specialism'].unique(), list(df['Specialism'].unique()))
    selected_age_groups = st.sidebar.multiselect('Select Age Groups', df['Age Group'].unique(), list(df['Age Group'].unique()))
    filtered_data = df[(df['Country'].isin(selected_countries)) &
                       (df['Specialism'].isin(selected_specialisms)) &
                       (df['Age Group'].isin(selected_age_groups)) &
                       (df['C/U/A'] == 'Uncapped') &
                       (df['IPL'] == 0)]
    fig = px.sunburst(filtered_data, path=['Country', 'State Association', 'Name'],
                      title='Players who are uncapped and never played IPL',
                      color='State Association')
    st.plotly_chart(fig)

elif chart_dropdown == 'Horizontal Bar Chart':
    # Horizontal Bar Chart based on checklist selections
    st.title('Horizontal Bar Chart')
    selected_countries = st.sidebar.multiselect('Select Countries', df['Country'].unique(), list(df['Country'].unique()))
    selected_rl = st.sidebar.multiselect('Select R/L', ['RHB', 'LHB'], ['RHB'])
    selected_specialisms = st.sidebar.multiselect('Select Specialisms', df['Specialism'].unique(), list(df['Specialism'].unique()))
    filtered_data = df[(df['Country'].isin(selected_countries)) &
                       (df['R/L'].isin(selected_rl)) &
                       (df['Specialism'].isin(selected_specialisms))]
    country_color_scale = px.colors.qualitative.Set1[:len(selected_countries)]
    fig = px.bar(filtered_data, y='Age Group', color='Country', facet_col='R/L',
                 text='Name',
                 title='Players by Age Group, Specialism, and R/L (Second Chart)',
                 labels={'Age Group': 'Player Age Group'},
                 template='plotly_dark',
                 orientation='h',
                 color_discrete_sequence=country_color_scale,
                 facet_col_wrap=2)
    st.plotly_chart(fig)
