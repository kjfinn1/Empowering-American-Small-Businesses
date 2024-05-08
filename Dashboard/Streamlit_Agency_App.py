import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.title("Small Business Agency Recommender")

st.header("Returns the federal agencies that are most likely to contract with a business like yours.")

with st.form('Business Information'):
    st.subheader('**Enter information about your business. The more information, the better the recommendation.**')

    # Input widgets
    organizational_type = st.multiselect('Organizational Type, select all that apply:', 
                                         [
                                             #'Corporate, Tax Exempt',
                                             'Corporate, Not Tax Exempt',
                                             'Partnership/LLP',
                                             # 'Sole Proprietorship',
                                             # 'Small Agricultural Co-op',
                                             #'International Organization',
                                             #'Architecture & Engineering',
                                             #'Community-Owned Corp',
                                             #'Construction Firm',
                                             #'Domestic Shelter',
                                             #'Foundation',
                                             'Manufacturer of Goods',
                                             #'Research and Development',
                                             'Service Provider',
                                             #'Veterinary Hospital',
                                             #'Hispanic Servicing Institution',
                                             'Limited Liability Corp',
                                             #'Educational Institution',
                                             'For-Profit Organization'
                                         ])
    organizational_features = st.multiselect('Business Features, select all that apply:',
                                            [
                                                'Women-Owned',
                                                'Small Disadvantaged Business',
                                                'DOT-Certified Disadvantaged Business',
                                                '8(a) Firm',
                                                # '8(a) Joint Venture'
                                            ])

    naics_url = "https://www.naics.com/search/"
    naics_code = st.text_input('NAICS Code [(How do I find this?)](%s)' % naics_url)
    zip_code = st.text_input('5-digit Zip Code*')
    good_service = st.selectbox('Do you mainly provide goods or services?', 
                               ['Goods', 'Services'])
    place_manufacture = st.selectbox("Is the product you're selling manufactured in the US?",
                                  ['Yes', 'No', 'N/A (Service)'])
    veteran_status = st.multiselect('Veteran Status, select all that apply:',
                                   ['Service-Disabled Veteran-Owned',
                                   'Veteran-Owned'])
    contracts_per_year = st.number_input('Number of Contracts with Fed Govt per Year (Enter 0 if none or do not yet contract with Fed Govt)', value=0, step=1)
    st.write('*Indicates Required Field')

    submitted = st.form_submit_button('Submit') #boolean

# Checking Inputs
not_full = False
to_be_filled = []
if len(str(zip_code)) < 1:
    not_full = True
    to_be_filled.append("Zip Code")
    
if submitted and not_full:
    st.write(f"Please fill out the {','.join(to_be_filled)} field/s.")
    
