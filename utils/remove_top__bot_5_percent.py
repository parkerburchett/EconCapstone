import pandas as pd
import numpy as np

def main():
    df = pd.read_csv(r"C:\Users\parke\Documents\GitHub\EconCapstone\utils\clean_final_data_out.csv")
    full_data = df.to_numpy()
    header = df.columns
    print(header)
    top_5_percent = 7.384592
    bot_5_percent = -12.733103
    total = len(full_data)
    too_large = 0
    too_small = 0
    keep =0
    data_to_keep =[]
    for row in full_data:
        if row[7]>= top_5_percent:
            too_large += 1
        elif row[7]<= bot_5_percent:
            too_small += 1
        else:
            keep +=1
            data_to_keep.append(row)

    final_np_array = np.array(data_to_keep)

    df2 = pd.DataFrame(final_np_array, columns=header)
    print(final_np_array[:10])
    print('The total data set', total)
    print('# to exclude due to to large {}'.format(too_large/total))
    print('# to exclude due to too small {}'.format(too_small / total))
    print('# to exclude due to to large {}'.format(keep / total))
    df2.to_csv('CleanFinalDataNoOutliers.csv', index=False)
main()