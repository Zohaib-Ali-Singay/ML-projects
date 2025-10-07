import streamlit  as st
import pickle
import pandas as pd
import numpy as np
import sklearn
# import the model

df = pickle.load(open('df.pkl', 'rb'))
st.title('Laptop Price Predictor')

# Brand
company = st.selectbox('Brand', df['brand'].unique())

if company == 'APPLE':
    weight = "Casual"
    processor_name = 'M1'
    processor_generation = '10th'
    os = 'Mac'
    os_bit = 64
    graphic_card_gb = 0
    hdd = 0
    touchscreen = 0
    msoffice = 0

    ram_type = st.selectbox('RAM Type', ['DDR3', 'DDR4', 'LPDDR4X']) # 0, 2, 4
    if ram_type == 'DDR3':
        ram_type = 0
    elif ram_type == 'DDR4':
        ram_type = 2
    
    else:
        ram_type = 4
    
    ram_gb_dict = {}
    for index, value in df.groupby(df[df['brand'] == 'APPLE']['ram_type']):
        ram_gb_dict[int(index)] = value['ram_gb'].unique()

    ram_gb = st.selectbox('Select RAM size', ram_gb_dict[ram_type])

    ssd_dict = {}
    df_temp = df[df['brand'] == 'APPLE']
    for index, value in df_temp.groupby(['ram_type', 'ssd']):
        ssd_dict[index[0]] = [index[1]]

    # Actually index and ram_type will have same value
    
    ssd = st.selectbox('SSD Memory', ssd_dict[ram_type])

    st.write('Type of Laptop is automatically selected as "Casual"')
    st.write('Processor name is automatically selected as "M1"')
    st.write('Processor Generation is automatically selected as "10th"')
    st.write('OS is automatically selected as "MAC"')
    st.write('OS-bit is automatically selected as "64"')
    st.write('Graphic Card Memory, HDD, MS Office and TouchScreen are automatically selected as 0')


else:
    dft = df[df['brand'] != 'APPLE']
    # Type(or weight) of Laptop
    weight = st.selectbox('Type', dft['weight'].unique())

    # Ram type
    st.write('Select 0 for "DDR3", 1 for "LPDDR3", 2 for "DDR4", 3 for "DDR4", 4 for "LPDDR4", 5 for "LPDDR4X" and 6 for "DDR5"')
    ram_type = st.selectbox("RAM Type", [0, 1, 2, 3, 4, 5])

    # Ram
    ram_gb = st.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])

    # Touch Screen
    touchscreen = st.selectbox('Touch Screen', ['No', 'Yes'])
    if touchscreen == "No":
        touchscreen = 0
    else:
        touchscreen = 1

    # Processor Name
    processor_name = st.selectbox('Process Name', dft['processor'].unique())

    # Processor Generation
    processor_generation = st.selectbox("Select Processor Generation", dft[dft['processor_gnrtn'] != 'Not Available']['processor_gnrtn'].unique())

    # ssd
    ssd = st.selectbox("Enter SSD Memory", dft['ssd'].unique())

    # hdd
    hdd = st.selectbox("Enter HDD Memory", dft['hdd'].unique())

    # OS
    os = st.selectbox("Choose Operating Systems", dft['os'].unique())

    # os_bit
    os_bit = st.selectbox("Choose the architecture", dft['os_bit'].unique())

    # graphic card gb
    graphic_card_gb = st.selectbox('Choose the graphic card memory', dft['graphic_card_gb'].unique())

    # msoffice
    msoffice = st.selectbox('MS Office', df['msoffice'].unique())

processor_generation_na = 0

no_of_ratings = st.number_input('Enter the number of Ratings of this laptop', min_value=0, step=1)
no_of_reviews = st.number_input('Enter the number of reviews', min_value=0, step=1)

if st.button("Predict Value"):
    pipe = pickle.load(open('best_model.pkl', 'rb'))
    #query = np.array([company, processor_generation, ram_gb, ram_type, ssd, hdd, os, os_bit, 
                      #graphic_card_gb, weight, touchscreen, msoffice, no_of_ratings, no_of_reviews, 
                      #processor_generation_na, processor_name])
    
    #query = pd.DataFrame(data = [[company], [processor_generation], [ram_gb], [ram_type], [ssd], [hdd], [os], [os_bit], 
                      #[graphic_card_gb], [weight], [touchscreen], [msoffice], [no_of_ratings], [no_of_reviews], 
                      #[processor_generation_na], [processor_name]], columns = df.drop(columns = ['Price']).columns.to_list())
    
    query = pd.DataFrame(data = {'brand' : [company], 'processor_gnrtn' : [processor_generation],'ram_gb' : [ram_gb], 
                                 'ram_type' : [ram_type], 'ssd' : [ssd], 'hdd' : [hdd], 'os' : [os], 'os_bit' : [os_bit], 
                      'graphic_card_gb' : [graphic_card_gb], 'weight' : [weight], 'Touchscreen' : [touchscreen], 
                      'msoffice' : [msoffice], 'Number of Ratings' : [no_of_ratings], 'Number of Reviews' : [no_of_reviews], 
                      'prcessor_gnrtn_na' : [processor_generation_na], 'processor' :[processor_name]})
    
    #query = query.reshape(1, 16)
    st.title(np.exp(pipe.predict(query)))