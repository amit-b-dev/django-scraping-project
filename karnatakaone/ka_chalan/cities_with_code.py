class CityRtoList:
    city_rto_list = [
        {
            "city_code": "BN",
            "city_name": "Bengaluru",
            "rto_codes": [
                "KA01", "KA02", "KA03", "KA04", "KA05",
                "KA33", "KA50", "KA51", "KA52", "KA53",
                "KA54", "KA55", "KA56", "KA57", "KA58",
                "KA59", "KA60", "KA61", "KA62"
            ]
        },
        {
            "city_code": "MY",
            "city_name": "Mysuru",
            "rto_codes": [
                "KA09", "KA64", "KA65", "KA67",
                "KA68", "KA71", "KA72", "KA73", "KA74"
            ]
        },
        {
            "city_code": "BL",
            "city_name": "Ballari",
            "rto_codes": ["KA26", "KA27", "KA89"]
            # KA89 = Vijayanagara area earlier handled here also
        },
        {
            "city_code": "BG",
            "city_name": "Belagavi",
            "rto_codes": ["KA19", "KA38", "KA39", "KA96", "KA97", "KA98", "KA99"]
        },
        {
            "city_code": "HD",
            "city_name": "Hubballi-Dharwad",
            "rto_codes": ["KA17", "KA25"]
        },
        {
            "city_code": "DK",
            "city_name": "Mangaluru",
            "rto_codes": ["KA18", "KA19", "KA40"]
        },
        {
            "city_code": "SH",
            "city_name": "Shivamogga",
            "rto_codes": ["KA12", "KA42", "KA43"]
        },
        {
            "city_code": "DA",
            "city_name": "Davanagere",
            "rto_codes": ["KA13"]
        },
        {
            "city_code": "TU",
            "city_name": "Tumakuru",
            "rto_codes": ["KA06", "KA32", "KA47", "KA51", "KA54"]
        },
        {
            "city_code": "GU",
            "city_name": "Kalaburagi",
            "rto_codes": ["KA22", "KA23"]
        },
        {
            "city_code": "GA",
            "city_name": "Gadag",
            "rto_codes": ["KA16"]
        },
        {
            "city_code": "VJ",
            "city_name": "Vijayapur",
            "rto_codes": ["KA21"]
        },
        {
            "city_code": "UK",
            "city_name": "Karwar",
            "rto_codes": ["KA18", "KA40"]
        },
        {
            "city_code": "UD",
            "city_name": "Udupi",
            "rto_codes": ["KA20"]
        },
        {
            "city_code": "BK",
            "city_name": "Bagalkot",
            "rto_codes": ["KA20"]
        },
        {
            "city_code": "BD",
            "city_name": "Bidar",
            "rto_codes": ["KA38"]
        },
        {
            "city_code": "DN",
            "city_name": "Dandeli",
            "rto_codes": ["KA18"]
        },
        {
            "city_code": "CJ",
            "city_name": "Chamarajanagar",
            "rto_codes": ["KA75", "KA76", "KA77", "KA78"]
        },
        {
            "city_code": "CB",
            "city_name": "Chikballapur",
            "rto_codes": ["KA30", "KA48"]
        },
        {
            "city_code": "CK",
            "city_name": "Chikkamagaluru",
            "rto_codes": ["KA28", "KA81", "KA82", "KA83", "KA84", "KA85", "KA86", "KA87"]
        },
        {
            "city_code": "CT",
            "city_name": "Chitradurga",
            "rto_codes": ["KA14", "KA49"]
        },
        {
            "city_code": "HS",
            "city_name": "Hassan",
            "rto_codes": ["KA11", "KA44"]
        },
        {
            "city_code": "HV",
            "city_name": "Haveri",
            "rto_codes": ["KA15", "KA35", "KA36"]
        },
        {
            "city_code": "KL",
            "city_name": "Kolar",
            "rto_codes": ["KA07", "KA08", "KA48"]
        },
        {
            "city_code": "KP",
            "city_name": "Koppal",
            "rto_codes": ["KA25", "KA92", "KA93", "KA94"]
        },
        {
            "city_code": "MA",
            "city_name": "Mandya",
            "rto_codes": ["KA10", "KA66", "KA69"]
        },
        {
            "city_code": "RA",
            "city_name": "Raichur",
            "rto_codes": ["KA24"]
        },
        {
            "city_code": "RN",
            "city_name": "Ramanagara",
            "rto_codes": ["KA31", "KA45"]
        },
        {
            "city_code": "YG",
            "city_name": "Yadagiri",
            "rto_codes": ["KA23"]
        },
        {
            "city_code": "KD",
            "city_name": "Kodagu",
            "rto_codes": ["KA12", "KA52", "KA53"]
        },
        {
            "city_code": "BR",
            "city_name": "Bangalore Rural",
            "rto_codes": ["KA33", "KA58", "KA59", "KA60", "KA61"]
        },
        {
            "city_code": "VN",
            "city_name": "Vijayanagara",
            "rto_codes": ["KA35", "KA89", "KA91"]
        }
    ]
    @classmethod
    def get_city_by_vehicle_no(cls,vehicle_no: str):
        rto = vehicle_no.replace("-", "").upper()[:4]

        for item in cls.city_rto_list:
            if rto in item["rto_codes"]:
                return item["city_name"]
        return None
