from zoneinfo import ZoneInfo
from adhanpy.PrayerTimes import PrayerTimes
from adhanpy.calculation import CalculationMethod
from datetime import date, timedelta
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Location coordinates for Istiqlal Mosque
location = [-6.169741002239878, 106.83109703180207]
zone = ZoneInfo("Asia/Jakarta")

# Number of days to track
num_days = 5000

# Lists to store data
days = []
fajr_times = []
dhuhr_times = []
asr_times = []
maghrib_times = []
isha_times = []

start_date = date.today()
for i in range(num_days):
    current_date = start_date + timedelta(days=i)
    prayer_times = PrayerTimes(
        location,
        current_date,
        CalculationMethod.SINGAPORE,
    )

    days.append(i + 1)
    fajr_times.append(prayer_times.fajr.astimezone(zone))
    dhuhr_times.append(prayer_times.dhuhr.astimezone(zone))
    asr_times.append(prayer_times.asr.astimezone(zone))
    maghrib_times.append(prayer_times.maghrib.astimezone(zone))
    isha_times.append(prayer_times.isha.astimezone(zone))


def datetime_to_hours(dt_list):
    return [dt.hour + dt.minute / 60 for dt in dt_list]


fajr_hours = datetime_to_hours(fajr_times)
dhuhr_hours = datetime_to_hours(dhuhr_times)
asr_hours = datetime_to_hours(asr_times)
maghrib_hours = datetime_to_hours(maghrib_times)
isha_hours = datetime_to_hours(isha_times)


def hours_to_time_str(hour_value):
    hours = int(hour_value)
    minutes = int((hour_value - hours) * 60)
    return f"{hours:02d}:{minutes:02d}"


print("\n" + "=" * 50)
print(f"PRAYER TIME STATISTICS ({num_days} days)")
print("=" * 50 + "\n")

prayers = {
    "Fajr": fajr_hours,
    "Dhuhr": dhuhr_hours,
    "Asr": asr_hours,
    "Maghrib": maghrib_hours,
    "Isha": isha_hours,
}

for prayer_name, prayer_hours in prayers.items():
    avg_time = sum(prayer_hours) / len(prayer_hours)
    min_time = min(prayer_hours)
    max_time = max(prayer_hours)
    range_time = max_time - min_time

    print(f"{prayer_name} Prayer:")
    print(f"  Average Time: {hours_to_time_str(avg_time)}")
    print(f"  Earliest:     {hours_to_time_str(min_time)}")
    print(f"  Latest:       {hours_to_time_str(max_time)}")
    print(f"  Time Range:   {int(range_time * 60)} minutes\n")

print("=" * 50 + "\n")

plt.figure(figsize=(12, 8))
plt.plot(days, fajr_hours, marker="o", label="Fajr", linewidth=2)
plt.plot(days, dhuhr_hours, marker="s", label="Dhuhr", linewidth=2)
plt.plot(days, asr_hours, marker="^", label="Asr", linewidth=2)
plt.plot(days, maghrib_hours, marker="d", label="Maghrib", linewidth=2)
plt.plot(days, isha_hours, marker="*", label="Isha", linewidth=2)

plt.xlabel("Day", fontsize=12)
plt.ylabel("Time (24-hour format)", fontsize=12)
plt.title(
    "Prayer Times Movement\n",
    fontsize=14,
    fontweight="bold",
)
plt.legend(loc="best", fontsize=10)
plt.grid(True, alpha=0.3)


def format_time(x, _):
    hours = int(x)
    minutes = int((x - hours) * 60)
    return f"{hours:02d}:{minutes:02d}"


plt.gca().yaxis.set_major_formatter(FuncFormatter(format_time))

plt.tight_layout()
plt.savefig("prayer_times_graph.png", dpi=300, bbox_inches="tight")
print("Graph saved as 'prayer_times_graph.png'")
plt.show()
