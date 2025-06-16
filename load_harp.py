import harp
reader = harp.create_reader(r'C:\Users\Phd Programme\Documents\CAJAL25\Experiments\test_test_2025_06_16T13_26_58\test_test_2025_06_16T13_26_58_HarpBehavior.harp')

dir(reader)

df = reader.AnalogData.read()
print(df.head())

