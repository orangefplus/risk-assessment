import pandas as pd

# Load your CSV file into a DataFrame
df = pd.read_csv('./result_29_company.csv')

# Merge 所属产业链 and 所属产业链1, and 所属产业链位置 and 所属产业链1位置
df['所属产业链合并'] = df['所属产业链'].fillna('') + df['所属产业链1'].fillna('')
df['所属产业链位置合并'] = df['所属产业链位置'].fillna('') + df['所属产业链1位置'].fillna('')

# Handle 所属产业链2 and 所属产业链2位置 based on the condition
# df.loc[df['所属产业链2'].str.startswith('其他', na=False), ['所属产业链2', '所属产业链2位置']] = [None, None]

# Delete the original four columns
df.drop(['所属产业链', '所属产业链1', '所属产业链位置', '所属产业链1位置'], axis=1, inplace=True)

# Rename the merged columns
df.rename(columns={'所属产业链合并': '所属产业链1', '所属产业链位置合并': '所属产业链1位置'}, inplace=True)

# Rearrange the columns to move 所属产业链2 and 所属产业链2位置 to the end
cols = [col for col in df.columns if col not in ['所属产业链2', '所属产业链2位置']]
cols += ['所属产业链2', '所属产业链2位置']  # Add these columns to the end
df = df[cols]

# Save the updated DataFrame to a new CSV file
df.to_csv('./result_29_company_v2.csv', index=False)
