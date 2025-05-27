import xml.etree.ElementTree as ET
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

files = glob.glob('C:/Users/felip/Desktop/School/CREST/Metal-Chelate-Complex-Analysis/Metal-Chelate-Complex-Graphs/SpecData/Cu + EDTA/*.smbl')

dataframes = []

for file in files:

    tree = ET.parse(file)
    root = tree.getroot()
    
    wavelengths = []
    absorbance_values = []
    
    for column in root.findall(".//DataColumn"):
        data_name = column.find("DataObjectName").text
        data_values = column.find("ColumnCells").text.strip().split('\n')

        temp = [float(i) for i in data_values if i.strip()]
        
        if data_name == "Wavelength":
            wavelengths = temp
        elif data_name == "Absorbance":
            absorbance_values = temp

    ratio_name = os.path.basename(file).replace('.smbl', '')
    if not wavelengths or not absorbance_values:
        print(f"Skipping file {ratio_name} due to missing data.")
    else:
        df = pd.DataFrame({
            'Wavelength': wavelengths,
            'Absorbance': absorbance_values
        })
        df['Ratio'] = ratio_name
        dataframes.append(df.copy())
        print(f"Processed file: {ratio_name}")

full_data = pd.concat(dataframes, ignore_index=True)


grouped_data = full_data.groupby('Ratio')
for ratio, group in grouped_data:
    print(f"\nRatio: {ratio}")
    print(group.head(3))

print(full_data['Ratio'].unique())

#JOBS PLOT
job_plot_data = []

for ratio, group in grouped_data:
    max_absorbance = group['Absorbance'].max()  # Maximum absorbance for each ratio
    try:
        # Extract the mole fraction of Cu from the ratio string
        mole_fraction = float(ratio.split('-')[0])
        print(mole_fraction)
        job_plot_data.append((mole_fraction, max_absorbance))
    except ValueError:
        # Skip if the ratio cannot be converted to a float (e.g., "Cu + Water")
        continue

# Convert the data into a DataFrame for plotting
job_df = pd.DataFrame(job_plot_data, columns=['Mole Fraction', 'Max Absorbance']).sort_values(by='Mole Fraction')

# Plot Job's Plot
plt.figure(figsize=(10, 6)) 
plt.plot(job_df['Mole Fraction'], job_df['Max Absorbance'], 'o-', color='blue')
plt.xlabel('Mole Fraction of Cu ion (Cu^2+/(Cu+EDTA))')
plt.ylabel('Absorbance at Maximum Peak')
plt.title("Job's Plot for Cu-EDTA Complex")
plt.grid(True)
plt.show()