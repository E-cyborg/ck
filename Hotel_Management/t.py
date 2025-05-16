# import datetime
# import numpy as np

# dummy_data = [
#     {"form_date": datetime.date(2025, 1, 2), "to_date": datetime.date(2025, 3, 10), "rooms": [2, 4]},
#     {"form_date": datetime.date(2025, 4, 15), "to_date": datetime.date(2025, 4, 20), "rooms": [1, 3, 5]},
#     {"form_date": datetime.date(2025, 6, 7), "to_date": datetime.date(2025, 6, 12), "rooms": [2]},
#     {"form_date": datetime.date(2025, 8, 22), "to_date": datetime.date(2025, 8, 25), "rooms": [1, 4]},
#     {"form_date": datetime.date(2025, 9, 30), "to_date": datetime.date(2025, 10, 5), "rooms": [3, 6]}
# ]

# # Check for rooms booked between these dates
# m_f = datetime.date(2025, 1, 31)
# m_t = datetime.date(2025, 2, 1)

# l = []

# no_os_room=10


# for x in dummy_data:
#     if not (x["to_date"] < m_f or x["form_date"] > m_t):
#         l.append(x["rooms"])

# # Convert to unique 1D list
# l = np.array(l).ravel()
# l = sorted(set(map(int, l)))  # Sorted for readability

# avilable_rooms =[x for x in range(no_os_room) if x not in l]

# print(avilable_rooms)

from datetime import datetime,timedelta
print(datetime.today()+timedelta(days=30))
