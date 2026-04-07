import pandas as pd
import numpy as np

# Constraints: At least 100 rows, 5 columns 
data = {
    'wafer_id': [f"W-{i:03d}" for i in range(1, 151)],
    'batch_id': np.random.choice(['B-01', 'B-02', 'B-03'], 150),
    'critical_dimension_nm': np.random.normal(22, 0.5, 150), # Semiconductor feature size
    'defect_density': np.random.uniform(0.1, 5.0, 150),
    'yield_score': np.random.uniform(70, 99, 150),
    'process_temp': np.random.normal(180, 5, 150) # render 180°C
}

df = pd.DataFrame(data)
df.to_csv('custom_dataset.csv', index=False)
print("custom_dataset.csv generated with 150 rows.")