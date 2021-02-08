

import compute_elasticity

start_month ='2019-10'
end_month ='2020-05'

all_months = compute_elasticity.get_all_months()
start_index = all_months.index(start_month)
end_index = all_months.index(end_month)
months_between = all_months[start_index:end_index+1]
months_with_elasticity = months_between[2:-1]
print(start_month)
print(end_month)
print(months_between)
print(months_with_elasticity)