elif submitted:
    place_of_manufacture_class = pd.Series(place_manufacture).map({'Yes': 'YES',
                                                       'No': 'NO',
                                                       'N/A (Service)': 'NONE'}).iloc[0]
    zip_code_region = str(zip_code)[:1] #grab region from zip code
    naics_code_sector = str(naics_code)[:4] #first 4 digits of NAICS Code
    good_service = pd.Series(good_service).map({'Goods': 'P',
                                     'Services': 'S'}).iloc[0]
    
    if 'Service-Disabled Veteran-Owned' in veteran_status:
        srdvob_flag = 'YES'
    else:
        srdvob_flag = 'NO'
        
    if 'Partnership/LLP' in organizational_type:
        llp = 'YES'
    else:
        llp = 'NO'
        
    if 'Veteran-Owned' in veteran_status:
        veteran_flag = 'YES'
    else:
        veteran_flag = 'NO'
        
    if 'Corporate, Not Tax Exempt' in organizational_type:
        corp_taxed = 'YES'
    else:
        corp_taxed = 'NO'
    
    if 'Manufacturer of Goods' in organizational_type:
        manufacturer = 'YES'
    else:
        manufacturer = 'NO'
    
    if 'Service Provider' in organizational_type:
        service_provider = 'YES'
    else:
        service_provider = 'NO'
        
    if 'For-Profit Organization' in organizational_type:
        for_profit = 'YES'
    else:
        for_profit = 'NO'
    
    if 'Limited Liability Corp' in organizational_type:
        llc = 'YES'
    else:
        llc = 'NO'
    
    if '8(a) Firm' in organizational_features:
        firm_8a = 'YES'
    else:
        firm_8a = 'NO'
    
    if '8(a) Joint Venture' in organizational_features:
        firm_8a_joint = 'YES'
    else:
        firm_8a_joint = 'NO'
    
    if 'Women-Owned' in organizational_features:
        women_flag = 'YES'
    else:
        women_flag = 'NO'
    
    if 'Small Disadvantaged Business' in organizational_features:
        sdb = 'YES'
    else:
        sdb = 'NO'
        
    if 'DOT-Certified Disadvantaged Business' in organizational_features:
        dot_small = 'YES'
    else:
        dot_small = 'NO'
    
    df = pd.DataFrame({
        'PLACE_OF_MANUFACTURE_CLASS': [place_of_manufacture_class],
        'PRINCIPAL_NAICS_CODE': [naics_code_sector],
        'PRODUCT_OR_SERVICE_TYPE': [good_service],
        'SERVICE_PROVIDER': [service_provider],
        'SRDVOB_FLAG': [srdvob_flag],
        'VENDOR_ADDRESS_ZIP_CODE': [zip_code_region],
        'VETERAN_OWNED_FLAG': [veteran_flag],
        'CORP_ENTITY_NOT_TAX_EXEMPT': [corp_taxed],
        'MANUFACTURER_OF_GOODS': [manufacturer],
        'FOR_PROFIT_ORGANIZATION': [for_profit],
        'LIMITED_LIABILITY_CORPORATION': [llc],
        'FIRM_8A_FLAG': [firm_8a],
        # 'FIRM_8A_JOINT_VENTURE': [firm_8a_joint],
        'WOMEN_OWNED_FLAG': [women_flag],
        'SDB': [sdb],
        'CONTRACTS_PER_YEAR': [contracts_per_year],
        'DOT_CERTIFIED_DISADV_BUS': [dot_small],
        'PARTNERSHIP_OR_LLP': [llp],
    })
    categoricals = df.select_dtypes(include=['object', 'category']).columns.tolist()
    quantitatives = df.columns.difference(categoricals)
    
    df_cat = pd.get_dummies(df[categoricals])
    if len(quantitatives) > 0:
        with open('Dashboard_Scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        df_quant = scaler.transform(df[quantitatives])
        df_quant = pd.DataFrame(df_quant, columns=quantitatives)
        df_cat = df_cat.reset_index()
    else:
        df_quant = df[quantitatives]
    
    df = pd.concat([df_cat, df_quant], axis=1).drop('index', axis=1)
    
    with open('Dashboard_Columns.pkl', 'rb') as f:
        dash_cols = pickle.load(f)
    
    df = df.reindex(columns=dash_cols, fill_value=False)
    
    # st.write(df)
    
    with open('Agency_Model_250.pkl', 'rb') as f:
        clf = pickle.load(f)
    
    probabilities = clf.predict_proba(df)
    
    def top_n(n):
        #top n classes (indices)
        input_top_n_indices = np.argsort(probabilities, axis=1)[:, -n:]
        #top n class labels
        input_predicted_labels = clf.classes_[input_top_n_indices]
        # #top n class probabilities
        # input_top_n_probabilities = np.take_along_axis(input_probabilities, input_top_n_indices, axis=1)
        #top n
        top_n_agencies = input_predicted_labels[0].tolist()
        top_n_agencies = pd.Series(top_n_agencies)
        top_n_agencies.name = 'Agency ID'
        return top_n_agencies
    
    top_agencies = top_n(20)
    
    with open('Agency_ID_to_Name.pkl', 'rb') as f:
        agency_id_to_name = pickle.load(f)
    with open('Class_IDs.pkl', 'rb') as f:
        class_label_to_id = pickle.load(f)
    with open('Agency_Contracts.pkl', 'rb') as f:
        agency_contracts = pickle.load(f)
    with open('Agency_Name_to_Link.pkl', 'rb') as f:
        agency_links = pickle.load(f)
    
    output_df = pd.DataFrame(top_agencies)
    
    output_df['Agency ID'] = output_df['Agency ID'].map(class_label_to_id)
    output_df['Agency Name'] = output_df['Agency ID'].map(agency_id_to_name)
    output_df['Bids per Contract (5th pct, AVG, 95th pct)'] = output_df['Agency ID'].map(agency_contracts).apply(lambda x: ', '.join([str(i) for i in list(x)]))
    output_df['Link to Agency Site'] = output_df['Agency Name'].map(agency_links)
    output_df['Agency Name'] = output_df.apply(lambda x: f'<a href="{x["Link to Agency Site"]}">{x["Agency Name"]}</a>', axis=1)
    output_df = output_df.drop('Link to Agency Site', axis=1)
    output_df.index += 1 
    
    html = output_df.to_html(escape=False, index=False)
    
    sam_url = 'https://sam.gov/search/'
    st.write("The Agency IDs below can be input directly into [SAM.gov](%s)'s Search function to filter by the agency." % sam_url)
    
    st.markdown(html, unsafe_allow_html=True)

    # st.write(output_df)
