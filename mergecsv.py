import pandas as pd

file_names = ['galaxyU.csv', 'galaxy2U.csv', 'ISRO1U.csv', 'ISRO2U.csv', 'ISRO3U.csv', 'moondocU.csv', 'moondoc2U.csv', 'moondoc3U.csv', 'moondoc3aU.csv', 'moondoc3bU.csv', 'moondoc4U.csv', 'moondoc5U.csv', 'moondoc6U.csv', 'moondoc7U.csv', 'moondoc8U.csv', 'moondoc9U.csv', 'moondoc10U.csv', 'spaceM1U.csv', 'spaceM2U.csv', 'spaceM3U.csv', 'spaceM4U.csv', 'spaceM5U.csv', 'spaceM6U.csv']

data_frames = [pd.read_csv(file) for file in file_names]
data_dict = {}

for idx, file in enumerate(file_names):
    column_name = f'Column_{idx + 1}'  
    data_dict[column_name] = data_frames[idx].iloc[:, 0]

merged_df = pd.DataFrame(data_dict)
merged_df.to_csv('merged_file2.csv', index=False)
