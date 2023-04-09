import json

state_info = []

state_name = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

state_abbr = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

state_fips = ['01', '02', '04', '05', '06', '08', '09', '10', '12', '13', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56']

state_natural_gas_series = ['N5060AL2', 'NGM_EPG0_SAI_SAK_MMCF', '', 'N5060AR2', 'N5060CA2', 'N5060CO2', '', '', '', '', '', '', 'N5060IL2', 'N5060IN2', 'N5060IA2', 'N5060KS2', 'N5060KY2', 'N5060LA2', '', 'N5060MD2', '', 'N5060MI2', 'N5060MN2', 'N5060MS2', 'N5060MO2', 'N5060MT2', 'N5060NE2', '', '', '', 'N5060NM2', 'N5060NY2', '', '', 'N5060OH2', 'N5060OK2', 'N5060OR2', 'N5060PA2', '', '', '', 'N5060TN2', 'N5060TX2', 'N5060UT2', '', 'N5060VA2', 'N5060WA2', 'N5060WV2', '', 'N5060WY2']

base_station_id = 'GHCND:USW00'
station_id = ['013876', '026529', '003192', '053920', '093209', '093067', '014752', '013764', '012819', '003813', '021510', '004114', '053802', '093819', '094989', '013940', '093808', '013976', '014610', '093721', '094746', '094860', '094938', '053893', '053931', '024036', '004935', '093102', '014745', '093780', '023050', '004725', '013722', '024011', '053844', '053913', '024230', '014736', '014787', '053854', '024025', '013897', '053997', '093141', '094705', '093736', '094239', '013866', '000132', '024089']

for i in range(50):
    state_info.append(
        {
            'state': state_name[i],
            'abbr': state_abbr[i],
            'fips_code': state_fips[i],
            'station_id': f"{base_station_id}{station_id[i]}",
            'natural_gas_series': state_natural_gas_series[i],
        }
    )

with open('state info.json', 'w') as file:
    json.dump(state_info, file)
