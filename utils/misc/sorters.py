from typing import List, Dict


def lowprice_sort(hotels: List[Dict]):
    return sorted(hotels, key=lambda price: price["ratePlan"]["price"]["exactCurrent"])
