# bazi-calculate

## Run FastAPI

```
git clone https://github.com/phawitb/bazi-calculate.git
cd bazi-calculate

uvicorn bazi_calulate_fastapi:app --reload
```
```
POST :: http://127.0.0.1:8000/calculate_bazi
BODY :: 
{
    "date_input": "1976-04-19",
    "time_input": "11:23",
    "sex": "male"
}

***IF DON'T KNOW BIRTH TIME***
BODY :: 
{
    "date_input": "1976-04-19",
    "sex": "male"
}
```
```
RESPONSE ::
{
    "input_data": {
        "date_input": "1976-04-19",
        "time_input": "11:23",
        "sex": "male"
    },
    "four_pillars": {
        "Year": {
            "stem": "Bing (丙)",
            "branch": "Chen (辰)"
        },
        "Month": {
            "stem": "Ren (壬)",
            "branch": "Chen (辰)"
        },
        "Day": {
            "stem": "Xin (辛)",
            "branch": "Chou (丑)"
        },
        "Hour": {
            "stem": "Unknown",
            "branch": "Wu (午)"
        },
        "LunarDate": "1976-3-20"
    },
    "luck_pillars": [
        {
            "age": "0-10",
            "stem": "Example Stem",
            "branch": "Example Branch"
        },
        {
            "age": "10-20",
            "stem": "Example Stem",
            "branch": "Example Branch"
        },
        {
            "age": "20-30",
            "stem": "Example Stem",
            "branch": "Example Branch"
        },
        {
            "age": "30-40",
            "stem": "Example Stem",
            "branch": "Example Branch"
        },
        {
            "age": "40-50",
            "stem": "Example Stem",
            "branch": "Example Branch"
        },
        {
            "age": "50-60",
            "stem": "Example Stem",
            "branch": "Example Branch"
        },
        {
            "age": "60-70",
            "stem": "Example Stem",
            "branch": "Example Branch"
        },
        {
            "age": "70-80",
            "stem": "Example Stem",
            "branch": "Example Branch"
        },
        {
            "age": "80-90",
            "stem": "Example Stem",
            "branch": "Example Branch"
        }
    ],
    "percen_elements": {
        "Wood": 0.2,
        "Fire": 0.2,
        "Earth": 0.2,
        "Metal": 0.2,
        "Water": 0.2
    }
}
```

## Docker
```
sudo docker build -t fastapi-bazi .
```
