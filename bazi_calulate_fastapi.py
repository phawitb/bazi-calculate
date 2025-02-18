from datetime import datetime, timedelta
import pandas as pd
import lunarcalendar
from collections import Counter
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define Heavenly Stems & Earthly Branches
heavenly_stems = ["Jia (甲)", "Yi (乙)", "Bing (丙)", "Ding (丁)", "Wu (戊)",
                  "Ji (己)", "Geng (庚)", "Xin (辛)", "Ren (壬)", "Gui (癸)"]

earthly_branches = ["Zi (子)", "Chou (丑)", "Yin (寅)", "Mao (卯)", "Chen (辰)", 
                    "Si (巳)", "Wu (午)", "Wei (未)", "Shen (申)", "You (酉)", 
                    "Xu (戌)", "Hai (亥)"]

reference_date = datetime(1900, 1, 31)  # Reference for day stem/branch calculations

class BaziInput(BaseModel):
    date_input: str  # Format: YYYY-MM-DD
    time_input: str = None  # Optional, default is noon if not provided
    sex: str  # 'male' or 'female'

def get_heavenly_earthly_year(lunar_year):
    """ Compute the Heavenly Stem and Earthly Branch for a given lunar year. """
    stem_index = (lunar_year - 4) % 10
    branch_index = (lunar_year - 4) % 12
    return heavenly_stems[stem_index], earthly_branches[branch_index]

def get_heavenly_earthly_month(lunar_year, lunar_month):
    """ Compute the Heavenly Stem and Earthly Branch for a given lunar month. """
    branch_index = (lunar_month + 1) % 12  
    year_stem_index = (lunar_year - 4) % 10 
    stem_index = (year_stem_index * 2 + lunar_month) % 10 - 9
    return heavenly_stems[stem_index], earthly_branches[branch_index]

def get_heavenly_earthly_day(gregorian_date):
    """ Compute the Heavenly Stem and Earthly Branch for a given day. """
    days_since_reference = (gregorian_date - reference_date).days
    stem_index = (days_since_reference) % 10  # Offset by +6
    branch_index = (days_since_reference + 4) % 12  # Offset by +4
    return heavenly_stems[stem_index], earthly_branches[branch_index]

def get_earthly_branch_from_hour(input_time):
    """Determine the Earthly Branch (Shichen) from a given hour."""
    hour = int(input_time.split(":")[0])
    shichen_table = {
        (23, 24): earthly_branches[0], (0, 0.9): earthly_branches[0], 
        (1, 2): earthly_branches[1], (3, 4): earthly_branches[2], 
        (5, 6): earthly_branches[3], (7, 8): earthly_branches[4], 
        (9, 10): earthly_branches[5], (11, 12): earthly_branches[6], 
        (13, 14): earthly_branches[7], (15, 16): earthly_branches[8], 
        (17, 18): earthly_branches[9], (19, 20): earthly_branches[10], 
        (21, 22): earthly_branches[11]
    }
    for (start, end), branch in shichen_table.items():
        if start <= hour <= end:
            return branch
    return "Unknown"

def get_heavenly_earthly_hour(input_time, day_stem):
    """ Compute the Heavenly Stem and Earthly Branch for a given hour. """
    branch = get_earthly_branch_from_hour(input_time)
    return "Unknown", branch  # Placeholder logic

def get_stem_branch_for_date(date_str, time_input):
    """ Convert a Gregorian date to a Lunar date and return the Heavenly Stem and Earthly Branch. """
    gregorian_date = datetime.strptime(date_str, "%Y-%m-%d")
    lunar_date = lunarcalendar.Converter.Solar2Lunar(gregorian_date)

    year_stem, year_branch = get_heavenly_earthly_year(lunar_date.year)
    month_stem, month_branch = get_heavenly_earthly_month(lunar_date.year, lunar_date.month)
    day_stem, day_branch = get_heavenly_earthly_day(gregorian_date)
    hour_stem, hour_branch = get_heavenly_earthly_hour(time_input, day_stem)

    return {
        "Year": {"stem": year_stem, "branch": year_branch},
        "Month": {"stem": month_stem, "branch": month_branch},
        "Day": {"stem": day_stem, "branch": day_branch},
        "Hour": {"stem": hour_stem, "branch": hour_branch},
        "LunarDate": f"{lunar_date.year}-{lunar_date.month}-{lunar_date.day}"
    }

def AllBaziCalculate(date_input, time_inputs, sex):
    """ Main function to calculate BaZi Four Pillars & Luck Pillars. """
    
    # Set default time to 12:00 noon if not provided
    time_input = time_inputs if time_inputs else "12:00"

    # Calculate the Four Pillars
    stem_branch = get_stem_branch_for_date(date_input, time_input)

    # Placeholder Luck Pillars (needs full logic implementation)
    luck_pillars_list = [
        {"age": f"{10*i}-{10*(i+1)}", "stem": "Example Stem", "branch": "Example Branch"}
        for i in range(9)
    ]

    # Calculate element proportions (placeholder logic)
    element_counts = Counter(["Wood", "Fire", "Earth", "Metal", "Water"])
    total_elements = sum(element_counts.values())
    element_proportions = {key: value / total_elements for key, value in element_counts.items()}

    # Prepare the result
    results = {
        "input_data": {"date_input": date_input, "time_input": time_inputs, "sex": sex},
        "four_pillars": stem_branch,
        "luck_pillars": luck_pillars_list,
        "percen_elements": element_proportions
    }

    # If time input is None, remove the Hour pillar
    if time_inputs is None:
        results["four_pillars"]["Hour"] = None

    return results

@app.post("/calculate_bazi")
def calculate_bazi(input_data: BaziInput):
    """ API Endpoint for BaZi Calculation """
    result = AllBaziCalculate(input_data.date_input, input_data.time_input, input_data.sex)
    return result
